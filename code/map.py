import folium
import folium.vector_layers
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from PyQt5.QtCore import QObject, pyqtSignal
import threading

class FoliumServer(BaseHTTPRequestHandler):
    def __init__(self, *args, mapInstance=None, **kwargs):
        self.mapInstance = mapInstance
        super().__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_POST(self):
        contentLength = int(self.headers['Content-Length'])
        postData = self.rfile.read(contentLength)

        jsonData = postData.decode("utf-8")
        
        try:
            data = json.loads(jsonData)
            if 'name' in data and self.mapInstance:
                self.mapInstance.marker_clicked.emit(data['name'])
            else:
                self.mapInstance.position_changed.emit(data['northWest']['lat'], data['northWest']['lng'], data['southEast']['lat'], data['southEast']['lng'])
        except json.JSONDecodeError:
            pass
        
        self._set_response()

class Map(QObject):

    position_changed = pyqtSignal(float, float, float, float)
    marker_clicked = pyqtSignal(str)

    def __init__(self, mapFilepath, coordinate, events, foliumPort=3001):
        super().__init__()

        self.map = folium.Map(coordinate, zoom_start=13)
        self.markers = {}

        for event in events:
            folium.Marker(
                location=(event.latitude, event.longitude),
                tooltip=event.name
            ).add_to(self.map)

        self.map.save(mapFilepath)

        self.html = None
        with open(mapFilepath, 'r', encoding='utf-8') as mapfile:
            self.html = mapfile.read()

        if events:
            self.find_all_markers_name()

        self.mapVariableName = self.find_variable_name(self.html, "map_")

        pend = self.find_end_of_slice(self.html, "L.map")
        self.html = self.html[:pend] + self.custom_map_code(self.mapVariableName, foliumPort) + self.html[pend + 1:]

        if events: 
            for key, value in self.markers.items():
                pend = self.find_end_of_slice(self.html, f"{value}.bindTooltip")
                self.html = self.html[:pend] + self.custom_marker_handler(value, key) + self.html[pend + 1:]

        with open(mapFilepath, 'w', encoding='utf-8') as mapfile:
            mapfile.write(self.html)

        self.listen_to_folium_map()

    def find_end_of_slice(self, html, pattern):

        startIndex = html.find(pattern)
        tmpHtml = html[startIndex:]

        found = 0
        index = 0
        openingFound = False
        while not openingFound or found > 0:
            if tmpHtml[index] == "(":
                found += 1
                openingFound = True
            elif tmpHtml[index] == ")":
                found -= 1

            index += 1
        endIndex = startIndex + index + 1

        return endIndex    

    def find_variable_name(self, html, nameStart):
    
        pattern = "var " + nameStart

        startIndex = html.find(pattern) + 4
        tmpHtml = html[startIndex:]
        endIndex = tmpHtml.find(" =") + startIndex

        return html[startIndex:endIndex]

    def find_all_markers_name(self):

        startIndex = self.html.find("var marker_")
        tmpHtml = self.html[startIndex:]
        startIndex = 0
        while startIndex != -1:
            endIndex = tmpHtml.find(" =")
            markerName = tmpHtml[startIndex + 4:endIndex]

            startIndex = tmpHtml.find("<div>")
            endIndex = tmpHtml.find("</div>")
            markerTooltip = tmpHtml[startIndex + 5:endIndex].replace('\n', '').lstrip().rstrip()
            self.markers[markerTooltip] = markerName

            tmpHtml = tmpHtml[endIndex + 6:]
            startIndex = tmpHtml.find("var marker_")

    def custom_marker_handler(self, markerVariableName, markerTooltip):
        return '''               
            %s.on('click', function(event) {

                if(lastSelectedMarker) {
                    lastSelectedMarker.setIcon(defaultIcon);
                }

                %s.setIcon(redIcon);
                lastSelectedMarker = %s;

                sendMarkerName('%s')
            });
        ''' % (markerVariableName,markerVariableName,markerVariableName,markerTooltip)

    def custom_map_code(self, mapVariableName, foliumPort):
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
        ''' % (mapVariableName, foliumPort, mapVariableName, mapVariableName, mapVariableName, foliumPort)

    def listen_to_folium_map(self, port=3001):
        serverAddress = ('', port)
        self.httpd = HTTPServer(serverAddress, lambda *args, **kwargs: FoliumServer(*args, mapInstance=self, **kwargs))

        thread = threading.Thread(target=self.httpd.serve_forever)
        thread.daemon = True
        thread.start()

    def __del__(self):
        self.httpd.server_close()