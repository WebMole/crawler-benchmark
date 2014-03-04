$(function() {
    $('.btnAddAuto').click(function() {
    	$.ajax({
          type: "POST",
          url: $(this).attr('url') + '/' + $('#num' + $(this).attr('route')).val(),
          success: function() {
          	alert('Success');
          },
          error: function() {
          	alert('Error')
          }
        });
    });

    $('.btnClearEntries').click(function() {
      $.ajax({
          type: "DELETE",
          url: $(this).attr('url'),
          success: function() {
            alert('Success');
          },
          error: function() {
            alert('Error')
          }
        });
    });

    $('#clearLogUserAgents').click(function( event ) {
		event.preventDefault();

		if (confirm("Do you really want to clear the log for these user agents?")) {
	    	var userAgents = $('#selUserAgent').val();
	    	var clearUserAgentsUrl = $(this).attr('url');

			if (userAgents != null) {
		    	var userAgentsString = '';
		    	for (var i = userAgents.length - 1; i >= 0; i--) {
		    		userAgentsString = 'selUserAgent=' + encodeURIComponent(userAgents[i]) + '&' + userAgentsString;
		    	};
		    	userAgentsString = userAgentsString.substring(0, userAgentsString.length - 1);
		    	clearUserAgentsUrl = clearUserAgentsUrl + '?' + userAgentsString;

		    	$.ajax({
		          type: "DELETE",
		          url: clearUserAgentsUrl,
		          success: function() {
		            alert('Success');
		          },
		          error: function() {
		            alert('Error')
		          }
		        });
		    }
		}
    });

    $('#frmUserAgent').submit(function( event ) {
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
	    	};
	    	userAgentsString = userAgentsString.substring(0, userAgentsString.length - 1);
	    	imgUrl = imgUrl + '?' + userAgentsString;
	    }

    	$('#imgResult').attr('src', imgUrl);
	});
});