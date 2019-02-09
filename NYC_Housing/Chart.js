var trace = {
    
    "x": [
    "BROOKLYN",
    "MANHATTAN",
    "QUEENS",
    "BRONX",
    "STATEN ISLAND",
        ],
    "y": [
    42814,
    34078,
    28320,
    27779,
    4607,
    ],
    "type": "bar",
    color: "purple",
        opacity: 0.5
    }

    var data = [trace]

    var layout = {
        title: "Felonies per Borough",
        
        
      };
    Plotly.newPlot("plot",data,layout);
