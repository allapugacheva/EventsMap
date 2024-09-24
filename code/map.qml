import QtQuick 2.0
import QtLocation 5.0
import QtPositioning 5.0

Map {
    id: map
    anchors.fill: parent
    center: QtPositioning.coordinate(53.9161154, 27.5873412) // Москва
    zoomLevel: 100

    plugin: Plugin {
        name: "osm" // Использование OpenStreetMap
    }

    function setCenter(lat, lon) {
        map.center = QtPositioning.coordinate(lat, lon);
    }  
}
