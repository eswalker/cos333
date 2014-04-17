$( "tr.note_head").click(
	function() {
		$(this).next().toggle();
	}
);