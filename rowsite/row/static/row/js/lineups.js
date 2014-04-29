
$( "#open_erg, .boat, ._ergs" ).disableSelection();

$( "ul, span, ._ergs, ._row, .boat, div" ).disableSelection();
$( ".connectedSortable" ).sortable({
    connectWith: ".connectedSortable"
}).disableSelection();



$('.boat').click(function(){ $(this).children().eq(3).toggle(); });

function resetError() { $('#error').text("").hide(); }
function resetSuccess() { $('#success').hide();}

$('._clear').click(function() {
	resetSuccess();
		resetError();
	$('._athlete').each(function() {
		$(this).detach();
		$("#sortable0").append($(this));
	});

	setCookie("lineup","",365);

	$('.boat').each(function() {		
		$(this).removeClass('_erg_valid');
		$(this).removeClass('_erg_error');

	});

});





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

function storeLineups() {
	var cookie = "";
	$('._athlete').each(function() {
		if($(this).parent().hasClass("hull")) {
			boatId = $(this).parent().parent().children().eq(4).text();
			athleteId = $(this).children().eq(1).text();
			cookie += boatId + ":" + athleteId + ",";
		}
	});
	setCookie("lineup", cookie, 365);
	console.log(getCookie("lineup"));
}

function restoreErgPositions() {
	var cookie = getCookie("lineup");
	console.log("COOKIE: " + cookie);
	data = cookie.split(',');
	

	for (i = 0; i < data.length - 1; i++) {

		data2 = data[i].split(':');

		if (data2.length == 2) {
			boatId = data2[0];
			athleteId = data2[1];
		
			$('._athlete').each(function() {
				athlete = $(this);
				aId = $(this).children().eq(1).text();
				$('.boat').each(function() {
					bId = $(this).children().eq(4).text();
					if (bId == boatId && aId == athleteId) {
						athlete.detach();
						$(this).children().eq(3).append(athlete);
					}	

				});
			});
		}
	}
}

restoreErgPositions();



$('._submit').click(function(){

	storeLineups();

	var resultString = "";
	var allBoatsValid = true;

	$('#error').text('').hide();
	$('#success').hide();

	$('.boat').each(function() {
		boatId = parseInt($(this).children().eq(4).text());
		boatSeats = parseInt($(this).children().eq(5).text());
		boatCoxed = ($(this).children().eq(6).text() == "True");
		boatName = $(this).children(".boatname").text();

		console.log(boatName);

		numChildren = $(this).children().eq(3).children().length;
		expSeats = boatSeats;
		if (boatCoxed)
			expSeats += 1;

		var numPorts = 0; var numStarboards = 0; var numBoth = 0; var numCoxswains = 0;
		$(this).children('.hull').children('._athlete').each(function(){
			var side = $(this).children().eq(3).text();
			var role = $(this).children().eq(2).text();
			if (role == "Rower") {
				if (side == "Port")
					numPorts += 1;
				else if (side == "Starboard")
					numStarboards += 1;
				else if (side == "Both")
					numBoth += 1;
			} else if (role = "Coxswain")
				numCoxswains += 1;
		});

		var correctNumRowers = false;
		var correctNumPorts = false;
		var correctNumStarboards = false;
		var coxswainCorrectPosition = false;
		var validBoatId = false;

		if (boatId)
			validBoatId = true;
		if (numChildren == expSeats)
			correctNumRowers = true;
		if (!boatCoxed ||  $(this).children().eq(3).children().eq(0).children().eq(2).text() == 'Coxswain') 
			coxswainCorrectPosition = true;
		if (numPorts + numBoth >= Math.floor(expSeats/2))
			correctNumPorts = true;
		if (numStarboards + numBoth >= Math.floor(expSeats/2))
			correctNumStarboards = true;

		if (numChildren == 0) { $(this).removeClass('_erg_valid').removeClass('_erg_error'); }
		else {
		
			
			if (!validBoatId) $('#error').append('Invalid boat id for ' + boatName + ".<br>").show();
			if (!correctNumRowers) $('#error').append('Incorrect number of rowers in ' + boatName + ".<br>").show();
			else {
				if (!coxswainCorrectPosition) $('#error').append('Invalid coxswain position for ' + boatName + ".<br>").show();
				if (!correctNumPorts) $('#error').append('Too few ports in ' + boatName + ".<br>").show();
				if (!correctNumStarboards) $('#error').append('Too few starboards in ' + boatName + ".<br>").show();
			}

			if (!(validBoatId && coxswainCorrectPosition && correctNumRowers && correctNumStarboards && correctNumPorts)) {
				allBoatsValid = false;
				$(this).removeClass('_erg_valid').addClass('_erg_error');	
			} else {
				$(this).removeClass('_erg_error').addClass('_erg_valid');
				resultString += boatId + ",";
				$(this).children().eq(3).children().each(function(){
					resultString += $(this).children().eq(1).text() + ",";
				});
				resultString += ";";	
			}

		
		}

	});

	if (allBoatsValid) {

		var posted_data = { results : resultString };

		console.log(posted_data);
		$.post( "", posted_data , function( data ) {
			$('#success').show();
		});	
	}
	console.log(resultString);

});

$('._done').click(function(){ storeLineups(); });

	
