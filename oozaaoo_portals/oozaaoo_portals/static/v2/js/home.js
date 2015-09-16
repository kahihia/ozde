


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
			    format: 'dd/mm/yyyy',
			    orientation: "top left",
			    autoclose: true,
			    endDate: "+60d"
			});
			$( "#datepicker2" ).datepicker(
				{
				todayHighlight: true,
				startDate: today,
			    format: 'dd/mm/yyyy',
			    orientation: "top left",
			    autoclose: true,
			    endDate: "+60d"
			});
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

		var add_room_search = $('.add_room_holder_search');
		$('.add_room_act_search').click(function (e) {
			e.preventDefault();
			if(i < max_fields){
				i++;
				$(add_room_search).append("<div class='clonedInput' id='clonedInput0'>"
					+"<label>Rooms "+i+"</label>"
					+"<input class='form-control hidden_input' name='room"+i+"' type='hidden' value='"+i+"' readonly='readonly' />"
					+"<div class='fl add_room_fields add_room_fields_87 adults'>"
					+"<div class='form-group form-group-md form-group-select-plus nomargin'>"
					+"<label>Adults</label>"                                       
					+"<select id='adults"+i+"' class='form-control adults' name='adults"+i+"'>"  
					+"<option selected='selected' value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"<option value='3' >3</option>"
					+"<option value='4' >4</option>"
					+"</select><div class='error_mgs_adult' style='display:none; color:red;'>Enter the no of adults</div></div></div>"
					+"<div class='fl add_room_fields add_room_fields_87 childs'>"
					+"<div class='form-group form-group-md form-group-select-plus nomargin'>"
					+"<label>Children</label>"                                     
					+"<select id='childs"+i+"' class='form-control child_age_act child' name='childs"+i+"'> "
					+"<option selected='selected' value='0' >0</option>"
					+"<option value='1' >1</option>"
					+"<option value='2' >2</option>"
					+"</select><div class='error_mgs_child' style='display:none; color:red;'>Enter the child age</div>"
					+"</div>"
					+"</div>"
					+"<div class='fl add_room_fields child-1-act dn' id='test1'>"
					+"<div class='form-group form-group-md form-group-select-plus nomargin'>"
					+"<label>Child-1 age</label>"                              
					+"<select id='childage1_"+i+"' class='form-control child_age child_age_1' name='childage1_"+i+"'> "  
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
					+"<select id='childage2_"+i+"' class='form-control child_age child_age_2' name='childage2_"+i+"'> "
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


		$(add_room_search).on("click",".remove_room_fields_act", function(e){ //user click on remove text
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
	     		return false;
	     	}
	    }
	    else{
	        return true;
	    }
	});
	
	$('#done').click(function(){
		var room1=$('input[name="room1"]').val();
		var room2=$('input[name="room2"]').val()==null?0:1;
		var room3=$('input[name="room3"]').val()==null?0:1;
		var room4=$('input[name="room4"]').val()==null?0:1;
		var adults1=$('#adults1').val();
		var adults2=$('#adults2').val()==null?0:$('#adults2').val();
		var adults3=$('#adults3').val()==null?0:$('#adults3').val();
		var adults4=$('#adults4').val()==null?0:$('#adults4').val();
		var childs1=$('#childs1').val();
		var childs2=$('#childs2').val()==null?0:$('#childs1').val();
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
		var no_of_rooms=parseInt(room1)+parseInt(room2)+parseInt(room3)+parseInt(room4);
		var guest=parseInt(adults1)+parseInt(childs1)+parseInt(adults2)+parseInt(childs2)+parseInt(adults3)+parseInt(childs3)+parseInt(adults4)+parseInt(childs4);	
		$('.details_rooms').text(no_of_rooms+'Rooms/'+guest+'Guest');
	});


	
});