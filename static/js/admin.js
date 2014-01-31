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
});