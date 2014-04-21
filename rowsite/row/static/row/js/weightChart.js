
var _weights = []
var _datetimes = []

$( "#_toggle-weight-table" ).click(function() {
  	$( "#_weight-table" ).toggle();
});

$( '._weight').each(function( index ) {
	_weights.push(parseFloat($(this).text()));
});
$( '._weight-datetime').each(function( index ) {
	datetime = $(this).text();
	index = datetime.indexOf(",");
	index = datetime.indexOf(",", index + 1);
	datetime = datetime.substring(0, index);
	ms = Date.parse(datetime);
	_datetimes.push(ms);
});


	var new_weights = [];
	var new_dates = [];
	var for_chart = [];
	var old = _datetimes[0];
	var sum = _weights[0];
	var n = 1;
	for (var i = 1; i < _datetimes.length; i++) {
		if (old != _datetimes[i]) {
			avg_weight = (1.0 * sum) / n;
			new_dates.push(old);
			new_weights.push(avg_weight);
			for_chart.push([old, avg_weight]);
			sum = _weights[i];
			n = 1;
		} else {
			n += 1; sum += _weights[i];
		}
		old = _datetimes[i];

		
	}
	new_dates.push(old);
	new_weights.push((1.0 * sum) / n);

if (new_dates.length > 1) {
	var ctx = $("#_weight-chart").get(0).getContext("2d");


	var data = {
		labels : new_dates,
		datasets : [
			{
				fillColor : "rgba(151,187,205,0.5)",
				strokeColor : "rgba(151,187,205,1)",
				pointColor : "rgba(151,187,205,1)",
				pointStrokeColor : "#fff",
				data : new_weights
			}
		]
	}

	var options = {
					
		//Boolean - If we show the scale above the chart data			
		scaleOverlay : false,
		
		//Boolean - If we want to override with a hard coded scale
		scaleOverride : false,
		
		//** Required if scaleOverride is true **
		//Number - The number of steps in a hard coded scale
		scaleSteps : null,
		//Number - The value jump in the hard coded scale
		scaleStepWidth : null,
		//Number - The scale starting value
		scaleStartValue : null,

		//String - Colour of the scale line	
		scaleLineColor : "rgba(0,0,0,.1)",
		
		//Number - Pixel width of the scale line	
		scaleLineWidth : 1,

		//Boolean - Whether to show labels on the scale	
		scaleShowLabels : true,
		
		//Interpolated JS string - can access value
		scaleLabel : "<%=value%>",
		
		//String - Scale label font declaration for the scale label
		scaleFontFamily : "'Arial'",
		
		//Number - Scale label font size in pixels	
		scaleFontSize : 12,
		
		//String - Scale label font weight style	
		scaleFontStyle : "normal",
		
		//String - Scale label font colour	
		scaleFontColor : "#666",	
		
		///Boolean - Whether grid lines are shown across the chart
		scaleShowGridLines : true,
		
		//String - Colour of the grid lines
		scaleGridLineColor : "rgba(0,0,0,.05)",
		
		//Number - Width of the grid lines
		scaleGridLineWidth : 1,	
		
		//Boolean - Whether the line is curved between points
		bezierCurve : true,
		
		//Boolean - Whether to show a dot for each point
		pointDot : true,
		
		//Number - Radius of each point dot in pixels
		pointDotRadius : 3,
		
		//Number - Pixel width of point dot stroke
		pointDotStrokeWidth : 1,
		
		//Boolean - Whether to show a stroke for datasets
		datasetStroke : true,
		
		//Number - Pixel width of dataset stroke
		datasetStrokeWidth : 2,
		
		//Boolean - Whether to fill the dataset with a colour
		datasetFill : true,
		
		//Boolean - Whether to animate the chart
		animation : true,

		//Number - Number of animation steps
		animationSteps : 60,
		
		//String - Animation easing effect
		animationEasing : "easeOutQuart",

		//Function - Fires when the animation is complete
		onAnimationComplete : null
		
	}


	var myNewChart = new Chart(ctx).Line(data);

} else {
	$( "#_weight-chart" ).toggle();
}



