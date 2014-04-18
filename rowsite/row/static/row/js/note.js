$( "tr.note_head").click(
	function() {
		$(this).next().toggle();
		var symbol = $(this).find("b.note_subject_symbol");
		if ($(symbol).text() == '+') {
			$(symbol).text('—');
		} else {
			$(symbol).text('+');
		}

	}
);