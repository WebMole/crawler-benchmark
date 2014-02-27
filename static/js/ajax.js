var infiniteScrollOn = false;
var infiniteScrollThreshold = 50;

function loadMoreContent()
{
	// We are not on the last page
	if (!$(".pagination :last-child").is('strong'))
	{
		var pageToLoad = $('.pagination a').last().attr('href');
		$('.pagination').html('<img style="display:block;margin:auto;" src="/static/img/loadingBar.gif">');

		$("<div>").load(pageToLoad, function() {
			$("#content ul.entries").append($(this).find("ul.entries").html());
			$('.pagination').html($(this).find(".pagination").html());
		});
	}
};

$(function() {
	$("#content").load($("#content").attr('firstUrl'));
	
    $(document).on('click', '.btnPaging' , function( event ) {
		event.preventDefault();
		$("#content").load($(this).attr('href'));
	});

	if ($('#infiniteScrollOn').val() === "on")
		infiniteScrollOn = true;

	$(window).scroll(function() {
		if (infiniteScrollOn)
		{
			if ($(window).scrollTop() + infiniteScrollThreshold >= $(document).height() - $(window).height()) {
				loadMoreContent();
			}
		}
	});
});