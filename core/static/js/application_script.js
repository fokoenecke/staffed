$('.appl_approve').click(function() {
	console.log("approve");
	
	var application_id = $(this).parent().parent().data('id');
	console.log(application_id);
	var jsonString = JSON.stringify(application_id)
	
    $.ajax({
        type:"POST",
        url:"/projects/applications/accept/",
        data:jsonString,
        success: function(msg){
			if (msg.error) {
				$('#error').text(msg.error);
				$('#error').show();
			}
            if (msg.return === 'true') {
				window.location.reload();
			}
        }
    });
});

$('.appl_decline').click(function() {
	console.log("decline");
	
	var application_id = $(this).parent().parent().data('id');
	console.log(application_id);
	var jsonString = JSON.stringify(application_id)
	
    $.ajax({
        type:"POST",
        url:"/projects/applications/decline/",
        data:jsonString,
        success: function(msg){
			if (msg.error) {
				$('#error').text(msg.error);
				$('#error').show();
			}
            if (msg.return === 'true') {
				window.location.reload();
			}
        }
    });
});

