
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
		        	$('#slots').replaceWith(msg);
					updateColor();
		        }
		    });
		}
	});
	
}

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
	
	var color = get_filter_color($('.slot_skills'));
	console.log(color);
}

$(function() {
	makeDroppable();
});

$('#profile_finder').click(function() {
	console.log("find for skills");
	
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
            		console.log(skill['id']);
            		var $skill_slot = $(".skillset_slot[data-slot='" + idx + "']");            		
            	    var $img = $skill_slot.find('img');
            	    
            	    console.log($skill_slot);
            	    console.log($img);
            	    $skill_slot.html(skill['name']);
            	    $skill_slot.data('skill_id', skill['id']);
            	    
            	    $img.attr('src', "../../static/img/" + skill['img']);
            	    $skill_slot.append($img);
            	    
            	    idx++;
            		
            	});
            	var color = get_filter_color($('.slot_skills'));
			}
        }
    });
});
