function toggle_note(note_header) {
	//$(note_header).css( "background-color", "red" )

	$(note_header).addClass(" hover ");
}

//$( "tr.note_header").hover(toggle_note(this), toggle_note(this));

$( "tr.note_header").hover(
	function() {
		$(this).next().toggle();
	}, function() {
		$(this).next().toggle();
	}
);

// $(this). toggle_note(this));