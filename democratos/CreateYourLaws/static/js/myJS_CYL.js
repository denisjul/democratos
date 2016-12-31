//setup JQuery's AJAX methods to setup CSRF token in the request before sending it off.


// This function gets cookie with a given name
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

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// ############################  Objects  ##############################

// The donut widget

var DonutChart = function (canvas, radius, lineWidth, arraySlices, label) {
    this._radius = radius;
    this._lineWidth = lineWidth; //px
    this._arraySlices = arraySlices;
    this.label = label;
    this._x_center = canvas.width / 2;
    this._y_center = canvas.height / 2;
    this._context = canvas.getContext("2d");

    this.drawCircle = function () {
        var context = this._context;
        context.lineWidth = this._lineWidth;
        var radius = this._radius;
        var offset_radians = -0.5 * Math.PI;
        var start_radians = offset_radians;
        var counterClockwise = true;
        var self = this;
        this._arraySlices.forEach(function (slice) {
            context.beginPath();
            context.strokeStyle = slice.color;
            var end_radians = start_radians - (Math.PI * 2) * slice.percent / 100;
            context.arc(self._x_center, self._y_center, radius,
            start_radians, end_radians, counterClockwise);
            context.stroke();
            start_radians = end_radians;
        });
    };

    this.drawText = function () {
        var fontSize = this.label.font_size;
        var context = this._context;
        context.font = 'bold ' + fontSize + 'pt Arial';
        context.textAlign = 'center';
        context.fillStyle = this.label.color;
        var text = this.label.text;
        context.fillText(text, this._x_center, this._y_center + fontSize / 2);
    };

    this.render = function () {
        this.drawCircle();
        this.drawText();
    };
};

// ######################### functions ############################



// ##########################  MAIN   #############################

$(document).ready(function() {
	// preload icons for JStree?????

	// -------------Displaying Forms for q,exp,op etc. -------------
	$("#opform").css('display','none');
	$("#expform").css('display','none');
	$("#qform").css('display','none');
	$("#disform").css('display','none');
	$("#propform").css('display','none');

	$(".butopinion").click(function(event) {
		if ( $("#opform").css('display') == 'none' ){
		    $("#opform").css('display','block');
		}
		else{
			$("#opform").css('display','none');
		}
	});
	$(".butexp").click(function(event) {
		if ( $("#expform").css('display') == 'none' ){
		    $("#expform").css('display','block');
		}
		else{
			$("#expform").css('display','none');
		}

	});
	$(".butq").click(function(event) {
		if ( $("#qform").css('display') == 'none' ){
		    $("#qform").css('display','block');
		}
		else{
			$("#qform").css('display','none');
		}
	});
	$(".butdis").click(function(event) {
		if ( $("#disform").css('display') == 'none' ){
		    $("#disform").css('display','block');
		}
		else{
			$("#disform").css('display','none');
		}
	});
	$(".butprop").click(function(event) {
		if ( $("#propform").css('display') == 'none' ){
		    $("#propform").css('display','block');
		}
		else{
			$("#propform").css('display','none');
		}
	});


	// -------------- JStree settings ---------------------
	$("#jstree_CYL").jstree({ 
		'core' : {
		  'data' : {
		    'url' : function (node) {
		      return node.id === '#' ?
				        '/CYL/nav_init' :    // A modifier lors de la mise en prod
					    '/CYL/nav_up/' + node.id;  // A modifier lors de la mise en prod
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
	$('#jstree_CYL').on('load_node.jstree', function (e, data) {
		if (data.node.id != '#'){
			for (var i= 0; i < data.node.children.length; i++) {
				console.log('hey')
				var child = data.instance.get_node(data.node.children[i])
				if (child.a_attr.class === 'Reflection'){
					data.instance.set_icon(child, "/static/icons/article.png");
				}
				else {
					data.instance.set_icon(data.node.children[0],true);
				}
			}
		}
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

    // --------------- Set Donuts -----------------------
    $('.donut').each(function(){
    	$(this).on('MakeMyDonuts', function(event, value) {
    		var nameread = $(this).attr('name').replace(',','.')
		    var value = (typeof value !== 'undefined') ? value : parseFloat(nameread);
		    //var value = parseInt($(this).attr('name'));
		    var donvalue = Math.round(((parseFloat(value))+100)*5)/10;
		    var canvas = $(this).get(0);
		    var sideLength = 36;
		    canvas.width = canvas.height = sideLength;
		    canvas.width +=  canvas.width*0.33;
		    var lineWidth = 9;
		    var radius = (sideLength - lineWidth) / 2;
		    var slices = [{
		        percent: 100-donvalue,	
		        color: "#ff7474"
		    }, {
		        percent: donvalue,
		        color: "#4ce64c"
		    }];
		    if (value >= 0){
			    var label = {
			        text: donvalue + '%',
			        color: "#007a00",
			        font_size: 11,
		    	};
		   	}
			else{
				var label = {
				    text: donvalue + '%',
				    color: "#992600",
				    font_size: 11,
				};
			}
		    var donutChart = new DonutChart(canvas, radius, lineWidth, slices, label);
		    donutChart.render(); 
			});
    	$(this).trigger('MakeMyDonuts');
	});

    // --------------- up button -----------------------
    $('.UP').click(function(){
    	// var tomodif = '#' + $(this).attr('name').replace(':','');
     	var dontomodif = '#don' + $(this).attr('name').replace(':','');
         	 $.ajax({
               type: "POST",
               url: '/CYL/UP',
               data: {'slug': $(this).attr('name') ,csrfmiddlewaretoken: csrftoken},
               dataType: "json",
               success: function(response) {
                    if (response.message != ""){
                  		alert(response.message)
                  	};
                    if(response.data != {}){
						for (var key in response.data) {
							var context = $(key)[0].getContext('2d');
                    		context.clearRect(0, 0, context.width, context.height);
							$(key).trigger('MakeMyDonuts', response.data[key]);
						}
                    };
                    // $(tomodif).html(Math.round((parseFloat(response.approb))*100)/100);
                    var context = $(dontomodif)[0].getContext('2d');
                    context.clearRect(0, 0, context.width, context.height);
                    $(dontomodif).trigger('MakeMyDonuts', [response.approb]);
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          }); 
    });
    // --------------- down button -----------------------
    $('.DOWN').click(function(){
     	var tomodif = '#' + $(this).attr('name').replace(':','');
     	var dontomodif = '#don' + $(this).attr('name').replace(':','');
     	$.ajax({
            type: "POST",
            url: '/CYL/DOWN',
            data: {'slug': $(this).attr('name') ,csrfmiddlewaretoken: csrftoken},
            dataType: "json",
            success: function(response) {
                if (response.message != ""){
              		alert(response.message)
              	};
                $(tomodif).html(Math.round(parseFloat(response.approb)*100)/100);
                var context = $(dontomodif)[0].getContext('2d');
                context.clearRect(0, 0, context.width, context.height);
                $(dontomodif).trigger('MakeMyDonuts', [response.approb]);

            },
            error: function(rs, e) {
                alert(rs.responseText);
            }
        }); 
    });
    // --------------- Checkbox suscribe -----------------------
	$('.suscribe').click(function() {
	    var checked = $(this).is(':checked');
	    var idbox = $(this).attr('id').replace('check','')
	    var typeref = idbox.substring(0,3)
	    var ref_id = idbox.slice(3,idbox.length)
	    $.ajax({
	        type: "POST",
	        url: '/CYL/checkbox',
	        data: { check : checked, typeref : typeref, ref_id : ref_id, csrfmiddlewaretoken: csrftoken},
	        dataType: "json",
	        success: function(data) {
	        	if (checked) {
	        		alert('Vous êtes abonné');
	        	}
	        	else{
	        		alert('Vous êtes désabonné')
	        	}
	        },
	        error: function() {
	            alert('it broke');
	        },
	    });
	});
	    // --------------- Box loading AJAX -----------------------
    $("body").on("click",".InDatBox",function(){
	 	$.ajax({
	        type: "POST",
	        url: '/CYL/InDatBox',
	        data: {'slug': $(this).attr('name') ,csrfmiddlewaretoken: csrftoken},
	        dataType: "json",
	        success: function(response) {
	            $("#intro").html(response.intro);
	            $("#content").html(response.content);
	        },
	        error: function(rs, e) {
	            alert(rs.responseText);
	        }
	    });
	});
		    // --------------- Reflection loading AJAX -------------------
    $("body").on("click",".GetReflection",function(){
	 	$.ajax({
	        type: "POST",
	        url: '/CYL/reflection',
	        data: {'slug': $(this).attr('name') ,csrfmiddlewaretoken: csrftoken},
	        dataType: "json",
	        success: function(response) {
	        	alert("wai")
	            $("#intro").html(response.intro);
	            $("#content").html(response.content);
	        },
	        error: function(rs, e) {
	            alert(rs.responseText);
	        }
	    });
	}); 
});
