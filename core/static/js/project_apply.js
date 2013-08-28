$('.apply').click(function() {
	console.log("apply");
	
	var slot_id = $(this).parent().data('id');
	console.log(slot_id);
	var jsonString = JSON.stringify(slot_id)
	
    $.ajax({
        type:"POST",
        url:"/projects/slots/apply/",
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
