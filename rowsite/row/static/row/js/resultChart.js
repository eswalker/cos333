var _paces = [];
var _athletes = [];

$( "#_toggle-result-table" ).click(function() {
    $( "#_result-table" ).toggle();
});

$( '._pace').each(function( index ) {
	_paces.push(toSeconds($(this).text()));
});
$( '._athlete').each(function( index ) {
	_athletes.push($(this).text());
});

var piece_name = $( '#piece_name' ).text()

var _results = {};
var _keys = [];

/* go through each piece of a data and create an array of keys
and an associative array of paces and athletes */
for (var i = 0; i < _paces.length; i++) {
	if (!(_paces[i] in _results)) {
		_results[_paces[i]] = [];
		_keys.push(_paces[i]);
	}

	_results[_paces[i]].push(_athletes[i]);
}

/* sort the paces */
_keys.sort(function(a,b){return a-b});

/* prepare the arrays for categories and data */
var _categories = [];
var _data = [];
for (var i = 0; i < _keys.length; i++) {
	_categories.push(readableSeconds(_keys[i])); // paces as keys
	_data.push(_results[_keys[i]].length); // frequency as values
}


var _athlete_lists = [];
for (var i = 0; i < _keys.length; i++) {
    var list = "";
    for (var j = 0; j < _results[_keys[i]].length; j++) {
        list += (_results[_keys[i]][j] + "<br>");
    }
    _athlete_lists[_keys.indexOf(_keys[i])] = list;
}
    
if (_paces.length > 1) {

    $(function () {
            $('#_result-chart').highcharts({
                chart: {
                    type: 'column'
                },
                title: {
                    text: piece_name
                },
                xAxis: {
                    categories: _categories,
                    title: {
                    	text: 'Split (Time Per 500m)'
                    }
                },
                yAxis: {
                    allowDecimals: false,
                    min: 0,
                    title: {
                        text: 'Number of Rowers'
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>'+this.x+'</b><br/>'+ _athlete_lists[_categories.indexOf(this.x)];
                    }
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0
                    }
                },
                series: [{
                    name: 'Results',
                    data: _data
                }]
            });
        });

} else {
    $( "#_result-chart" ).toggle();
    $( "#_result-table" ).toggle();
    $( "#_toggle-result-table" ).toggle();
}
    
