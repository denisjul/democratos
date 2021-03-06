//setup JQuery's AJAX methods to setup CSRF token in the request before sending it off.


function ConfirmDialog(qorigin, title, message, data) {
    $('<div></div>').appendTo('body')
                    .html('<div>'+message+'?</div>')
                    .dialog({
                        modal: true, title: title, zIndex: 10000, autoOpen: true,
                        width: 'auto', resizable: false,
                        buttons: {
                            Oui: function () {
                                Confirmresult(qorigin, true, data);
                                $(this).dialog("close");                               
                            },
                            Annuler: function () {                                                                
                                Confirmresult(qorigin, false, data);
                                $(this).dialog("close");
                            }
                        },
                        close: function (event, ui) {
                            $(this).remove();
                        }
                    });
};

function Confirmresult(qorigin, answer, data) {
    switch (qorigin){
        case "DelOwnRef":
            if (answer){
                $.ajax({
                    type: "POST",
                    url: '/CYL/DeleteReflection',
                    data: {'typeref': data[1] ,'idref': data[2] ,csrfmiddlewaretoken: csrftoken},
                    dataType: "json",
                    success: function(rs) {
                        alert(rs.message);
                        GoAjax(history.state.url, history.state.slug, false);

                    },
                    error: function(rs, e) {
                        alert(rs.responseText);
                    }
                });
            }
        //case
    }
}


function UpAndDown(tomodif,dontomodif,slug,url){
    $.ajax({
       type: "POST",
       url: url,
       data: {'slug': slug,csrfmiddlewaretoken: csrftoken},
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
}

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

function Setbutform(){
    $("#oppform").css('display','none');
    $("#opnform").css('display','none');
    $("#expform").css('display','none');
    $("#qstform").css('display','none');
    $("#prpform").css('display','none');

    $(".butopp").click(function(event) {
        if ( $("#oppform").css('display') == 'none' ){
            $("#oppform").css('display','block');
        }
        else{
            $("#oppform").css('display','none');
        }
    });
    $(".butopn").click(function(event) {
        if ( $("#opnform").css('display') == 'none' ){
            $("#opnform").css('display','block');
        }
        else{
            $("#opnform").css('display','none');
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
    $(".butqst").click(function(event) {
        if ( $("#qstform").css('display') == 'none' ){
            $("#qstform").css('display','block');
        }
        else{
            $("#qstform").css('display','none');
        }
    });
    $(".butprp").click(function(event) {
        if ( $("#prpform").css('display') == 'none' ){
            $("#prpform").css('display','block');
        }
        else{
            $("#prpform").css('display','none');
        }
    });
}

function SetDonuts(){
    $("#content").find('.donut').each(function(){
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
}

function loadckeditorJS () {
    var fileref=document.createElement('script')
    fileref.setAttribute("type","text/javascript")
    fileref.setAttribute("src", 'ckeditor/ckeditor-init.js')
}

function SetTheForm(FormId){ // Il faut aussi joindre l'ID de la reflection auquel est attaché le form
    $('#'+FormId).on('submit',function() { // catch the form's submit event
        for ( instance in CKEDITOR.instances ) // recover data in CKeditor fields
            CKEDITOR.instances[instance].updateElement();
        var datatosend = $(this).serialize()
        datatosend['csrfmiddlewaretoken']=csrftoken
        // alert($(this).parent().parent().attr('id'));
        var place = '#' + $(this).parent().parent().attr('id')
        $.ajax({ // create an AJAX call...
            data: datatosend, // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success..
                $(place).html(response.reflection);
                var formtodel = "#" +  response.typeref + 'askform' + response.idref;
                $('#content').find(formtodel).html(' ');
                if (response.message != ""){
                    alert(response.message);
                }
                $('form').each(function(){
                    SetTheForm($(this).attr('id')) // joindre l'ID de la réflexion
                });
                /*switch(response.section_type){
                    case'exp':
                        $('#content').find('#exptd' + response.tdid).html(response.reflection); // update the DIV
                        break;
                       case'qst':
                        $('#content').find('#qsttd' + response.tdid).html(response.reflection); // update the DIV
                        break;
                       case'opn': // <----------------------------------------------------A REVOIR
                        $('.proposition').html(response.reflection); // update the DIV
                        break;
                    case 'prp':
                        $('.proposition').html(response.reflection); // update the DIV
                        break;
                    default:
                        alert('erreur sur la nature de la réflexion retournée');
                        break;
                };*/  
                Setbutform();
                SetDonuts();
            },
            error: function(rs, e) {
               alert(rs.responseText);
            },
        });
        return false;
    });
}

// #################  AJAX, Back and Forward ##########################


window.histstate = {pop:false, hash: false, lastref:false};

var popstatehaspoped = new Event("popstatehaspoped", {"bubbles":true, "cancelable":true});

window.addEventListener("popstatehaspoped",function(e){
    popstatehaspoped.stopPropagation();
    setTimeout(isbackorforward, 200);
});

function isbackorforward(){
    if (window.histstate.pop){
        if (window.histstate.hash){
            window.histstate.hash = false;
            window.histstate.pop = false;
            if (window.histstate.lastref && location.href.charAt(location.href.length - 1) == "#"){
                history.forward();
                console.log(location.href.slice(0,37));
                if (location.href.slice(0,37) == "http://127.0.0.1:8000/CYL/Reflection/"){
                    window.histstate.lastref = true;
                }
                else{
                    window.histstate.lastref = false;
                }               
            }
        }
        else{
            window.histstate.pop = false;
            console.log("on back    ", window.histstate,"   ", location.href)
            if (location.href.charAt(location.href.length - 1) == "#") {
                history.back();               
            }
            try{
                GoAjax(history.state.url, history.state.slug, false);
            }
            catch(e){
                GoAjax('/', null, false);
            }
        }
    }
}


window.addEventListener("hashchange",function(e){
    e.target.histstate.hash = true;
    console.log("hashchange: ", e.target.histstate.hash);
});


window.addEventListener("popstate",function(e){
    e.target.histstate.pop = true;
    console.log("popstate: ", e.target.histstate.pop);
    document.dispatchEvent(popstatehaspoped)
});

function GoAjax(url, slug, push) {
    console.log(url);
    if (url.indexOf("Reflection") > 0){
        url = url.replace("Reflection","reflection");
    }
    $.ajax({
        type: "POST",
        url: url,
        data: {'slug': slug ,csrfmiddlewaretoken: csrftoken},
        dataType: "json",
        success: function(response) {
            $("#intro").html(response.intro);
            $("#content").html(response.content);
            $('html,body').scrollTop(0);
            if (url == "/CYL/InDatBox"){
                console.log("InDatbox");
            }
            else{
                Setbutform();
                SetDonuts();
                loadckeditorJS();
                $('form').each(function(){
                    SetTheForm($(this).attr('id')) // joindre l'ID de la réflexion
                });
                $('textarea').each( function() {
                    CKEDITOR.replace( $(this).attr('id') );
                });
            }
            // need a pushState if not Back or Forward
            if (push){
                switch(url){
                    case "/CYL/InDatBox":
                        window.history.pushState({url: url,slug: slug}, null, url + "/" + response.box_type + "/" + response.box_id);
                        window.histstate.lastref = false;
                        break;
                    case "/CYL/Reflection":
                    case "/CYL/reflection":
                        if (url.indexOf("reflection") > 0){
                            url = url.replace("reflection","Reflection");
                        }
                        window.history.pushState({url: url,slug: slug}, null, url + "/" + response.typeref + "/" + response.id_ref);
                        window.histstate.lastref = true; 
                        break;                         
                    default:
                        console.log("GoAjax error")
                    }
                }
            },
        error: function(rs, e) {
        alert(rs.responseText);
        }
    });
}


// ##########################  MAIN   #############################



$(document).ready(function() {
    console.log("doc ready");
    // -------------Displaying Forms for q,exp,op etc. -------------
    Setbutform();
    // -------------- JStree settings ---------------------
    $("#jstree_CYL").jstree({
        'core' : {
          'data' : {
            'url' : function (node) {
                return node.id === '#' ?
                    '/CYL/nav_init' :   
                    '/CYL/nav_up/' + node.id;
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
                var child = data.instance.get_node(data.node.children[i])
                if (child.a_attr.class === 'GetReflection'){
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
    SetDonuts();
    // --------------- up button -----------------------
    $('body').on('click','.UP',function(){
        var tomodif = '#' + $(this).attr('name').replace(':','');
        var dontomodif = '#don' + $(this).attr('name').replace(':','');   
        var slug = $(this).attr('name');     
        UpAndDown(tomodif,dontomodif,slug,'/CYL/UP');
    });

    // --------------- down button -----------------------
    $('body').on('click','.DOWN',function(){
        var tomodif = '#' + $(this).attr('name').replace(':','');
        var dontomodif = '#don' + $(this).attr('name').replace(':','');
        var slug = $(this).attr('name');
        UpAndDown(tomodif,dontomodif,slug,'/CYL/DOWN');
    });
    // --------------- ask for form -----------------------
    $('body').on('click','.butexp, .butqst',function(){
        if ($(this).attr('name').substring(3,7) != "form"){
            $.ajax({
                type: "GET",
                url: '/CYL/GetForm',
                data: {'name': $(this).attr('name') ,csrfmiddlewaretoken: csrftoken},
                dataType: "json",
                success: function(response) {
                    var idtomodif = "#" +  response.typeref + 'askform' + response.idref;
                    $('#content').find(idtomodif).html(response.newform);
                    $('#content').find("form").each(function(){
                        SetTheForm($(this).attr('id'));
                    });
                    loadckeditorJS();
                    $('form').each(function(){
                        $('textarea').each( function() {
                            CKEDITOR.replace( $(this).attr('id') );
                        });
                        SetTheForm($(this).attr('id')) // joindre l'ID de la réflexion
                    });
                },
                error: function(rs, e) {
                    alert(rs.responseText);
                }
            });
        /*}
        else {
            SetTheForm($(this).attr('name'));*/
        };

    });
   
    // --------------- Checkbox suscribe -----------------------
    $('.suscribe').click(function() {
        var checked = $(this).is(':checked');
        var idbox = $(this).attr('id').replace('check','');
        var typeref = idbox.substring(0,3);
        var ref_id = idbox.slice(3,idbox.length);
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
                    alert('Vous êtes désabonné');
                }
            },
            error: function() {
                alert('it broke');
            },
        });
    });
   
    // --------------- Box loading AJAX -----------------------
    $("body").on("click",".InDatBox",function(){
        var url = '/CYL/InDatBox';
        var slug = $(this).attr('name');
        GoAjax(url,slug,true);
    });

    // --------------- Reflection  loading AJAX -------------------
    $("body").on("click",".GetReflection",function(){
        var url = '/CYL/reflection';
        var slug = $(this).attr('name');
        GoAjax(url,slug,true);
    });
       //---------------------  Get Child comments---------------------
    $("body").on("click", ".GetDebateChild",function(){
        $.ajax({
            type: "POST",
            url: '/CYL/childcomments',
            data: {'slug': $(this).attr('name') ,csrfmiddlewaretoken: csrftoken},
            dataType: "json",
            success: function(response) {
                var idtomodif = "#child" +  response.typeref + response.idref;
                $('#content').find(idtomodif).replaceWith(response.newcomments);
                SetDonuts();
                ConfirmDialog('Êtes vous sûr de vouloir supprimer cette réflexion?');
            },
            error: function(rs, e) {
                alert(rs.responseText);
            }
        });
    });
    //---------------------  Delete own ref---------------------
    $('body').on('click', '.DelOwnRef', function(){
        var name = $(this).attr('name').split(":");
        console.log(name);
        ConfirmDialog("DelOwnRef", "supprimer réflexion", 'Êtes vous sûr de vouloir supprimer cette réflexion?', name);
    });
    //---------------------  Modif own ref---------------------
    $('body').on('click', '.ModifRef', function(){
        var data =  $(this).attr('name').split(":");
        $.ajax({
            type: "POST",
            url: '/CYL/ModifReflection',
            data: {'typerequest': 'form', 'typeform': data[1] ,'idform': data[2], 'typeref': data[3] ,'idref': data[4] ,csrfmiddlewaretoken: csrftoken},
            dataType: "json",
            success: function(rs) {
                    var idtomodif = "#" +  rs.typeform + 'td' + rs.idform;
                    var oldhtml = $('#content').find(idtomodif).html();
                    $('#content').find(idtomodif).html(rs.ModifForm);
                    $('#content').find("Cancel" + rs.typeform + rs.idform + "form").each(function(){
                        $(this).click(function(){
                            $('#content').find(idtomodif).html(oldhtml)
                        });
                    });
                    $('#content').find("form").each(function(){
                        SetTheForm($(this).attr('id'));
                    });
            },
            error: function(rs, e) {
                alert(rs.responseText);
            }
        });
    });
});