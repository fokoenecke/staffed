
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