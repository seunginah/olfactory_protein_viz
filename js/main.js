function selectedSlice(txt) {
	print_txt = 'you have selected slice ' + txt;
	img_path = './images/Bmpr2/'+txt+'.jpg'
    document.getElementById("desc_slice").innerHTML = print_txt;
    document.getElementById("view_slice").src = img_path;
}

function selectedSegment(txt) {
	print_txt = 'you have selected segment ' + txt;
    document.getElementById("desc_segment").innerHTML = print_txt;
}


// Create chart objects associated with the container elements identified by the css selector. Note: It is often a good idea to have these objects accessible at the global scope so that they can be modified or filtered by other page controls.
var segment_hist = dc.barChart("#segment_hist");


d3.csv('../toy_dataset_long.csv', function(error, data) {
	if (error) {
		console.error('Error getting or parsing the data.');
        throw error;
    }
    console.log(data[0]);

    // create "dimensions"
    var cf = crossfilter(data),
    pixValueDim = cf.dimension(function (d) { return d.pix_value; }),
    pixFreqDim = cf.dimension(function (d) { return d.pix_freq; }),
    proteinDim = cf.dimension(function (d) { return d.protein; }),
    zoneDim = cf.dimension(function (d) { return d.zone; }),
    proteinGroup = proteinDim.group(),
    pixValueGroup = pixValueDim.group();

    console.log("cf.size(): ", cf.size())
    console.log(pixValueDim.top(10))
    console.log(pixValueGroup.all())
    console.log(proteinGroup.all())
    console.log(pixValueGroup.top(10))

    // given the pixel value as a dimension, return pixel frequency
    var valFreq = pixValueGroup.reduceSum(function(d) {return d.pix_freq; });

    // console.log(valFreq.value())

	segment_hist
    	.width(600)
    	.height(400)
    	.x(d3.scale.linear().domain([0,255]))
	    .brushOn(false)
	    .xAxisLabel("pixel value")
	    .yAxisLabel("frequency")
	    .dimension(pixValueDim)
	    .group(valFreq)
	    .elasticY(true)
	    .on('renderlet', function(chart) {
	        chart.selectAll('rect').on("click", function(d) {
	            console.log("click!", d);
	        });
	    });

	    segment_hist.render();

    // var random_chart = bubbleChart().width(600).height(600);
    // d3.select('#random_chart').data(data).call(random_chart);

    // pane 7 data table
    var sortAscending = true;
		  var table = d3.select('#page-wrap').append('table');
		  var titles = d3.keys(data[0]);

	var headers = table.append('thead').append('tr')
		                   .selectAll('th')
		                   .data(titles).enter()
		                   .append('th')
		                   .text(function (d) {
			                    return d;
		                    })
		                   .on('click', function (d) {
		                	   headers.attr('class', 'header');
		                	   
		                	   if (sortAscending) {
		                	     rows.sort(function(a, b) { return b[d] < a[d]; });
		                	     sortAscending = false;
		                	     this.className = 'aes';
		                	   } else {
		                		 rows.sort(function(a, b) { return b[d] > a[d]; });
		                		 sortAscending = true;
		                		 this.className = 'des';
		                	   }
		                	   
		                   });
		  
		  var rows = table.append('tbody').selectAll('tr')
		               .data(data).enter()
		               .append('tr');

		  rows.selectAll('td')
		    .data(function (d) {
		    	return titles.map(function (k) {
		    		return { 'value': d[k], 'name': k};
		    	});
		    }).enter()
		    .append('td')
		    .attr('data-th', function (d) {
		    	return d.name;
		    })
		    .text(function (d) {
		    	return d.value;
		    });
});
