function ajax_assign_skill( event, ui ){
	var skill = new Object;
	$slot = $(this).parent();

	skill.id = ui.draggable.data( 'id' );
	skill.slot_nr = $slot.data('slot');
	
	var jsonString = JSON.stringify(skill);
	console.log(jsonString);
	
	$.ajax({
		type:"POST",
		url:"/profile/assign_skill/",
		data:jsonString,
		success: function(msg) {
			console.log(msg.color);
			$('.color_box').data('color', msg.color);
			updateColor();
		}
	});
	
    var $img = $(this);
    $slot.find('span').html("");
    $slot.find('span').html(ui.draggable.data( 'name' ));
    $slot.data('skill_id', skill.id);
	
	var img_src = ui.draggable.find('img').attr('src');
	var path = img_src.substring(0, img_src.lastIndexOf("/"));
	var file = img_src.substring(img_src.lastIndexOf("/"));
	
	
	console.log(path + "/64" + file);
	$(this).attr('src', path + "/64" + file);
	
}

function makeDroppable() {
    $('.slot img').droppable( {
        accept: $( ".drag", $( ".skill", $("#slider") ) ),
        hoverClass: 'hovered',
        drop: ajax_assign_skill
    });
}

$(function() {
	makeDroppable();
});