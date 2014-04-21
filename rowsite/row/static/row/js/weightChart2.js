var _weights = []
var _datetimes = []

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
    var weight_charts = [];
    var old = _datetimes[0];
    var sum = _weights[0];
    var n = 1;
    for (var i = 1; i < _datetimes.length; i++) {
        if (old != _datetimes[i]) {
            avg_weight = (1.0 * sum) / n;
            new_dates.push(old);
            new_weights.push(avg_weight);
            weight_charts.push([old, avg_weight]);
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

    $(function () {
            $('#_weights-chart').highcharts({
                chart: {
                    type: 'spline'
                },
                title: {
                    text: 'Athlete weight'
                },
                xAxis: {
                    type: 'datetime',
                    dateTimeLabelFormats: { // don't display the dummy year
                        month: '%e. %b',
                        year: '%b'
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
                            Highcharts.dateFormat('%e. %b', this.x) +': '+ this.y +' m';
                    }
                },
                
                series: [{
                    name: 'Athlete weight',
                    data: weight_charts
                }]
            });
        });
}
    