function buildCharts(firstOffense){

  // var url =`/crime/${firstOffense}`
  d3.json(`/crime/${firstOffense}`).then((trace)=>{
    console.log(trace);
  
      var data = [trace];
  
      var layout = {
          title: "Felonies per Borough",
          
      
        };
      Plotly.newPlot("plot",data,layout);
  
      });
  }
  
  
      function init() {
          // Grab a reference to the dropdown select element
          var selector = d3.select("#offense");
        
          // Use the list of sample names to populate the select options
          d3.json("/offense").then((sampleNames) => {
            sampleNames.forEach((sample) => {
              selector
                .append("option")
                .text(sample)
                .property("value", sample);
            });
        
            // Use the first sample from the list to build the initial plots
            const firstOffense = sampleNames[0];
            console.log(firstOffense)
            buildCharts(firstOffense);
            
          });
        }
  
        function optionChanged(firstOffense) {
          // Fetch new data each time a new sample is selected
          buildCharts(firstOffense);
        }
  
        init();