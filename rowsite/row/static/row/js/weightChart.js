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

var name = $( '#athlete_name' ).text()

var weight_data = [];
var old = _datetimes[0];
var sum = _weights[0];
var n = 1;
for (var i = 1; i < _datetimes.length; i++) {
    if (old != _datetimes[i]) {
        avg_weight = (1.0 * sum) / n;
        weight_data.push([old, avg_weight]);
        sum = _weights[i];
        n = 1;
    } else {
        n += 1; sum += _weights[i];
    }
    old = _datetimes[i];        
}

weight_data.push([old, (1.0 * sum) / n]);

if (weight_data.length > 1) {

    $(function () {
            $('#_weight-chart').highcharts({
                chart: {
                    type: 'spline'
                },
                title: {
                    text: name
                },
                xAxis: {
                    type: 'datetime',
                    dateTimeLabelFormats: { // don't display the dummy year
                        day: '%b %e',
                        week: '%b %e',
                        month: '%b %e',
                        month: '%b %Y',
                        year: '%Y',
                    }
                },
                yAxis: {
                    title: {
                        text: 'Weight (lbs)'
                    },
                },
                tooltip: {
                    formatter: function() {
                            return '<b>'+ this.series.name +'</b><br/>'+
                            Highcharts.dateFormat('%b %e, %Y', this.x) +': '+ this.y +' lbs';
                    }
                },
                
                series: [{
                    name: name,
                    data: weight_data
                }]
            });
        });
} else {
    $( "#_weight-chart" ).toggle();
    $( "#_weight-table" ).toggle();
    $( "#_toggle-weight-table" ).toggle();
}
    