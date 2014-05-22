$(function () {
    if ($('#successes_table').length > 0) {
        new Tablesort(document.getElementById('successes_table'));
    }

    $('#clearLogUserAgents').click(function (event) {
        event.preventDefault();

        if (confirm("Do you really want to clear the log for these user agents?")) {
            var userAgents = $('#selUserAgent').val();
            var clearUserAgentsUrl = $(this).data('url');

            if (userAgents != null) {
                var userAgentsString = '';
                for (var i = userAgents.length - 1; i >= 0; i--) {
                    userAgentsString = 'selUserAgent=' + encodeURIComponent(userAgents[i]) + '&' + userAgentsString;
                }
                userAgentsString = userAgentsString.substring(0, userAgentsString.length - 1);
                clearUserAgentsUrl = clearUserAgentsUrl + '?' + userAgentsString;

                $.ajax({
                    type: "DELETE",
                    url: clearUserAgentsUrl,
                    success: function () {
                        //alert('Success');
                        loadUserAgents();
                    },
                    error: function () {
                        alert('Error')
                    }
                });
            }
        }
    });

    $('#frmUserAgent').submit(function (event) {
        event.preventDefault();
        //$.('#imgResult').attr('src', $("#frmUserAgent") + $.param($('#selUserAgent').val()));
        /*$.ajax({
         url: $("#frmUserAgent").attr('action'),
         data: $('#selUserAgent').val();,
         success: function() {

         },
         });*/
        var userAgents = $('#selUserAgent').val();
        var imgUrl = $("#frmUserAgent").attr('action');
        if (userAgents != null) {
            var userAgentsString = '';
            for (var i = userAgents.length - 1; i >= 0; i--) {
                userAgentsString = 'selUserAgent=' + encodeURIComponent(userAgents[i]) + '&' + userAgentsString;
            }
            userAgentsString = userAgentsString.substring(0, userAgentsString.length - 1);
            imgUrl = imgUrl + '?' + userAgentsString;
        }

        $('#imgResult').attr('src', imgUrl);
    });

    $(document).on('submit', '#frm_add_entry', function (event) {
        event.preventDefault();

        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function () {
                //alert('Success');
                loadMode();
            },
            error: function () {
                alert('Error')
            }
        });
        //event.preventDefault();
        //console.log($(this).serialize());
    });

    $(document).on('click', '.btnAddAuto', function () {
        $.ajax({
            type: "POST",
            url: $(this).attr('url') + '/' + $('#num' + $(this).attr('route')).val(),
            success: function () {
                //alert('Success');
                loadMode();
            },
            error: function () {
                alert('Error')
            }
        });
    });

    $(document).on('click', '.btnClearEntries', function () {
        if (confirm("Do you really want to clear all the entries for this mode?")) {
            $.ajax({
                type: "DELETE",
                url: $(this).data('url'),
                success: function () {
                    //alert('Success');
                    loadMode();
                },
                error: function () {
                    alert('Error')
                }
            });
        }
    });

    loadMode();

    $('#sel_modes').change(function () {
        loadMode(this.value);
    });
});

function loadUserAgents() {
    url = $('#selUserAgent').data('url');

    $.getJSON(url, function (data) {
        $('#selUserAgent').find('option').remove();

        var strToAppend = "";

        $.each(data, function (key, value) {

            var option = $('<option/>');
            option.attr({ 'value': value }).text(value);

            $('#selUserAgent').append(option);
        });
    });
}

function loadMode(url) {
    if (url === undefined)
        url = $('#sel_modes').val();
    $('#div_mode').html('<img style="display:block;margin:auto;" src="/static/img/loadingBar.gif">');
    $('#div_mode').load(url);
}