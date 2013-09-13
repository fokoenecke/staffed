
function get_filter_color($filter_div){
	
	var skillset = new Object;
	
	skillset.skills = []
	$filter_div.children('.skillset_slot').each(function() {
		var skill = new Object;
		skill.id = $(this).data('skill_id');
		skillset.skills.push(skill);
	});
	
	
	var color = '';
	var jsonString = JSON.stringify(skillset)
	console.log(jsonString);
	$.ajax({
		type:"POST",
		url:"/ajax/get_color/",
		data:jsonString,
		success: function(msg) {
			$('#skillset_color').data('color', msg.color);			
			
			var ajax_info = new Object;
			ajax_info.color = $('#skillset_color').data('color');
			var jsonString = JSON.stringify(ajax_info)
			
		    $.ajax({
		        type:"POST",
		        url:"/projects/slots/",
				data:jsonString,
		        success: function(msg){
		        	$('#slot_list ul').replaceWith(msg);
					updateColor();
		        }
		    });
		}
	});
	
}

function makeDroppable() {
    $('.skillset_slot img').droppable( {
        accept: $( ".drag", $( ".skill", $("#slider") ) ),
        hoverClass: 'hovered',
        drop: project_assign_skill
    });
}

function project_assign_skill( event, ui ){
	var skill_id = ui.draggable.data( 'id' );
    var $img = $(this);
    
    $slot = $(this).parent();
	
    $slot.data('skill_id', skill_id);    
	var img_src = ui.draggable.find('img').attr('src');
	var path = img_src.substring(0, img_src.lastIndexOf("/"));
	var file = img_src.substring(img_src.lastIndexOf("/"));
	$(this).attr('src', path + "/64" + file);
	
	var color = get_filter_color($('.slot_skills'));
}

$(function() {
	makeDroppable();
});

$('#profile_finder').click(function() {
    $.ajax({
        type:"POST",
        url:"/profile_skills/",
        success: function(msg){
			if (msg.error) {
				$('#error').text(msg.error);
				$('#error').show();
			}
            if (msg.return === 'true') {
            	var idx = 0;
            	msg.skills.map( function(skill)  {
            		var $skill_slot = $(".skillset_slot[data-slot='" + idx + "']");            		
            	    var $img = $skill_slot.find('img');
            	    
            	    $skill_slot.data('skill_id', skill['id']);
            	    
            	    $img.attr('src', "../../static/img/skills/64/" + skill['img']);
            	    $skill_slot.append($img);
            	    
            	    idx++;
            		
            	});
            	var color = get_filter_color($('.slot_skills'));
			}
        }
    });
});
