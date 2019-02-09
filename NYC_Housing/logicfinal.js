var url = "https://data.cityofnewyork.us/resource/b2iz-pps8.json?";

var heat = d3.json(url, function(response) {
  

  var heatArray = [];
  
  for (var i = 0; i < response.length; i++) {
    
    var location = response[i].coordinates;
  
    if (response[i].latitude && response[i].longitude) {
      heatArray.push([response[i].latitude, response[i].longitude]);
    }
  }
  console.log(heatArray)
  var heat = L.heatLayer(heatArray, {
    minOpacity: 0.1,
    maxZoom: 18,
    radius: 40,
    blur: 35,
  
  }); 
    
   
  var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
  });
  

  var baseMaps = {
    "Street Map": streetmap,
  };

  var overlayMaps = {
    Violations: heat
  };


var mymap = L.map("map", {
  center: [40.7, -73.95],
  zoom: 11,
  layers: [streetmap, heat]
});


var APILink = "http://data.beta.nyc//dataset/d6ffa9a4-c598-4b18-8caf-14abde6a5755/resource/74cdcc33-512f-439c-a43e-c09588c4b391/download/60dbe69bcd3640d5bedde86d69ba7666geojsonmedianhouseholdincomecensustract.geojson";
var State = "STATEFP10";

var url = APILink + State;



var geojson;
function NYCFilter(feature) {
  if (feature.properties.COUNTY === "New York County"||feature.properties.COUNTY === "Bronx County"||
  feature.properties.COUNTY === "Kings County"||feature.properties.COUNTY === "Queens County"||
  feature.properties.COUNTY === "Richmond County"
  ) return true
  }
// Grab data with d3
d3.json(url, function(data) {

  // Create a new choropleth layer
  geojson = L.choropleth(data, {filter: NYCFilter,

    // Define what  property in the features to use
    valueProperty: "MED_VAL",
    valueState: "STATEFP10",

    // Set color scale
    scale: ["#ffffb2", "#b10026"],

    // Number of breaks in step range
    steps: 10,

    // q for quartile, e for equidistant, k for k-means
    mode: "q",
    style: {
      // Border color
      color: "#fff",
      weight: 1,
      fillOpacity: 0.6
    },

    // Binding a pop-up to each layer
    onEachFeature: function(feature, layer) {
      layer.bindPopup(feature.properties.LOCALNAME + ", " + feature.properties.State + "<br>Median Home Value:<br>" +
        "$" + feature.properties.MED_VAL);
    }
  }).addTo(mymap);

  // Set up the legend
  var legend = L.control({ position: "bottomright" });
  legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");
    var limits = geojson.options.limits;
    var colors = geojson.options.colors;
    var labels = [];

    // Add min & max
    var legendInfo = "<h1>Median Home Value</h1>" +
      "<div class=\"labels\">" +
        "<div class=\"min\">" + limits[0] + "</div>" +
        "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
      "</div>";

    div.innerHTML = legendInfo;

    limits.forEach(function(limit, index) {
      labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
    });

    div.innerHTML += "<ul>" + labels.join("") + "</ul>";
    return div;
  };

  // Adding legend to the map
  legend.addTo(mymap);

  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(mymap);
  });

});
