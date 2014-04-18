
$(function() {
	$( "#ergs" ).sortable({
		revert: true
	});
	$( "#open_erg" ).draggable({
		connectToSortable:"#ergs",
		helper: "clone",
		revert: "invalid"
	});


$( "#open_erg, ._erg, ._ergs" ).disableSelection();

$( "#sortable" ).sortable({
      revert: true
    });
    $( "#draggable" ).draggable({
      connectToSortable: "#sortable",
      helper: "clone",
      revert: "invalid"
    });
    $( "ul, span, ._ergs, ._row, ._erg, div" ).disableSelection();

});

$( ".connectedSortable" ).sortable({
    connectWith: ".connectedSortable"
}).disableSelection();


num_rows = 3;
function add_row(){
	$('#content').append('<br><div class="_row"><p>Row ' + num_rows + '</p><ul id="" class="connectedSortable _ergs"></ul></div>');
	num_rows += 1;
	$( "#sortable" ).sortable({
      revert: true
    });
    $( "#draggable" ).draggable({
      connectToSortable: "#sortable",
      helper: "clone",
      revert: "invalid"
    });
    $( "ul, span, ._ergs, ._row, ._erg, div" ).disableSelection();

 	$( ".connectedSortable" ).sortable({
      connectWith: ".connectedSortable"
    }).disableSelection();

}
$('._add_row').click(add_row);


function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}

$('._submit').click(function() {

	valid = true;

	athletes = [];
	times = [];
	distances = [];

	distance = parseInt($("#distance").val());
	if (!distance) {
		valid =false;
		$("#distance").parent().removeClass("_erg_valid");
		$("#distance").parent().addClass("_erg_error");
	} else {
		$("#distance").parent().addClass("_erg_valid");
		$("#distance").parent().removeClass("_erg_error");
	}

	$('._erg').each(function() {
		if (!$(this).parent().hasClass("_athlete_bin")) {
			athleteId = parseInt($(this).children().eq(1).text());
			min = parseInt($(this).children().eq(3).children().eq(0).val());
			sec = parseFloat($(this).children().eq(5).children().eq(0).val());
			
			if (!min || !athleteId || !sec) {
				$(this).removeClass("_erg_valid");
				$(this).addClass("_erg_error");
				valid = false;
			} else {
				$(this).removeClass("_erg_error");
				$(this).addClass("_erg_valid");
				athletes.push(athleteId);
				times.push(min * 60 + sec);
				distances.push(distance);
			}

		}
	});
	if (valid) {
		console.log(athletes);
		console.log(times);
		console.log(distances);
		s = ""
		for (i = 0; i < athletes.length; i++) {
			s += athletes[i] + "," + times[i] + "," + distances[i] + "," ;
		}
		if (s.length > 1)
			s = s.substr(0,s.length - 1);
		console.log({results:s});
		$.post( "", {results : s}, function( data ) {
			$('._erg').each(function() {
				$(this).children().eq(3).children().eq(0).val("");
				$(this).children().eq(5).children().eq(0).val("");
			});

			var next = getUrlParameter("next");
			if (next != null) {
				window.location.href = next;
			}
  				
		});
			
	}
});




$('._clear').click(function() {
    location.reload();
});

