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
	$('#error').hide();
	console.log("test");
    $.ajax({
        type:"POST",
        url:"/login/ajax_login/",
        data:$('#login_form').serialize(),
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
});

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
});