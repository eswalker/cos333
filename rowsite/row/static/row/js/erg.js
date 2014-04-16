
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
    $( "ul, span" ).disableSelection();

});




    $( "#sortable0, #sortable1, #sortable2" ).sortable({
      connectWith: ".connectedSortable"
    }).disableSelection();
