// #######################  functions   ###########################
function set_to_info () {
		$("#Profile_set").css('background-color','#6666ff')
		$("#Change_pwd").css('background-color','#f0f0f0')
		$("#del_account").css('background-color','#f0f0f0')
		$("#suscr_set").css('background-color','#f0f0f0')
		$("#up_profile").css('display','inline');
		$("#change_pwd").css('display','none');
		$("#del_profile").css('display','none');
		$("#suscription_profile").css('display','none');
}

function set_to_pwd() {
		$("#Profile_set").css('background-color','#f0f0f0')
		$("#Change_pwd").css('background-color','#6666ff')
		$("#del_account").css('background-color','#f0f0f0')
		$("#suscr_set").css('background-color','#f0f0f0')
		$("#up_profile").css('display','none');
		$("#change_pwd").css('display','inline');
		$("#del_profile").css('display','none');
		$("#suscription_profile").css('display','none');
	}

function set_to_del() {
		$("#Profile_set").css('background-color','#f0f0f0')
		$("#Change_pwd").css('background-color','#f0f0f0')
		$("#del_account").css('background-color','#6666ff')
		$("#suscr_set").css('background-color','#f0f0f0')
		$("#up_profile").css('display','none');
		$("#change_pwd").css('display','none');
		$("#del_profile").css('display','inline');
		$("#suscription_profile").css('display','none');
	}

function set_to_suscr() {
		$("#Profile_set").css('background-color','#f0f0f0')
		$("#Change_pwd").css('background-color','#f0f0f0')
		$("#del_account").css('background-color','#f0f0f0')
		$("#suscr_set").css('background-color','#6666ff')
		$("#up_profile").css('display','none');
		$("#change_pwd").css('display','none');
		$("#del_profile").css('display','none');
		$("#suscription_profile").css('display','inline');
	}

function update_page(){
		if ($("#set_var").html() == "info"){
			set_to_info();
		}
		else if ($("#set_var").html() == "pwd"){
			set_to_pwd();
		}
		else if ($("#set_var").html() == "del"){
			set_to_del();
		}
		else if ($("#set_var").html() == "suscr"){
			set_to_suscr();
		}
	};

// ##########################  MAIN   #############################

$(document).ready(function() {
	// -------------Displaying Forms for q,exp,op etc. -------------
	$("#Profile_set").css('background-color','#6666ff')
	$("#change_pwd").css('display','none');
	$("#del_profile").css('display','none');
	$("#suscription_profile").css('display','none');

	$("#set_var").ready(function(event){
		update_page();
	});

	window.scrollTo(0, 0)

	$("#Profile_set").click(function(event) {
		$("#set_var").html("info");
		update_page();
	});
	$("#Change_pwd").click(function(event) {
		$("#set_var").html("pwd");
		update_page();
	});
	$("#del_account").click(function(event) {
		$("#set_var").html("del");
		update_page();
	});
	$("#suscr_set").click(function(event) {
		$("#set_var").html("suscr");
		update_page();
	});
});
