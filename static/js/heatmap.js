var myMap = L.map("map", {
  center: [40.7, -73.95],
  zoom: 11
});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
maxZoom: 18,
id: "mapbox.streets",
accessToken: API_KEY
}).addTo(myMap);

var url = "https://data.cityofnewyork.us/resource/b2iz-pps8.json?";


d3.json(url, function(response) {
  
// console.log(response);
// var coordinates = [url.longitude, url.latitude];

var violations = heatArray
var heatArray = [];

for (var i = 0; i < response.length; i++) {
  
  var location = response[i].coordinates;

  if (response[i].latitude && response[i].longitude) {
    heatArray.push([response[i].latitude, response[i].longitude]);
  }
}
console.log(heatArray)
var heat = L.heatLayer(heatArray, {
  minOpacity: 0.05,
  maxZoom: 18,
  radius: 40,
  blur: 35  

  
}).addTo(myMap);




});

