// Map centered in NowSecure HQ by default
var map = L.map('map').setView([40.2001925,-89.0876265], 3);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
