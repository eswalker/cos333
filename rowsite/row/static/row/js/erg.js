
$(function() {
	$( "#sortable" ).sortable({
		revert: true
	});
	$( "#draggable" ).draggable({
		connectToSortable: "#sortable",
		revert: "valid"
	});
	$( "ul, li" ).disableSelection();
});