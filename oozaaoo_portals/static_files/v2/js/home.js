


	$( ".mySelectCalendar2" ).datepicker({
      dateFormat: "yy/mm/dd",
      changeDate:true,
      changeMonth: true,//this option for allowing user to select month
      changeYear: true //this option for allowing user to select from year range
    });

	jQuery(function($) {
		"use strict";
		var nowDate = new Date();
		var today = new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate(), 0, 0, 0, 0)
			$( "#datepicker1" ).datepicker(
				{
				todayHighlight: true,
				startDate: today,
				onRender: function(date) {
					return date.valueOf() < today.valueOf() ? 'disabled' : '';
				},
			    format: 'dd/mm/yyyy',
			    orientation: "top left",
			    autoclose: true,
			    endDate: "+60d"
			}).on('changeDate', function(ev){
    			$('#datepicker1').datepicker('hide');
			});
			$( "#datepicker2" ).datepicker(
				{
				todayHighlight: true,
				startDate: today,
				onRender: function(date) {
					return date.valueOf() < today.valueOf() ? 'disabled' : '';
				},
			    format: 'dd/mm/yyyy',
			    orientation: "top left",
			    autoclose: true,
			    endDate: "+60d"
			}).on('changeDate', function(ev){
    			$('#datepicker2').datepicker('hide');
			});
			$( "#datepicker3" ).datepicker(
				{
				todayHighlight: true,
				startDate: today,
				onRender: function(date) {
					return date.valueOf() < today.valueOf() ? 'disabled' : '';
				},
			    format: 'dd/mm/yyyy',
			    orientation: "bottom auto",
			    autoclose: true,
			    endDate: "+60d"
			}).on('changeDate', function(ev){
    			$('#datepicker3').datepicker('hide');
			});
			$( "#datepicker4" ).datepicker(
				{
				todayHighlight: true,
				startDate: today,
				onRender: function(date) {
					return date.valueOf() < today.valueOf() ? 'disabled' : '';
				},
			    format: 'dd/mm/yyyy',
			    orientation: "bottom auto",
			    autoclose: true,
			    endDate: "+60d"
			}).on('changeDate', function(ev){
    			$('#datepicker4').datepicker('hide');
			});
			$( "#datepicker5" ).datepicker(
				{
				todayHighlight: true,
			    format: 'yyyy-mm-dd',
			    orientation: "bottom auto",
			    autoclose: true,
			}).on('changeDate', function(e) {
			$('#datepicker5').datepicker('hide');
        	});

			var checkin = $('#datepicker7').datepicker({
				format: 'dd/mm/yyyy',
				orientation: "bottom auto",
				onRender: function(date) {
					return date.valueOf() < today.valueOf() ? 'disabled' : '';
				}
				}).on('changeDate', function(ev) {
					if (ev.date.valueOf() > checkout.date.valueOf() || ev.date.valueOf() < checkout.date.valueOf()) {
						var newDate = new Date(ev.date)
						newDate.setDate(newDate.getDate() + 1);
						checkout.setValue(newDate);
					}
					checkin.hide();
					$('#datepicker8')[0].focus();
				}).data('datepicker');

			var checkout = $('#datepicker8').datepicker({
				format: 'dd/mm/yyyy',
				orientation: "bottom auto",
				onRender: function(date) {
					return date.valueOf() <= checkin.date.valueOf() ? 'disabled' : '';
				}
				}).on('changeDate', function(ev) {
					checkout.hide();
				}).data('datepicker');



	});
	jQuery(function($) {
		"use strict";
		var nowDate = new Date();
		var today = new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate(), 0, 0, 0, 0)
		var checkin = $('#datepicker9').datepicker({
			format: 'dd/mm/yyyy',
			orientation: "bottom left",
			onRender: function(date) {
				return date.valueOf() < today.valueOf() ? 'disabled' : '';
			}
			}).on('changeDate', function(ev) {
				if (ev.date.valueOf() > checkout.date.valueOf() || ev.date.valueOf() < checkout.date.valueOf()) {
					var newDate = new Date(ev.date)
					newDate.setDate(newDate.getDate() + 1);
					checkout.setValue(newDate);
				}
				checkin.hide();
				$('#datepicker10')[0].focus();
			}).data('datepicker');

		var checkout = $('#datepicker10').datepicker({
			format: 'dd/mm/yyyy',
			orientation: "bottom right",
			onRender: function(date) {
				return date.valueOf() <= checkin.date.valueOf() ? 'disabled' : '';
			}
			}).on('changeDate', function(ev) {
				checkout.hide();
			}).data('datepicker');
	});
 	$(document).on('change', '.child_age_act', function() {
          if($(this).val() == 0 ) {
               $(this).parent().parent().siblings(".child-1-act").hide();
               $(this).parent().parent().siblings(".child-2-act").hide();
         }

         if($(this).val() == 1 ) {
               $(this).parent().parent().siblings(".child-1-act").show();
               $(this).parent().parent().siblings(".child-2-act").hide();
         }
         if($(this).val() == 2 ) {
               $(this).parent().parent().siblings(".child-1-act").show();
               $(this).parent().parent().siblings(".child-2-act").show();
         }
         if($(this).val() == 3 ) {
               $(this).parent().parent().siblings(".child-1-act").show();
               $(this).parent().parent().siblings(".child-2-act").show();
         }
    });
    $(document).ready(function() {

		$('#reg_password').keyup(function(){
	        $('#reg_result').html(checkStrength($('#reg_password').val()));
	    });
		$("#reg_mobile").keypress(function (e) {
     		//if the letter is not digit then display error and don't type anything
		     if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        	//display error message
        	$("#digit_only").html("Digits Only").show().fadeOut("slow");
            return false;
    		}
   		});
		function checkStrength(password){
		    //initial strength
		    var strength = 0
		    //if the password length is less than 6, return message.
		    if (password.length < 6) {
		        $('#reg_result').removeClass();
		        $('#reg_result').addClass('short');
		        return 'Too short'
		    }
		    //length is ok, lets continue.
		    //if length is 8 characters or more, increase strength value
		    if (password.length > 7) strength += 1
		    //if password contains both lower and uppercase characters, increase strength value
		    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/))  strength += 1
		    //if it has numbers and characters, increase strength value
		    if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/))  strength += 1
		    //if it has one special character, increase strength value
		    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/))  strength += 1
		    //if it has two special characters, increase strength value
		    if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,",%,&,@,#,$,^,*,?,_,~])/)) strength += 1
		    //now we have calculated strength value, we can return messages
		    //if value is less than 2
		    if (strength < 2 ) {
		        $('#reg_result').removeClass();
		        $('#reg_result').addClass('weak');
		        return 'Weak'
		    } else if (strength == 2 ) {
		        $('#reg_result').removeClass();
		        $('#reg_result').addClass('good');
		        return 'Good'
		    } else {
		        $('#reg_result').removeClass();
		        $('#reg_result').addClass('strong');
		        return 'Strong'
		    }
		}

		$('#reg_mobile').keyup(function(){
			var mobile = document.getElementById('reg_mobile');
			var message = document.getElementById('reg_mobile_check');
			var goodColor = "#0C6";
			var badColor = "#a490da";
			if(mobile.value.length!=10){
			mobile.style.backgroundColor = badColor;
			message.style.color = badColor;
			message.innerHTML = "required 10 digits, match requested format!";
			}
			else {
				mobile.style.backgroundColor = goodColor;
				message.style.color = goodColor;
				message.innerHTML = "";
			}
		});


		$('#reg_submit').click(function(){
			if($('#reg_name').val()== ''){
				$('.reg_name_error').show();
				return false;
			}
			else{
				$('.reg_name_error').hide();
			}

			var reg = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/

			if($('#reg_email').val()== ''){
				$('.reg_email_error').show();
				return false;
			}
			else if (reg.test($('#reg_email').val())){
			  $('.reg_email_error').hide();
			  $('.reg_email_valid_error').hide();
		  }
			else{
				$('.reg_email_valid_error').show();
			   	return false;
			}
			if($('#reg_password').val().trim()== ''){
				$('.reg_password_error').show();
				return false;
			}
			else{
				$('.reg_password_error').hide();
			}
			if($('#reg_mobile').val()== ''){
				$('.reg_mobile_error').show();
				return false;
			}
			else{
				$('.reg_mobile_error').hide();
			}
			if($('#datepicker5').val()){
				$('.reg_dob_error').hide();
				return true;
			}
			else{
				$('.reg_dob_error').show();
				return false;
			}

		});


    	$('.hotel_tab_act').click(function(){
    		$('#tab-3').hide();
    		$('#tab-4').hide();
 			$('#tab-1').show( "slide", { direction: "left"  }, 400 );

 			$('.hotel_tab_act').addClass("menu_active");
 			$('.bus_tab_act').removeClass("menu_active");
 			$('.flight_tab_act').removeClass("menu_active");

		});

		$('.bus_tab_act').click(function(){
  			$('#tab-1').hide();
  			$('#tab-4').hide();
 			$('#tab-3').show( "slide", { direction: "left"  }, 400 );

 			$('.hotel_tab_act').removeClass("menu_active");
 			$('.bus_tab_act').addClass("menu_active");
 			$('.flight_tab_act').removeClass("menu_active");

		});

		$('.flight_tab_act').click(function(){
  			$('#tab-1').hide();
  			$('#tab-3').hide();
 			$('#tab-4').show( "slide", { direction: "left"  }, 400 );
 			$('.hotel_tab_act').removeClass("menu_active")
 			$('.bus_tab_act').removeClass("menu_active")
 			$('.flight_tab_act').addClass("menu_active");

		});

		var max_fields= 4;
		var i = 1;
		var add_room = $('.add_room_holder');
		$('.add_room_act').click(function (e) {
			e.preventDefault();
			if(i < max_fields){
				i++;
				$(add_room).append("<div class='clonedInput' id='clonedInput0'>"
					+"<label>Rooms "+i+"</label>"
					+"<input class='form-control hidden_input' name='room"+i+"' type='hidden' value='"+i+"' readonly='readonly' />"
					+"<div class='fl add_room_fields add_room_fields_87 adults'>"
					+"<div class='form-group form-group-md form-group-select-plus nomargin'>"
					+"<label>Adults</label>"
					+"<select class='form-control adults' name='adults"+i+"'>"
					+"<option selected='selected' value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"<option value='3' >3</option>"
					+"<option value='4' >4</option>"
					+"</select><div class='error_mgs_adult' style='display:none; color:red;'>Enter the no of adults</div></div></div>"
					+"<div class='fl add_room_fields add_room_fields_87 childs'>"
					+"<div class='form-group form-group-md form-group-select-plus nomargin'>"
					+"<label>Children</label>"
					+"<select class='form-control child_age_act child' name='childs"+i+"'> "
					+"<option selected='selected' value='0' >0</option>"
					+"<option value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"</select><div class='error_mgs_child' style='display:none; color:red;'>Enter the child age</div>"
					+"</div>"
					+"</div>"
					+"<div class='fl add_room_fields child-1-act dn' id='test1'>"
					+"<div class='form-group form-group-md form-group-select-plus nomargin'>"
					+"<label>Child-1 age</label>"
					+"<select class='form-control child_age child_age_1' name='childage1_"+i+"'> "
					+"<option selected='selected' value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"<option value='3' >3</option>"
					+"<option value='4' >4</option>"
					+"<option value='5' >5</option>"
					+"<option value='6' >6</option>"
					+"<option value='7' >7</option>"
					+"<option value='8' >8</option>"
					+"<option value='9' >9</option>"
					+"<option value='10' >10</option>"
					+"<option value='11' >11</option>"
					+"<option value='12' >12</option>"
					+"</select>"
					+"<div class='error_mgs_child_age1' style='display:none; color:red;''>Enter the child 1 age</div>"
					+"</div>"
					+"</div>"
					+"<div class='fl add_room_fields child-2-act dn'>"
					+"<div class='form-group form-group-md form-group-select-plus nomargin'>"
					+"<label>Child-2 age</label>"
					+"<select class='form-control child_age child_age_2' name='childage2_"+i+"'> "
					+"<option selected='selected' value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"<option value='3' >2</option>"
					+"<option value='4' >4</option>"
					+"<option value='5' >5</option>"
					+"<option value='6' >6</option>"
					+"<option value='7' >7</option>"
					+"<option value='8' >8</option>"
					+"<option value='9' >9</option>"
					+"<option value='10' >10</option>"
					+"<option value='11' >11</option>"
					+"<option value='12' >12</option>"
					+"</select>"
					+"<div class='error_mgs_child_age2' style='display:none; color:red;'>Enter the child age</div>"
					+"</div>"
					+"</div>"
					+"<div class='fl add_room_fields remove_room_fields remove_room_fields_act'> </div>"
					+"<div class='clear_both'> </div>"
					+"<div class='clear_both'> </div>"
					+"</div>");
			}
		});


		$(add_room).on("click",".remove_room_fields_act", function(e){ //user click on remove text
        	e.preventDefault(); $(this).parents('.clonedInput').remove(); i--;
    	});

		var add_room_modify = $('.add_room_holder_modify');
		$('.add_room_act_modify').click(function (e) {
			e.preventDefault();
			if(i < max_fields){
				i++;
				$(add_room_modify).append("<div class='clonedInput' id='clonedInput0'>"
					+"<label>Rooms "+i+"</label>"
					+"<input class='hidden_input' name='room"+i+"' type='hidden' value='"+i+"' readonly='readonly' />"
					+"<div class='fl adults'>"
					+"<div>"
					+"<label>Adults</label>"
					+"<select id='adults"+i+"' class='adults' name='adults"+i+"'>"
					+"<option selected='selected' value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"<option value='3' >3</option>"
					+"<option value='4' >4</option>"
					+"</select></div></div>"
					+"<div class='fl childs'>"
					+"<div>"
					+"<label>Children</label>"
					+"<select id='childs"+i+"' class='child_age_act child' name='childs"+i+"'> "
					+"<option selected='selected' value='0' >0</option>"
					+"<option value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"</select>"
					+"</div>"
					+"</div>"
					+"<div class='fl add_room_fields child-1-act dn' id='test1'>"
					+"<div>"
					+"<label>Child-1 age</label>"
					+"<select id='childage1_"+i+"' class='child_age child_age_1' name='childage1_"+i+"'> "
					+"<option selected='selected' value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"<option value='3' >3</option>"
					+"<option value='4' >4</option>"
					+"<option value='5' >5</option>"
					+"<option value='6' >6</option>"
					+"<option value='7' >7</option>"
					+"<option value='8' >8</option>"
					+"<option value='9' >9</option>"
					+"<option value='10' >10</option>"
					+"<option value='11' >11</option>"
					+"<option value='12' >12</option>"
					+"</select>"
					+"</div>"
					+"</div>"
					+"<div class='fl add_room_fields child-2-act dn'>"
					+"<div>"
					+"<label>Child-2 age</label>"
					+"<select id='childage2_"+i+"' class='child_age child_age_2' name='childage2_"+i+"'> "
					+"<option selected='selected' value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"<option value='3' >2</option>"
					+"<option value='4' >4</option>"
					+"<option value='5' >5</option>"
					+"<option value='6' >6</option>"
					+"<option value='7' >7</option>"
					+"<option value='8' >8</option>"
					+"<option value='9' >9</option>"
					+"<option value='10' >10</option>"
					+"<option value='11' >11</option>"
					+"<option value='12' >12</option>"
					+"</select>"
					+"</div>"
					+"</div>"
					+"<div class='fl add_room_fields remove_room_fields remove_room_fields_act_modify'> </div>"
					+"<div class='clear_both'> </div>"
					+"<div class='clear_both'> </div>"
					+"</div>");
			}
		});


		$(add_room_modify).on("click",".remove_room_fields_act_modify", function(e){ //user click on remove text
        	e.preventDefault(); $(this).parents('.clonedInput').remove(); i--;
    	});

		$('.details_rooms').click(function(){
			$('.add_room_right_side_holder').show();
			$('.add_room_right_side_holder').addClass('hotel_details_add_room');

		});

    	$('#oneway').click(function(){
	    	$('#oneway').attr('checked',true);
	    	$('#round').removeAttr('checked');
		});

		$('#round').click(function(){
	    	$('#round').attr('checked',true);
	    	$('#oneway').removeAttr('checked');
		});


		$('input:radio[name=trip]').change(function() {
	    	if (this.value == 'oneway') {
	        	$('.end_date,.f_end_date').attr('disabled',true);
	    	}
	    	else if (this.value == 'round') {
	        	$('.end_date,.f_end_date').removeAttr('disabled');
	    	}
		});

//********************************hotel home page validation***********************************//
		$('#searchBtn').click(function(){
			var startdate=$('.startdate').val().split('/');
			var enddate=$('.enddate').val().split('/');
			var startDate = new Date(startdate[1] + '/' + startdate[0] + '/' + startdate[2]);
			var endDate = new Date(enddate[1] + '/' + enddate[0] + '/' + enddate[2]);

		    if($('.typeahead').val() == '') {
		        $('.error_mgs_city').show();
		        return false;
		    }
		    else{
		    	$('.error_mgs_city').hide();
		    }
		    if($('.startdate').val() == ''){
		        $('.error_mgs_start_date').show();
		        $('.error_mgs_city').hide();
		        return false;
		    }
		    else{
		    	$('.error_mgs_start_date').hide();
		    }
		    if($('.enddate').val() == ''){
		        $('.error_mgs_end_date').show();
		        $('.error_mgs_start_date').hide();
		        return false;
		    }
		    else{
		    	$('.error_mgs_end_date').hide();
		    }
		    if(endDate<=startDate){

		    	$('.error_mgs_date').show();
		        return false;
		    }
		    // if($('.adults').val() == ''){
		    //     $('.error_mgs_adult').show();
		    //     return false;
		    // }
		    // else{
		    // 	$('.error_mgs_adult').hide();
		    // }
		    if($('.child').val() == ''){
		        $('.error_mgs_child').show();
		        return false;
		    }
		    else if($('.child').val() == 1){
		    	$('.error_mgs_child').hide();
		    	if($('.child_age_1').val() == 0){
		        	$('.error_mgs_child_age1').show();
		        	return false;
		    	}
		    	else if ($('.child_age_1').val() > 0){
		    		$('.error_mgs_child_age1').hide();
		    		return true;

		    	}
		    }
		   	else if($('.child').val() == 2){
		    	$('.error_mgs_child').hide();
		    	if($('.child_age_1').val() == 0){
		        	$('.error_mgs_child_age1').show();
		        	return false;
		    	}
		    	else if ($('.child_age_1').val() > 0){
		    		$('.error_mgs_child_age1').hide();
		    		if($('.child_age_2').val() == 0){
		        		$('.error_mgs_child_age2').show();
		        		return false;
		    		}
		    		else if($('.child_age_2').val() > 0){
		    			$('.error_mgs_child_age2').hide();
		    			return true;
		    		}

		    	}
		    }


		});
	//**************************for bus validation*******************************//
	$('#searchbus_return').click(function(){
		var startdate=$('.start_date').val().split('/');
		var enddate=$('.end_date').val().split('/');
		var startDate = new Date(startdate[1] + '/' + startdate[0] + '/' + startdate[2]);
		var endDate = new Date(enddate[1] + '/' + enddate[0] + '/' + enddate[2]);
	    if($('.source').val() == '') {
	        $('.error_source').show();
	        return false;
	    }
	    else if($('.destination').val() == ''){
	    	$('.error_source').hide();
	        $('.error_destination').show();
	        return false;
	    }
	    else if($('.source').val() == $('.destination').val()){
	        $('.error_same').show();
	        $('.error_destination').hide();
	        return false;
	    }
	    else if($('.start_date').val() == ''){
	        $('.error_start').show();
	         $('.error_same').hide();
	        return false;
	    }
	    else if($('#round').is(':checked')) {
	    	if($('.end_date').val() == ''){
	        	$('.error_end').show();
	        return false;
	     	}
	     	else if(startDate>=endDate){
	     		$('.error_date').show();
	     		return false;
	     	}
	    }
	    else{
	        return true;
	    }
	});

	$('#done').click(function(){
		$('.add_room_right_side_holder').hide();
		$('.add_room_right_side_holder').removeClass('hotel_details_add_room');
		$('.hotel_booknow').hide();
		var room1=$('input[name="room1"]').val();
		var room2=$('input[name="room2"]').val()==null?0:1;
		var room3=$('input[name="room3"]').val()==null?0:1;
		var room4=$('input[name="room4"]').val()==null?0:1;
		var adults1=$('#adults1').val();
		var adults2=$('#adults2').val()==null?0:$('#adults2').val();
		var adults3=$('#adults3').val()==null?0:$('#adults3').val();
		var adults4=$('#adults4').val()==null?0:$('#adults4').val();
		var childs1=$('#childs1').val();
		var childs2=$('#childs2').val()==null?0:$('#childs2').val();
		var childs3=$('#childs3').val()==null?0:$('#childs3').val();
		var childs4=$('#childs4').val()==null?0:$('#childs4').val();
		var childage1_1=$('#childage1_1').val();
		var childage2_1=$('#childage2_1').val();
		var childage1_2=$('#childage1_2').val()==null?0:$('#childage1_2').val();
		var childage2_2=$('#childage2_2').val()==null?0:$('#childage2_2').val();
		var childage1_3=$('#childage1_3').val()==null?0:$('#childage1_3').val();
		var childage2_3=$('#childage2_3').val()==null?0:$('#childage2_3').val();
		var childage1_4=$('#childage1_4').val()==null?0:$('#childage1_4').val();
		var childage2_4=$('#childage2_4').val()==null?0:$('#childage2_4').val();
		var modified_s_date = $('#datepicker9').val();
		split_s_date = modified_s_date.split('/');
		var modified_e_date = $('#datepicker10').val();
		split_e_date = modified_e_date.split('/');
		var joindata = $('#joindata').val();
		var spilt = joindata.split('-');
		var no_of_rooms=parseInt(room1)+parseInt(room2)+parseInt(room3)+parseInt(room4);
		if(no_of_rooms == '1'){
			var modified_joindata = spilt[0]+'-'+split_s_date[2]+split_s_date[1]+split_s_date[0]+'-'+split_e_date[2]+split_e_date[1]+split_e_date[0]+'-'+no_of_rooms+'-'+adults1+'_'+childs1+'_'+childage1_1+'_'+childage2_1;
		}
		else if(no_of_rooms == '2'){
			var modified_joindata = spilt[0]+'-'+split_s_date[2]+split_s_date[1]+split_s_date[0]+'-'+split_e_date[2]+split_e_date[1]+split_e_date[0]+'-'+no_of_rooms+'-'+adults1+'_'+childs1+'_'+childage1_1+'_'+childage2_1+'-'+adults2+'_'+childs2+'_'+childage1_2+'_'+childage2_2;
		}
		else if(no_of_rooms == '3') {
			var modified_joindata = spilt[0]+'-'+split_s_date[2]+split_s_date[1]+split_s_date[0]+'-'+split_e_date[2]+split_e_date[1]+split_e_date[0]+'-'+no_of_rooms+'-'+adults1+'_'+childs1+'_'+childage1_1+'_'+childage2_1+'-'+adults2+'_'+childs2+'_'+childage1_2+'_'+childage2_2+'-'+adults3+'_'+childs3+'_'+childage1_3+'_'+childage2_3;
		}
		else {
			var modified_joindata = spilt[0]+'-'+split_s_date[2]+split_s_date[1]+split_s_date[0]+'-'+split_e_date[2]+split_e_date[1]+split_e_date[0]+'-'+no_of_rooms+'-'+adults1+'_'+childs1+'_'+childage1_1+'_'+childage2_1+'-'+adults2+'_'+childs2+'_'+childage1_2+'_'+childage2_2+'-'+adults3+'_'+childs3+'_'+childage1_3+'_'+childage2_3+'-'+adults4+'_'+childs4+'_'+childage1_4+'_'+childage2_4;
		}
		var guest=parseInt(adults1)+parseInt(childs1)+parseInt(adults2)+parseInt(childs2)+parseInt(adults3)+parseInt(childs3)+parseInt(adults4)+parseInt(childs4);
		$('.details_rooms').text(no_of_rooms+'Rooms/'+guest+'Guest');
		$.ajax({
			  url: '/v2/gethoteldetails/',
			  type: 'post',
			  dataType: 'json',
			  data: {"joindata":modified_joindata},
			  success: function (data) {
				  $('.hotel_booknow').show();
				  if(data.rooms_data.length > 0 ){
					  $('.selectroomtypes').show();
					  $('.soldout').hide();
					  $('.selectroomtypes').empty();
					  for(var i=0;i<data.rooms_data.length;i++){
						  if(data.rooms_data[i].room_info.type_name){
						  //alert(data.rooms_data[i].mp);
						  $('.selectroomtypes').append('<option data-rpc='+data.rooms_data[i].rpc+' data-rtc='+data.rooms_data[i].rtc+' data-mp='+data.rooms_data[i].mp+' data-tp='+data.rooms_data[i].tp+' data-ttc='+data.rooms_data[i].ttc+' data-tp_alltax='+data.rooms_data[i].tp_alltax+'>'+data.rooms_data[i].room_info.type_name+'</option>');
					  		}
				  		}
						$('#joindata').val(modified_joindata);
						$('#selectedrpc').val(data.rooms_data[0].rpc);
						$('#selectedrtc').val(data.rooms_data[0].rtc);
						$('#mp').val(data.rooms_data[0].mp);
						$('#totalprice').val(data.rooms_data[0].tp);
						$('#totaltax').val(data.rooms_data[0].ttc);
						$('#totalprice_wt').val(data.rooms_data[0].tp_alltax);
						$('#roomname').val(data.rooms_data[0].room_info.type_name);
						$('.mp').html(data.rooms_data[0].mp);
					    $('.subtotal').html(data.rooms_data[0].tp);
			  		}
					else{
						$('.selectroomtypes').hide();
						$('.soldout').show();
						$('.mp').html('Rooms not available');
						$('.subtotal').html('Rooms not available');
					}


			  },

		});


	});
	// ============== For flight home page validation ============== //
	$('#flight_search_act').click(function(){
		var startdate=$('.f_start_date').val().split('/');
		var enddate=$('.f_end_date').val().split('/');
		var startDate = new Date(startdate[1] + '/' + startdate[0] + '/' + startdate[2]);
		var endDate = new Date(enddate[1] + '/' + enddate[0] + '/' + enddate[2]);
	    if($('.f_source').val() == '') {
	        $('.f_error_source').show();
	        return false;

	    }
		else{
			$('.f_error_source').hide();
		}
	    if($('.f_destination').val() == ''){
	        $('.f_error_destination').show();
	        return false;
	    }
		else{
			$('.f_error_destination').hide();
		}
	    if($('.f_source').val() == $('.f_destination').val()){
	        $('.error_same').show();
	        return false;
	    }
		else{
			$('.error_same').hide();
		}
	    if($('.f_start_date').val() == ''){
	        $('.f_error_start').show();
	        return false;
	    }
		else{
			$('.f_error_start').hide();
		}
	    if($('#round').is(':checked')) {
	    	if($('.f_end_date').val() == ''){
	        	$('.f_error_end').show();
	        return false;
	     	}
	     	else if(startDate>=endDate){
	     		$('.f_error_date').show();
	     		return false;
	     	}
	    }
		else if (parseInt($('#flight_adults').val())+parseInt($('#flight_childs').val())+parseInt($('#flight_infants').val()) > 9) {
			$('.f_traveller').show();
			return false;
		}
		else{
			$('.f_traveller').hide();
		}
		if (parseInt($('#flight_adults').val())>parseInt($('#flight_infants').val())) {
			return true;
		}
	    else{
	        $('.f_traveller_max').show();
			return false;
	    }
	});


});
