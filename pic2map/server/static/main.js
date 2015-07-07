// Map centered in NowSecure HQ by default
var map = L.map('map').setView([40.2001925,-89.0876265], 3);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

console.log('Adding markers for ' + rows.length + ' rows');
rows.forEach(function(row) {
    var coordinates = [row.latitude, row.longitude];
    var text = 'Filename: ' + row.filename;
    if (row.datetime) {
      text += '<br>GPS datetime: ' + row.datetime;
    }

    L.marker(coordinates).addTo(map).bindPopup(text);
});
