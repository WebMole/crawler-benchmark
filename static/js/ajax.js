$(function() {
	$("#content").load($("#content").attr('firstUrl'));
	
    $(document).on('click', '.btnPaging' , function( event ) {
		event.preventDefault();
		$("#content").load($(this).attr('href'));
	});
});