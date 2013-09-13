$('#project_form').submit(function(){
	var $ajaxData = $('#project_form').serializeArray();
	$ajaxData.push({name: 'member_list', value: createMemberString()});
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
				console.log("redirect");
				window.location = "/projects/" + msg.project_id;
			}
        }
    });
	return false;
});

function createMemberString() {
	  
	var members = [];
	$('.member').each(function() {
		
		var member = new Object();
		member.id = $(this).data('id');
		member.slots = [];
		
		$(this).find('.slot').each(function() {
			var slot = new Object();
			slot.id = $(this).data('skill_id');
			slot.slot = $(this).data('slot');
			member.slots.push(slot);
		})
		
		member.name = $(this).find('input').val();
		member.desc = $(this).find('textarea').val();
		
		members.push(member);
	});	
	
	var jsonString = JSON.stringify(members);	  
	return jsonString;
}


var $str = "<div class=\"member\">";
$str += "<div class=\"member_info\">"
$str += "<label>Bezeichnung:</label><input></input><br />"
$str += "<label>Beschreibung:</label><textarea rows=\"3\" cols=\"60\"></textarea>"
$str += "</div>"
$str += "<div class=\"slots\">"	
for (var i=0; i<5; i++) {
	$str += "<div class=\"slot\" data-slot=\""+i+"\">"
	$str += "<img src=\"/static/img/open.png\" alt=\"open\">"
	$str += "<span>offen</span></div>"
}
$str += "</div>"
$str += "</div>"

$('.add_slot').click(function() {
	console.log("test");
	$('#member_slots').append($str);	
	makeDroppable();
});

function makeDroppable() {
    $('.slot img').droppable( {
        accept: $( ".drag", $( ".skill", $("#slider") ) ),
        hoverClass: 'hovered',
        drop: project_assign_skill
    });
}

function project_assign_skill( event, ui ){
	var skill_id = ui.draggable.data( 'id' );
	console.log(skill_id);
    var $img = $(this);
    
    $slot = $(this).parent();
    $slot.find('span').html("");
    $slot.find('span').html(ui.draggable.data( 'name' ));
    $slot.data('skill_id', skill_id);
    
	var img_src = ui.draggable.find('img').attr('src');
	var path = img_src.substring(0, img_src.lastIndexOf("/"));
	var file = img_src.substring(img_src.lastIndexOf("/"));
	
	
	console.log(path + "/64" + file);
	$(this).attr('src', path + "/64" + file);
	
}

$(function() {
	makeDroppable();
});