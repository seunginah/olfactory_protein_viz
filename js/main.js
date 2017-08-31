// Create chart objects associated with the container elements identified by the css selector. Note: It is often a good idea to have these objects accessible at the global scope so that they can be modified or filtered by other page controls.
var segment_hist = dc.barChart("#segment_hist");

var zone_row = dc.rowChart('#zone_row');
var view_data = dc.dataTable('#view_data');

// example charts from https://dc-js.github.io/dc.js/
// following this tutorial https://dc-js.github.io/dc.js/docs/stock.html
// var gainOrLossChart = dc.pieChart('#gain-loss-chart');
// var fluctuationChart = dc.barChart('#fluctuation-chart');
// var quarterChart = dc.pieChart('#quarter-chart');
// var dayOfWeekChart = dc.rowChart('#day-of-week-chart');
// var moveChart = dc.lineChart('#monthly-move-chart');
// var volumeChart = dc.barChart('#monthly-volume-chart');
// var yearlyBubbleChart = dc.bubbleChart('#yearly-bubble-chart');
// var nasdaqCount = dc.dataCount('.dc-data-count');
// var nasdaqTable = dc.dataTable('.dc-data-table');

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
    proteinSliceSegment = cf.dimension(function (d) { return d.protein + '_' + d.image + '_' + d.segment + '_' + d.zone});
    
    // create filters

    // create groups
    var proteinGroup = proteinDim.group(),
    pixValueGroup = pixValueDim.group(),
    zoneGroup = zoneDim.group();

    console.log("cf.size(): ", cf.size())
    console.log(pixValueDim.top(10))
    console.log(pixValueGroup.all())
    console.log(proteinGroup.all())
    console.log(pixValueGroup.top(10))

    // create reduce functions
    // given the pixel value as a dimension, return pixel frequency
    var valFreq = pixValueGroup.reduceSum(function(d) {return d.pix_freq; });
    // console.log(valFreq.value())

    // this row chart allows filtering of zones until i figure out how to view them all
    zone_row
        .width(400)
        .height(400)
        .margins({top: 20, left: 10, right: 10, bottom: 20})
        .group(zoneGroup)
        .dimension(zoneDim)
        // .ordinalColors(['#3182bd', '#9ecae1', '#dadaeb'])
        .label(function (d) {
            return d.key;
        })
        .title(function (d) {
            return d.value;
        })
        .elasticX(true)
        .xAxis().ticks(4);    

    zone_row.render();

    // view image histogram (it's actually implemented as a bar chart tho)
	segment_hist
    	.width(600)
    	.height(400)
    	.x(d3.scale.linear().domain([0,255]))
	    .brushOn(false)
	    .xAxisLabel("Pixel value")
	    .yAxisLabel("Frequency")
	    .dimension(pixValueDim)
	    .group(valFreq)
	    .elasticY(true)
	    .on('renderlet', function(chart) {
	        chart.selectAll('rect').on("click", function(d) {
	            console.log("you clicked on:", d);
	        });
	    });

	segment_hist.render();

    // var random_chart = bubbleChart().width(600).height(600);
    // d3.select('#random_chart').data(data).call(random_chart);

    // pane 7 data table
	// Data table does not use crossfilter group but rather a closure as a grouping function
    view_data
	    .dimension(proteinSliceSegment)
	    .group(function (d) { return d.protein })
	    .columns(['protein','image','zone','segment','area','std_dev','std_error','avg_pix_intensity','num_pix','pix_value','pix_freq'])

	view_data.render();
});
