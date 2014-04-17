function toggle_note(note_header) {
	//$(note_header).css( "background-color", "red" )

	$(note_header).addClass(" hover ");
}

//$( "tr.note_header").hover(toggle_note(this), toggle_note(this));

$( "tbody.note_body").hover(
	function() {
		$(this).children("tr.note_text").toggle();
	}, function() {
		$(this).children("tr.note_text").toggle();
	}
);

// $(this). toggle_note(this));