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

function makeDroppable() {
    $('.skillset_slot').droppable( {
        accept: $( "img", $("#skills")),
        hoverClass: 'hovered',
        drop: ajax_assign_skill
    });
}

$(function() {
    for ( var i=0; i<5; i++ ) {
        $('#skillset_skill'+i).droppable( {
            accept: $( "img", $("#skills")),
            hoverClass: 'hovered',
            drop: ajax_assign_skill
        });
    }
    
	makeDroppable();
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

$(function() {
	makeDroppable();
});