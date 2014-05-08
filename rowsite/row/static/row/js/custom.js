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

function secondsToWatts(pace) {
	return 2.80 / (Math.pow(pace, 3));
}

var _distances = []
var _times = []

$( '._time').each(function() { 
	var org = $(this).text();
	$(this).text(org.substring(0, org.length-3) + '.' + org.substring(org.length-3, org.length-2) );
});

$( '._time').each(function( index ) {
	_times.push($(this).text());
});
$( '._distance').each(function( index ) {
	_distances.push($(this).text());
});

var _x = 0
var _y = 0
$( '._pace').each(function( index ) {
	var pace =  _times[_x] / _distances[_x] * 500;
	$(this).text(readableSeconds(pace));
	_x = _x + 1;
});

$( '._watts').each(function( index ) {
	var pace = (_times[_y] / _distances[_y]);
	$(this).text(secondsToWatts(pace).toFixed(1));
	_y = _y + 1;
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

$( '#id_time').each(function( index ) {
	val = $(this).val()
	if (val) {
		$(this).val(readableSeconds($(this).val() / 1000))
	}
})




	