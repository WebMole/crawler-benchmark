var infiniteScrollOn = false;
var infiniteScrollThreshold = 50;
var nextUrl = null;

function loadMoreContent(pageToLoad) {
    if (pageToLoad != null) {
        $('.pagination').html('<img style="display:block;margin:auto;" src="/static/img/loadingBar.gif">');

        $("<div>").load(pageToLoad, function () {
            $('.pagination').empty(); // Remove loadingBar
            $("#content ul.entries").append($(this).find("ul.entries").html());
            nextUrl = findNextPage($(this).find(".pagination"));
        });
    }
}

function findNextPage(divPagination) {
    var pageToLoad = null;
    // We are not on the last page
    if (!$(divPagination).find(":last-child").is('strong')) {
        pageToLoad = $(divPagination).find('a').last().attr('href');
    }
    return pageToLoad;
}

$(function () {
    if ($('#infiniteScrollOn').val() === "on") {
        infiniteScrollOn = true;
    }

    $("<div>").load($("#content").data('firstUrl'), function () {
        if (infiniteScrollOn) {
            $("#content").html($(this).find("ul.entries")).append('<div class="pagination"></div>');
            nextUrl = findNextPage($(this).find(".pagination"));
        }
        else {
            $("#content").html($(this).html());
        }
    });

    $(document).on('click', '.btnPaging', function (event) {
        event.preventDefault();
        if (!infiniteScrollOn) {
            $("#content").load($(this).attr('href'));
        }
    });

    $(window).scroll(function () {
        if (infiniteScrollOn) {
            if ($(window).scrollTop() + infiniteScrollThreshold >= $(document).height() - $(window).height()) {
                loadMoreContent(nextUrl);
            }
        }
    });
});