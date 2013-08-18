$('#project_form').submit(function(){
	var $ajaxData = $('#project_form').serializeArray();
	$ajaxData.push({name: 'slot_list', value: createSlotString()});
	$ajaxData.push({name: 'project_id', value: $('#project_form').data('id')});
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
		slot.id = $(this).data('id');
		slot.skills = [];
		
		$(this).find('.skillset_slot').each(function() {
			var skill = new Object();
			skill.id = $(this).data('skill_id');
			skill.slot = $(this).data('slot');
			slot.skills.push(skill);
		})
		
		slot.name = $(this).find('input').val();
		slot.desc = $(this).find('textarea').val();
		
		slots.push(slot);
	});	
	
	var jsonString = JSON.stringify(slots);	  
	return jsonString;
}


var $str = "<div class=\"slot\">";
$str += "<div class=\"slot_info\">"
$str += "<input></input><br />"
$str += "<textarea rows=\"\" cols=\"\"></textarea>"
$str += "</div>"
$str += "<div class=\"slot_skills\">"	
for (var i=0; i<5; i++) {
	$str += "<div class=\"skillset_slot\" data-skill_id=0 data-slot="+i+">"
	$str += "<img src=\"/static/img/open.png\" alt=\"open\">"
	$str += "Test</div>"
}
$str += "</div>"
$str += "</div>"

$('#add_slot').click(function() {
	console.log("test");
	$('#skill_slots').append($str);	
	makeDroppable();
});

function makeDroppable() {
    $('.skillset_slot').droppable( {
        accept: $( "img", $("#skills")),
        hoverClass: 'hovered',
        drop: project_assign_skill
    });
}

function project_assign_skill( event, ui ){
	var skill_id = ui.draggable.data( 'id' );
	console.log(skill_id);
    var $img = $(this).find('img');
    
    $(this).html(ui.draggable.data( 'name' ));
    $(this).append($img);
	
	console.log(ui.draggable.attr('src'));
	console.log($(this).find('img'));
	$(this).find('img').attr('src', ui.draggable.attr('src'));
	$(this).data('skill_id', skill_id);
}

$(function() {
	makeDroppable();
});