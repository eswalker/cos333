
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
	
	$(this).toggle();

	$('#content').append('<br><div class="_row"><p>Row ' + num_rows + '</p><ul id="sortable2" class="connectedSortable _ergs"></ul></div><br><button class="btn btn-primary _add_row">Add Row</button>');
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

 	$('._add_row').click(add_row);

}


$('._add_row').click(add_row);
