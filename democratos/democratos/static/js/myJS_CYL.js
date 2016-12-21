
//setup JQuery's AJAX methods to setup CSRF token in the request before sending it off.

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');



// ##########################  MAIN   #############################

$(document).ready(function() {
	// -------------Displaying Forms for q,exp,op etc. -------------
	$(".opform").css('display','none');
	$(".expform").css('display','none');
	$(".qform").css('display','none');
	$(".disform").css('display','none');
	$(".propform").css('display','none');

	$(".butopinion").click(function(event) {
		if ( $(".opform").css('display') == 'none' ){
		    $(".opform").css('display','block');
		}
		else{
			$(".opform").css('display','none');
		}
	});

	$(".butcom").click(function(event) {
		if ( $(".expform").css('display') == 'none' ){
		    $(".expform").css('display','block');
		}
		else{
			$(".expform").css('display','none');
		}

	});
	$(".butq").click(function(event) {
		if ( $(".qform").css('display') == 'none' ){
		    $(".qform").css('display','block');
		}
		else{
			$(".qform").css('display','none');
		}
	});
	$(".butdis").click(function(event) {
		if ( $(".disform").css('display') == 'none' ){
		    $(".disform").css('display','block');
		}
		else{
			$(".disform").css('display','none');
		}
	});
	$(".butprop").click(function(event) {
		if ( $(".propform").css('display') == 'none' ){
		    $(".propform").css('display','block');
		}
		else{
			$(".propform").css('display','none');
		}
	});


	// -------------- JStree settings ---------------------
	$("#jstree_CYL").jstree({  
		'core' : {
		  'data' : {
		    'url' : function (node) {
		      return node.id === '#' ?
				        'http://localhost:8000/CYL/nav_init' :    // A modifier lors de la mise en prod
					    'http://localhost:8000/CYL/nav_up/' + node.id;  // A modifier lors de la mise en prod
		    },

		    'data' : function (node) {
		      return JSON.stringify({ 'id' : node.id, 'text': node.text});
		    }
		  }
		},
	});

	$('#jstree_CYL').on('select_node.jstree', function (e, data) {
	    window.location = data.node.a_attr.href;
	});

	// --------------- resizable nav -----------------------
    var container = $("body");
    var numberOfCol = 2; 
    var sibTotalWidth;
    $("nav").resizable({
        handles: 'e',
        start: function(event, ui){
            sibTotalWidth = ui.originalSize.width + ui.originalElement.next().outerWidth();
        },
        stop: function(event, ui){     
            var cellPercentWidth=100 * ui.originalElement.outerWidth()/ container.innerWidth();
            ui.originalElement.css('width', cellPercentWidth + '%');  
            var nextCell = ui.originalElement.next();
            var nextPercentWidth=100 * nextCell.outerWidth()/container.innerWidth();
            nextCell.css('width', nextPercentWidth + '%');
        },
        resize: function(event, ui){ 
            ui.originalElement.next().width(sibTotalWidth - ui.size.width); 
        }
    });

    // --------------- up button -----------------------
    $('.UP').click(function(){
         	 $.ajax({
               type: "POST",
               url: 'http://localhost:8000/CYL/UP', // A modifier lors de la mise en prod
               data: {'slug': $(this).attr('name') ,csrfmiddlewaretoken: csrftoken},
               dataType: "json",
               success: function(response) {
                      if (response.message != ""){
                      		alert(response.message)
                      	};
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          }); 
    })
    // --------------- down button -----------------------
     $('.DOWN').click(function(){
         	 $.ajax({
               type: "POST",
               url: 'http://localhost:8000/CYL/DOWN', // A modifier lors de la mise en prod
               data: {'slug': $(this).attr('name') ,csrfmiddlewaretoken: csrftoken},
               dataType: "json",
               success: function(response) {
                      if (response.message != ""){
                      		alert(response.message)
                      	};
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          }); 
    })
});


