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


$('#project_form').submit(function(){
	var $ajaxData = $('#project_form').serializeArray();
	$ajaxData.push({name: 'slot_list', value: createSlotString()});
	console.log($ajaxData);
	
	$('#error').hide();
    $.ajax({
        type:"POST",
        url:"/projects/save/",
        data:$ajaxData,
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

function createSlotString() {
	  
	var slots = [];
	var $slots = $('.slot');
	$('.slot').each(function() {
		var slot = new Object();
		slot.skills = [];
		$(this).children().each(function() {
			var skill = new Object();
			skill.id = $(this).data('skill_id');
			skill.slot = $(this).data('slot');
			slot.skills.push(skill);
		})
		slots.push(slot);
	});	
	
	var jsonString = JSON.stringify(slots);	  
	return jsonString;
}

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
	skill.slot_nr = $(this).data( 'slot' );
	
	
	var jsonString = JSON.stringify(skill)
	$.ajax({
		type:"POST",
		url:"/profile/assign_skill/",
		data:jsonString,
		success: function(msg) {
			console.log(msg.color);
			$('#skillset_color').data('color', msg.color);
			updateColor();
		}
	});
	
    var $img = $(this).find('img');
    $(this).html(ui.draggable.data( 'name' ));
    $(this).append($img);
	
	console.log(ui.draggable.attr('src'));
	console.log($(this).find('img'));
	$(this).find('img').attr('src', ui.draggable.attr('src'));
	
}

function project_assign_skill( event, ui ){
	var skill_id = ui.draggable.data( 'id' );
    var $img = $(this).find('img');
    
    $(this).html(ui.draggable.data( 'name' ));
    $(this).append($img);
	
	console.log(ui.draggable.attr('src'));
	console.log($(this).find('img'));
	$(this).find('img').attr('src', ui.draggable.attr('src'));
	$(this).data('skill_id', skill_id);
}

$('#logout_button').click(function(){ 
	ajax_logout();
	return false;
});

function testDrop(){
	alert("Test");
}

function updateColor(){
	$('#skillset_color').css('background-color', $('#skillset_color').data('color'));
	
	$('.color_box').each(function() {
		$(this).css('background-color', $(this).data('color'));
		$(this).css('border-color', $(this).data('color'));
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
    $( "img", $("#skills") ).draggable({ revert: true, helper: "clone" });
    
    for ( var i=0; i<5; i++ ) {
        $('#skillset_skill'+i).droppable( {
            accept: $( "img", $("#skills")),
            hoverClass: 'hovered',
            drop: ajax_assign_skill
        });
    }
    updateColor();
});



var $str = "<div class=\"slot\">";
for (var i=0; i<5; i++) {
	$str += "<div class=\"skillset_slot\" data-skill_id=0 data-slot="+i+">"
	$str += "<img src=\"/static/img/open.png\" alt=\"open\">"
	$str += "Test</div>"
}
$str += "</div>"



$('#add_slot').click(function() {
	console.log("test");
	$('#skill_slots').append($str);	
	
    $('.skillset_slot').droppable( {
        accept: $( "img", $("#skills")),
        hoverClass: 'hovered',
        drop: project_assign_skill
    });
});
