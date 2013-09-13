var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('#login_form').submit(function(){
	$('#login_error').hide();
    $.ajax({
        type:"POST",
        url:"/login/ajax_login/",
        data:$('#login_form').serialize(),
        success: function(msg){
			if (msg.error) {
				$('#login_error').text(msg.error);
				$('#login_error').show();
			}
            if (msg.return === 'true') {
				window.location.reload();
			}
        }
    });
	return false;
});

function ajax_logout(){
    $.ajax({
        type:"POST",
        url:"/login/ajax_logout/",
        success: function(msg){
            console.log(msg.return);
			window.location.reload();
        }
    }); 
}

$('#logout_button').click(function(){ 
	ajax_logout();
	return false;
})

function updateColor(){
	$('.color_box').each(function() {
		$(this).css('background-color', $(this).data('color'));
		//$(this).css('border-color', $(this).data('color'));
	});
}


$(function() {
    var button = $('#login_button');
    var box = $('#login_box');
    var form = $('#login_form');
    button.removeAttr('href');
    button.mouseup(function(login) {
        box.toggle();
        button.toggleClass('active');
    });
    form.mouseup(function() { 
        return false;
    });
    $(this).mouseup(function(login) {
        if(!($(login.target).parent('#login_button').length > 0)) {
            button.removeClass('active');
            box.hide();
        }
    });
    $( ".drag", $( ".skill", $("#slider") ) ).draggable({ revert: true, helper: "clone" });
    updateColor();
    
	$('.skills_toggle').click(function() {
	  $( "#slider" ).toggle( "slide", { direction: "right" } );
	});
});


