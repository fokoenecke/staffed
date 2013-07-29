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

$('#profile_form').submit(function(){
	console.log("test");
	$('#error').hide();
    $.ajax({
        type:"POST",
        url:"/save_profile/",
        data:$('#profile_form').serialize(),
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

function ajax_assign_skill( event, ui ){
	var skill = new Object;
	skill.id = ui.draggable.data( 'id' );
	skill.slot_nr = $(this).data( 'number' );
	
	var jsonString = JSON.stringify(skill)
	$.ajax({
		type:"POST",
		url:"/profile/assign_skill/",
		data:jsonString
	});
}

$('#logout_button').click(function(){ 
	ajax_logout();
	return false;
});

function testDrop(){
	alert("Test");
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
    $( "img", $("#skills") ).draggable({ revert: true, helper: "clone" });
    
    var words = ['0', '1', '2', '3', '4'];
    for ( var i=0; i<5; i++ ) {
        $('#skillset_skill'+words[i]).droppable( {
            accept: $( "img", $({% for i in 3|get_range %"#skills")),
            hoverClass: 'hovered',
            drop: ajax_assign_skill
        });
    }    
});