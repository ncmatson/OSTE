L.mapbox.accessToken = 'pk.eyJ1IjoiZGlnaXRhbGdsb2JlIiwiYSI6ImNpdHRkOWk0ZDAwMTUzMG4yM2g5Nmhtb2wifQ.O-5kuQ4vKzy0lcuqMAbBMA';

var map = L.mapbox.map('map').setView([41.89, 12.486], 16);

var layers = {
    "DG Maps API: Recent Imagery with Streets": L.mapbox.tileLayer('digitalglobe.nal0mpda'),
        "DG Maps API: Recent Imagery": L.mapbox.tileLayer('digitalglobe.nal0g75k'),
        "DG Maps API: Terrain Map":
L.mapbox.tileLayer('digitalglobe.nako1fhg'),
        "DG Maps API: Street Map":
L.mapbox.tileLayer('digitalglobe.nako6329')
};

var base = L.mapbox.tileLayer('digitalglobe.nal0g75k').addTo(map);

L.control.layers(layers, null, {
    collapsed: false
}).addTo(map);
