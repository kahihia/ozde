


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
			$( "#datepicker3" ).datepicker(
				{
				todayHighlight: true,
				startDate: today,
			    format: 'dd/mm/yyyy',
			    orientation: "bottom auto",
			    autoclose: true,
			    endDate: "+60d"
			});
			$( "#datepicker4" ).datepicker(
				{
				todayHighlight: true,
				startDate: today,
			    format: 'dd/mm/yyyy',
			    orientation: "bottom auto",
			    autoclose: true,
			    endDate: "+60d"
			});
			$( "#datepicker5" ).datepicker(
				{
				todayHighlight: true,
			    format: 'yyyy-mm-dd',
			    orientation: "bottom auto",
			    autoclose: true,
			});
			$( "#datepicker7" ).datepicker({
				todayHighlight: true,
				startDate: today,
			    format: 'dd/mm/yyyy',
			    orientation: "bottom auto",
			    autoclose: true,
			    endDate: "+60d"
			});
			$( "#datepicker8" ).datepicker({
				todayHighlight: true,
				startDate: today,
			    format: 'dd/mm/yyyy',
			    orientation: "bottom auto",
			    autoclose: true,
			    endDate: "+60d"
			});
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
    	
    	$('.hotel_tab_act').tipsy({gravity: 's'});
		$('.bus_tab_act').tipsy({gravity: 's'});

    	$('.hotel_tab_act').click(function(){
 			$('#tab-1').addClass('active in').show( "slide", { direction: "left"  }, 200 );
 			$('#tab-3').removeClass('active in').hide( "slide", { direction: "right"  }, 200 );
 			$('.hotel_tab_act').addClass("menu_active")
 			$('.bus_tab_act').removeClass("menu_active")
 			
		});

		$('.bus_tab_act').click(function(){
  			$('#tab-1').removeClass('active in').hide( "slide", { direction: "right"  }, 200 );
 			$('#tab-3').addClass('active in').show( "slide", { direction: "left"  }, 200 );
 			$('.hotel_tab_act').removeClass("menu_active")
 			$('.bus_tab_act').addClass("menu_active")

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
					+"<option selected='selected' value='0' >0</option>"
					+"<option value='1' >1</option>"
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
					+"<option selected='selected' value='0' >0</option>"
					+"<option value='1' >1</option>"
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

    	$('#oneway').click(function(){
	    	$('#oneway').attr('checked',true);
	    	$('#round').removeAttr('checked');
		});

		$('#round').click(function(){
	    	$('#round').attr('checked',true);
	    	$('#oneway').removeAttr('checked');
		}); 

		$('.end_date').attr('disabled',true);

		$('input:radio[name=trip]').change(function() {
	    	if (this.value == 'oneway') {
	        	$('.end_date').attr('disabled',true);
	    	}
	    	else if (this.value == 'round') {
	        	$('.end_date').removeAttr('disabled');
	    	}
		});

//********************************hotel home page validation***********************************//
		$('#searchBtn').click(function(){ 
			var startDate = new Date($('.startdate').val());
			var endDate = new Date($('.enddate').val());
		    if($('.typeahead').val() == '') {
		        $('.error_mgs_city').show();
		        return false;
		    }
		    else{
		    	$('.error_mgs_city').hide();
		    }
		    if($('.startdate').val() == ''){
		        $('.error_mgs_start_date').show();
		        return false;
		    }
		    else{
		    	$('.error_mgs_start_date').hide();
		    }
		    if($('.enddate').val() == ''){
		        $('.error_mgs_end_date').show();
		        return false;
		    }
		    else{
		    	$('.error_mgs_end_date').hide();
		    }
		    if(startDate>=endDate){
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
		    	if($('.child_age_1').val() == ''){
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
		    	if($('.child_age_1').val() == ''){
		        	$('.error_mgs_child_age1').show();
		        	return false;
		    	}
		    	else if ($('.child_age_1').val() > 0){
		    		$('.error_mgs_child_age1').hide();
		    		if($('.child_age_2').val() == ''){
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
		var startDate = new Date($('.start_date').val());
		var endDate = new Date($('.end_date').val());
	    if($('.source').val() == '') {
	        $('.error_source').show();
	        return false;
	    }
	    else if($('.destination').val() == ''){
	        $('.error_destination').show();
	        return false;
	    }
	    else if($('.source').val() == $('.destination').val()){
	        $('.error_same').show();
	        return false;
	    }
	    else if($('.start_date').val() == ''){
	        $('.error_start').show();
	        return false;
	    }
	    else if($('#round').is(':checked')) {
	    	if($('.end_date').val() == ''){
	        	$('.error_end').show();
	        return false;
	     	}
	     	else if(startDate>=endDate){
	     		$('.error_date').show();
	     	}
	    }
	    else{
	        return true;
	    }
	});
	
	
	});