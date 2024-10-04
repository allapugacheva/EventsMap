import folium
import folium.vector_layers
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from PyQt5.QtCore import QObject, pyqtSignal
import threading

class FoliumServer(BaseHTTPRequestHandler):
    def __init__(self, *args, map_instance=None, **kwargs):
        self.map_instance = map_instance
        super().__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        json_data = post_data.decode("utf-8")
        
        try:
            data = json.loads(json_data)
            if 'name' in data and self.map_instance:
                self.map_instance.marker_clicked.emit(data['name'])
            else:
                self.map_instance.position_changed.emit(data['northWest']['lat'], data['northWest']['lng'], data['southEast']['lat'], data['southEast']['lng'])
        except json.JSONDecodeError:
            pass
        
        self._set_response()

class Map(QObject):

    position_changed = pyqtSignal(float, float, float, float)
    marker_clicked = pyqtSignal(str)

    def __init__(self, map_filepath, coordinate, events, folium_port=3001):
        super().__init__()

        self.map = folium.Map(coordinate, zoom_start=13)
        self.markers = {}

        for event in events:
            folium.Marker(
                location=(event.latitude, event.longitude),
                tooltip=event.name
            ).add_to(self.map)

        self.map.save(map_filepath)

        self.html = None
        with open(map_filepath, 'r', encoding='utf-8') as mapfile:
            self.html = mapfile.read()

        if events:
            self.findAllMarkersName()

        self.map_variable_name = self.find_variable_name(self.html, "map_")

        pend = self.find_end_of_slice(self.html, "L.map")
        self.html = self.html[:pend] + self.custom_map_code(self.map_variable_name, folium_port) + self.html[pend + 1:]

        if events: 
            for key, value in self.markers.items():
                pend = self.find_end_of_slice(self.html, f"{value}.bindTooltip")
                self.html = self.html[:pend] + self.custom_marker_handler(value, key) + self.html[pend + 1:]

        with open(map_filepath, 'w', encoding='utf-8') as mapfile:
            mapfile.write(self.html)

        self.listen_to_folium_map()

    def find_end_of_slice(self, html, pattern):

        start_index = html.find(pattern)
        tmp_html = html[start_index:]

        found = 0
        index = 0
        opening_found = False
        while not opening_found or found > 0:
            if tmp_html[index] == "(":
                found += 1
                opening_found = True
            elif tmp_html[index] == ")":
                found -= 1

            index += 1
        end_index = start_index + index + 1

        return end_index    

    def find_variable_name(self, html, name_start):
    
        variable_pattern = "var "
        pattern = variable_pattern + name_start

        start_index = html.find(pattern) + 4
        tmp_html = html[start_index:]
        end_index = tmp_html.find(" =") + start_index

        return html[start_index:end_index]

    def findAllMarkersName(self):

        start_index = self.html.find("var marker_")
        tmp_html = self.html[start_index:]
        start_index = 0
        while start_index != -1:
            end_index = tmp_html.find(" =")
            marker_name = tmp_html[start_index + 4:end_index]

            start_index = tmp_html.find("<div>")
            end_index = tmp_html.find("</div>")
            marker_tooltip = tmp_html[start_index + 5:end_index].replace('\n', '').lstrip().rstrip()
            self.markers[marker_tooltip] = marker_name

            tmp_html = tmp_html[end_index + 6:]
            start_index = tmp_html.find("var marker_")

    def custom_marker_handler(self, marker_variable_name, marker_tooltip):
        return '''               
            %s.on('click', function(event) {

                if(lastSelectedMarker) {
                    lastSelectedMarker.setIcon(defaultIcon);
                }

                %s.setIcon(redIcon);
                lastSelectedMarker = %s;

                sendMarkerName('%s')
            });
        ''' % (marker_variable_name,marker_variable_name,marker_variable_name,marker_tooltip)

    def custom_map_code(self, map_variable_name, folium_port):
        return '''
            function handleMapChanges(event) {
                if(lastSelectedMarker) {
                    lastSelectedMarker.setIcon(defaultIcon);
                    lastSelectedMarker = null;
                }

                var bounds = %s.getBounds();

                var northWest = bounds.getNorthWest();
                var southEast = bounds.getSouthEast();

                fetch('http://localhost:%s', {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        northWest: {
                            lat: northWest.lat,
                            lng: northWest.lng
                        },
                        southEast: {
                            lat: southEast.lat,
                            lng: southEast.lng
                        }
                    })
                });                
            }

            %s.on('moveend', handleMapChanges);

            %s.on('click', handleMapChanges);

            function getCenterCoordinates() {
                var center = %s.getCenter();
                return center.lat + ', ' + center.lng;
            }

            var lastSelectedMarker = null;

            var defaultIcon = new L.Icon.Default();

            var redIcon = new L.Icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
                shadowSize: [41, 41]
            });

            function sendMarkerName(name) {
                fetch('http://localhost:%s', {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: name // Используем переданное имя
                    })
                });
            }
        ''' % (map_variable_name, folium_port, map_variable_name, map_variable_name, map_variable_name, folium_port)

    def listen_to_folium_map(self, port=3001):
        server_address = ('', port)
        self.httpd = HTTPServer(server_address, lambda *args, **kwargs: FoliumServer(*args, map_instance=self, **kwargs))

        thread = threading.Thread(target=self.httpd.serve_forever)
        thread.daemon = True  # Позволяем потоку завершиться, когда основная программа завершится
        thread.start()

    def __del__(self):
        self.httpd.server_close()