
$( "#open_erg, .boat, ._ergs" ).disableSelection();

$( "ul, span, ._ergs, ._row, .boat, div" ).disableSelection();
$( ".connectedSortable" ).sortable({
    connectWith: ".connectedSortable"
}).disableSelection();



$('.boat').click(function(){ $(this).children().eq(3).toggle(); });
$('._clear').click(function() {
	
	$('._athlete').each(function() {
		$(this).detach();
		$("#sortable0").append($(this));
	});

	setCookie("lineup","",365);

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

	$('.boat').each(function() {
		boatId = parseInt($(this).children().eq(4).text());
		boatSeats = parseInt($(this).children().eq(5).text());
		boatCoxed = ($(this).children().eq(6).text() == "True");

		numChildren = $(this).children().eq(3).children().length;
		expSeats = boatSeats;
		if (boatCoxed)
			expSeats += 1;

		

		if (boatId && numChildren == expSeats && (!boatCoxed || $(this).children().eq(3).children().eq(0).children().eq(2).text() == 'Coxswain')) {
			$(this).removeClass('_erg_error');
			$(this).addClass('_erg_valid');	

			resultString += boatId + ",";
			$(this).children().eq(3).children().each(function(){
				resultString += $(this).children().eq(1).text() + ",";
			});
			resultString += ";";		
		} else if (numChildren != 0) {
			$(this).removeClass('_erg_valid');
			$(this).addClass('_erg_error');
		} else {
			$(this).removeClass('_erg_valid');
			$(this).removeClass('_erg_error');
		}

	});
	console.log(resultString);

});

$('._done').click(function(){ storeLineups(); });

	
