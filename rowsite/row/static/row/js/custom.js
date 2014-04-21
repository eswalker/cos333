
function readableSeconds(secs) {
	var mins = Math.floor(secs / 60);
	secs = secs - mins * 60;
	secs = Math.round(secs * 10) / 10;
	var strSec = secs;
	if (secs < 10)
		var strSec = "0" + secs;
	return (mins + ":" + strSec);
}

function toSeconds(pace) {
	var fields = pace.split(":");
	var min = parseInt(fields[0]);
	var secs = parseFloat(fields[1]);
	return parseInt(min * 60 + secs);
}


var _distances = []
var _times = []

$( '._time').each(function( index ) {
	_times.push($(this).text());
});
$( '._distance').each(function( index ) {
	_distances.push($(this).text());
});

var _x = 0
$( '._pace').each(function( index ) {
	var pace =  _times[_x] / _distances[_x] * 500;
	$(this).text(readableSeconds(pace));
	_x = _x + 1;
});


$( '._time').each(function( index ) {
	$(this).text(readableSeconds($(this).text()));
});


$( '._height').each(function( index ) {
	var inches = $(this).text();
	var feet = Math.floor(inches / 12);
	inches = inches - feet * 12;
	$(this).text(feet + "'" + inches + '"');
});

i = 1;
$( '._order').each(function( index ) { $(this).text("" + i++)});




	