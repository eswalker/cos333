



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
	$('#content').append('<br><div class="_row"><p>Row ' + num_rows + '</p><ul id="sortable' + num_rows + '" class="connectedSortable _ergs"></ul></div>');
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



// w3schools
function setCookie(cname,cvalue,exdays){
	var d = new Date();d.setTime(d.getTime()+(exdays*24*60*60*1000));
	var expires = "expires="+d.toGMTString();
	document.cookie = cname + "=" + cvalue + "; " + expires;
}

// w3schools 
function getCookie(cname){
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++) { var c = ca[i].trim(); if (c.indexOf(name)==0) return c.substring(name.length,c.length); }
  	return "";
}

function storeErgPositions() {
	var cookie = "" + num_rows + ",";
	$('._erg').each(function() {
		athleteId = parseInt($(this).children().eq(1).text());
		cookie += $(this).parent().attr('id') + ":" + athleteId + ",";
	});
	setCookie("ergPositions", cookie, 365);
	console.log(getCookie("ergPositions"));
}

function restoreErgPositions() {
	var cookie = getCookie("ergPositions");
	console.log("COOKIE: " + cookie);
	data = cookie.split(',');
	
	var rows = 3; if (data.length > 1) { rows = parseInt(data[0]); }
	while(num_rows < rows) { add_row() }

	for (i = 1; i < data.length; i++) {
		data2 = data[i].split(':');
		if (data2.length == 2) {
			divId = data2[0];
			athId = data2[1];
		
			$('._erg').each(function() {
				athleteId = $(this).children().eq(1).text();
				if (athleteId == athId) {
					$(this).detach();
					$("#" + divId).append($(this));
				}
			});
		}
	}

}

restoreErgPositions();


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

	distanceString = $("#distance").val();
	distance = parseInt(distanceString);
	if (!distance) {
		valid =false;
		$("#distance").parent().removeClass("_erg_valid");
		$("#distance").parent().addClass("_erg_error");
	} else {
		$("#distance").parent().addClass("_erg_valid");
		$("#distance").parent().removeClass("_erg_error");
	}


	storeErgPositions();

	$('._erg').each(function() {
		if (!$(this).parent().hasClass("_athlete_bin")) {
			athleteId = parseInt($(this).children().eq(1).text());
			min = parseInt($(this).children().eq(3).children().eq(0).val());
			sec = parseFloat($(this).children().eq(5).children().eq(0).val());
			
			if (!athleteId || !(min || sec)) {
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

		distanceString += " meters";
		var posted_data = { results : s , name : distanceString};

		console.log(posted_data);
		$.post( "", posted_data , function( data ) {
			$('._erg').each(function() {
				$(this).children().eq(3).children().eq(0).val("");
				$(this).children().eq(5).children().eq(0).val("");
			});

			alert("Successfully add new piece: " + distanceString + "\n" + "Successfully added " + athletes.length + " erg results");
			/*var next = getUrlParameter("next");
			if (next != null) {
				window.location.href = next;
			}*/
  				
		});	
	}
});






$('._clear').click(function() {
	setCookie("ergPositions", "", 365);
    location.reload();
});

