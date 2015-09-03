//------------------------------
//Picker
//------------------------------
jQuery(function($) {
"use strict";
var nowDate = new Date();
var today = new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate(), 0, 0, 0, 0)
	$( "#datepicker" ).datepicker();
	$( "#datepicker2" ).datepicker();
	$( "#datepicker3" ).datepicker(
		{
		todayHighlight: true,
		startDate: today,
	    format: 'yyyy/mm/dd'
	});
	$( "#datepicker4" ).datepicker(
		{
		todayHighlight: true,
		startDate: today,
	    format: 'yyyy/mm/dd'
	});
	$( "#datepicker5" ).datepicker();
	$( "#datepicker6" ).datepicker();
	$( "#datepicker7" ).datepicker({
		todayHighlight: true,
		startDate: today,
	    format: 'yyyy/mm/dd'
	});
	$( "#datepicker8" ).datepicker({
		todayHighlight: true,
		startDate: today,
	    format: 'yyyy/mm/dd'
	});
	$( "#datepicker9" ).datepicker();
	$( "#datepicker10" ).datepicker();
});


//------------------------------
//Custom Select
//------------------------------
jQuery(document).ready(function($){
"use strict";
	$('.mySelectBoxClass').customSelect();
	/* -OR- set a custom class name for the stylable element */
	//$('.customSelect2').customSelect({customClass:'customSelect2'});
});

function mySelectUpdate(){
"use strict";
	setTimeout(function (){
		$('.mySelectBoxClass').trigger('update');
		$('.customSelect2').trigger('update');
	}, 500);
}


$(window).resize(function() {
"use strict";
	mySelectUpdate();
});



//------------------------------
//Nicescroll
//------------------------------
jQuery(document).ready(function($) {
"use strict";
	var nice = jQuery("html").niceScroll({
		cursorcolor:"#ccc",
		background:"#fff",			
		cursorborder :"0px solid #fff",			
		railpadding:{top:0,right:0,left:0,bottom:0},
		//cursorwidth:"15px",
		cursorborderradius:"0px",
		cursoropacitymin:0,
		cursoropacitymax:0.7,
		boxzoom:true,
		autohidemode:false
	});  
	
	$("#air").niceScroll();
	$("#hotel").niceScroll();
	$("#car").niceScroll();
	$("#vacations").niceScroll();
	
	$('html').addClass('no-overflow-y');
	
});


//------------------------------
//Add rooms
//------------------------------
function addroom2(){
"use strict";
	$('.room2').addClass('block');
	$('.room2').removeClass('none');
	$('.addroom1').removeClass('block');
	$('.addroom1').addClass('none');
}
function removeroom2(){
"use strict";
	$('.room2').addClass('none');
	$('.room2').removeClass('block');
	
	$('.addroom1').removeClass('none');
	$('.addroom1').addClass('block');
}
function addroom3(){
"use strict";
	$('.room3').addClass('block');
	$('.room3').removeClass('none');
	
	$('.addroom2').removeClass('block');
	$('.addroom2').addClass('none');
}
function removeroom3(){
"use strict";
	$('.room3').addClass('none');
	$('.room3').removeClass('block');
	
	$('.addroom2').removeClass('none');
	$('.addroom2').addClass('block');			
}
	
	
	
//------------------------------
//TABS
//------------------------------
// Wait until the DOM has loaded before querying the document
$(document).ready(function(){
"use strict";
	$('ul.tabs').each(function(){
		// For each set of tabs, we want to keep track of
		// which tab is active and it's associated content
		var $active, $content, $links = $(this).find('a');

		// If the location.hash matches one of the links, use that as the active tab.
		// If no match is found, use the first link as the initial active tab.
		$active = $($links.filter('[href="'+location.hash+'"]')[0] || $links[0]);
		$active.addClass('active');
		$content = $($active.attr('href'));

		// Hide the remaining content
		$links.not($active).each(function () {
			$($(this).attr('href')).animate({'margin-left': -1000},{ duration: 500, queue: false }).hide();
		});
		
		// Bind the click event handler
		$(this).on('click', 'a', function(e){
			// Make the old tab inactive.
			$active.removeClass('active');
			$content.animate({'margin-left': -1000},{ duration: 500, queue: false });	
			$content.animate({'opacity': 0});
			//$content.hide();			

			// Update the variables with the new link and content
			$active = $(this);
			$content = $($(this).attr('href'));

			// Make the tab active.
			$active.addClass('active');
			setTimeout(function (){
				$content.animate({'opacity': 1});
				$content.animate({'margin-left': 0},{ duration: 500, queue: false }).show();	
			}, 500);	
			mySelectUpdate();

			// Prevent the anchor's default click action
			e.preventDefault();
		});
	});
});		
	
	
	
	
	
//-----------------------------------
//INTRO INITIALISATION AND ANIMATIONS
//-----------------------------------
	
$(document).ready(function($){
"use strict";	 
	var $iw = $(window).innerWidth();
	var $ih = $(window).innerHeight();	
	
	var $iwi = $(window).width();
	var $ihi = $(window).height();


	$('.loader').animate({'opacity': 1},{ duration: 200, queue: false });
	$('.bluediv').css({'width': $iw +'px', 'height': $ih +'px'});
 
 
	//loader position
	$('.loader').css({'left':$iwi/2.5+'px', 'top':'10%'});

});
	
$(function(){
"use strict";
	//PRELOAD IMAGES
	var $iwi = $(window).width();
	var images = [
		'../static/v2/img/parisbg.jpg',
		'../static/v2/img/couple.png',

		'../static/v2/img/logo-intro.png',
		'../static/v2/img/icon-facebook.png',
		'../static/v2/img/icon-twitter.png',
		'../static/v2/img/icon-gplus.png',
		'../static/v2/img/icon-youtube.png',
		'../static/v2/img/select.png',
		'../static/v2/img/girl.png',
	];

	$.preload(images, 1, function(last){

		for (var i = 0; i < this.length; i++) {
				$('<img height="200" src="' + this[i] + '" alt="" class="none"/>').appendTo('body');
		}

		if (last) {

					//WHEN PRELOAD FINISHES START JAVASCRIPT
					 $(document).ready(function($){
						"use strict";
						function StartAnimation() {
							var $screenwidth = $(window).innerWidth();
						
							if ($screenwidth >= 768){
								setTimeout(function (){
									
									
									var $iw = $(window).innerWidth();
									var $ih = $(window).innerHeight();					
								
									//initialize divs
									$('.bluediv').css({'opacity': 1});
									$('.whitediv').css({'opacity': 1});						
									$('.bluediv').css({'width': $iw +'px', 'height': $ih +'px'});
									$('.whitediv').css({'width': $iw/2 +'px', 'height': $ih +'px', 'top': 0 +'px'});
									$('.loader').animate({'opacity': 1},{ duration: 200, queue: false });
									$('.palmbgcontainer').css({'opacity': 1,'width': 1733 +'px', 'height': $ih+5 +'px'});
									
									
									
									//reset positions
									$('.logointro').css({'opacity': 0});	
									$('.tabscontainer').css({'opacity': 0});	
									$('.tabs').css({'opacity': 0});	
									$('.social').css({'opacity': 0});
									$('.palmbgcontainer').css({ 'left': '-750px'});
									$('.couple').css({'opacity': 1,'left': -220 +'px'});			
									$('.leaf').css({'opacity': 1,'left': -220 +'px'});	
									$('.b1,.b2,.b3,.b4,.b5,.b6').css({'opacity': 0});	

									$('.girl').css({'opacity': 0,'left': -400 +'px'});		
									$('.girl2').css({'opacity': 0,'left': -400 +'px'});	
									$('.dubai').css({'opacity': 0,'left': -200 +'px'});	
									$('.plane').css({'opacity': 0,'left': -100 +'px'});		
									$('.dubai').css({'opacity': 0,'left': -200 +'px'});	
									$('.girl-car').css({'opacity': 0,'left': -420 +'px'});					
									$('.road').css({'opacity': 0,'right': -400 +'px'});			
									$('.car').css({'opacity': 0,'left': -45 +'%'});	
									$('.girl-cruise').css({'opacity': 0,'left': -420 +'px'});					
									$('.cruise').css({'opacity': 0,'right': -100 +'px'});
									
														
									var $tw = $('.whitediv').width();
									$('#tab1,#tab2,#tab3,#tab4,#tab5,#tab6').css({'width': $tw/2 +'px' });							
									
									//loader position
									$('.loader').css({'left':$iwi/2.5+'px', 'top':'10%'});
								
									setTimeout(function (){
										$('.loader').animate({'opacity': 0},{ duration: 200, queue: false });			
									}, 0);	
									
									setTimeout(function (){
										$('.bluediv').animate({'width': $iw/2 +'px', 'height': $ih +'px'},{ duration: 400, queue: false });	
										$('.bluediv').animate({'margin-left': 0 +'px','margin-top':0 +'px'},{ duration: 200, queue: false });					
									}, 1000);
												
									//couple & bg animation
									setTimeout(function (){
										var $cw = $('.couple').width();
										$('.couple').animate({'opacity': 1,'left': -$cw/5.6 +'px','width':'100%'},{ duration: 8000, queue: false });
										$('.leaf').animate({'opacity': 1,'left': 0 +'px'},{ duration: 4000, queue: false });

										$('.palmbgcontainer').animate({
										  'left': '-800px',
										}, { duration: 4000, queue: false });	
										
									}, 1000);	
									
									setTimeout(function (){
										$('.logointro').animate({'opacity': 1},{ duration: 400, queue: false });	
										$('.tabscontainer').animate({'opacity': 1},{ duration: 400, queue: false });	
									}, 1500);
									
									setTimeout(function (){
										$('.tabs').animate({'opacity': 1},{ duration: 400, queue: false });	
										$('.social').animate({'opacity': 1},{ duration: 200, queue: false });				
									}, 1500);		
													
									//boolets animation
									setTimeout(function (){			$('.b1').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3500);			
									setTimeout(function (){			$('.b2').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3600);			
									setTimeout(function (){			$('.b3').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3700);			
									setTimeout(function (){			$('.b4').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3800);			
									setTimeout(function (){			$('.b5').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3900);
									setTimeout(function (){			$('.b6').animate({'opacity': 1},{ duration: 400, queue: false });			}, 4000);
									setTimeout(function (){			$('.b7').animate({'opacity': 1},{ duration: 400, queue: false });			}, 4100);		
									
									
									setTimeout(function (){
										$('#tab1').animate({'opacity': 1},{ duration: 1000, queue: false });	
										mySelectUpdate();
									}, 3000);
									
								}, 2000);
								
								
							}//endif
							else{

								setTimeout(function (){
									
									var $iw = $(window).innerWidth();
									var $ih = $(window).innerHeight();					
								
									//initialize divs
									$('.bluediv').css({'opacity': 1});
									$('.whitediv').css({'opacity': 1});						
									$('.bluediv').css({'width': $iw +'px', 'height': $ih +'px'});
									$('.whitediv').css({'width': $iw-70 +'px', 'height': $ih +'px', 'top': 0 +'px'});
									$('.loader').animate({'opacity': 1},{ duration: 200, queue: false });
									$('.palmbgcontainer').css({'opacity': 1,'width': 1733 +'px', 'height': $ih+5 +'px'});
									
									//reset positions
									$('.logointro').css({'opacity': 0});	
									$('.tabscontainer').css({'opacity': 0});	
									$('.tabs').css({'opacity': 0});	
									$('.social').css({'opacity': 0});
									$('.palmbgcontainer').css({ 'left': '-750px'});
									$('.couple').css({'opacity': 1,'left': -220 +'px'});		
									$('.leaf').css({'opacity': 1,'left': -220 +'px'});		
									$('.b1,.b2,.b3,.b4,.b5,.b6').css({'opacity': 0});
									
									$('.girl').css({'opacity': 0,'left': -400 +'px'});		
									$('.girl2').css({'opacity': 0,'left': -400 +'px'});	
									$('.dubai').css({'opacity': 0,'left': -200 +'px'});	
									$('.plane').css({'opacity': 0,'left': -100 +'px'});		
									$('.dubai').css({'opacity': 0,'left': -200 +'px'});	
									$('.girl-car').css({'opacity': 0,'left': -420 +'px'});					
									$('.road').css({'opacity': 0,'right': -400 +'px'});			
									$('.car').css({'opacity': 0,'left': -45 +'%'});	
									$('.girl-cruise').css({'opacity': 0,'left': -420 +'px'});					
									$('.cruise').css({'opacity': 0,'right': -100 +'px'});

									
									$('#tab1,#tab2,#tab3,#tab4,#tab5,#tab6').css({'width': $iw-70-20 +'px' });	

									
									//loader position
									$('.loader').css({'left':$iwi/2.5+'px', 'top':'10%'});
								
									setTimeout(function (){
										$('.loader').animate({'opacity': 0},{ duration: 200, queue: false });			
									}, 0);	
									
									setTimeout(function (){
										$('.bluediv').animate({'width': 70 +'px', 'height': $ih +'px'},{ duration: 400, queue: false });	
										$('.bluediv').animate({'margin-left': 0 +'px','margin-top':0 +'px'},{ duration: 200, queue: false });					
									}, 1000);
								
									//couple & bg animation
									setTimeout(function (){
										var $cw = $('.couple').width();
										$('.couple').animate({'opacity': 1,'left': -$cw/5.6 +'px'},{ duration: 8000, queue: false });
										$('.leaf').animate({'opacity': 1,'left': 0 +'px'},{ duration: 4000, queue: false });

										$('.palmbgcontainer').animate({
										  'left': '-800px',
										}, { duration: 4000, queue: false });	
										
									}, 1000);	
									
									setTimeout(function (){
										$('.logointro').animate({'opacity': 1},{ duration: 400, queue: false });	
										$('.tabscontainer').animate({'opacity': 1},{ duration: 400, queue: false });	
									}, 1500);
									
									setTimeout(function (){
										$('.tabs').animate({'opacity': 1},{ duration: 400, queue: false });	
										$('.social').animate({'opacity': 1},{ duration: 200, queue: false });				
									}, 1500);		
													
									//boolets animation
									setTimeout(function (){			$('.b1').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3500);			
									setTimeout(function (){			$('.b2').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3600);			
									setTimeout(function (){			$('.b3').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3700);			
									setTimeout(function (){			$('.b4').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3800);			
									setTimeout(function (){			$('.b5').animate({'opacity': 1},{ duration: 400, queue: false });			}, 3900);
									setTimeout(function (){			$('.b6').animate({'opacity': 1},{ duration: 400, queue: false });			}, 4000);		
									
									
									setTimeout(function (){
										$('#tab1').animate({'opacity': 1},{ duration: 1000, queue: false });
										mySelectUpdate();							
									}, 3000);
									
									
									
									
									
									
								}, 2000);
							}
							
						}//end start animation
						
						StartAnimation();					
						
						//var $getwidth = window.innerWidth;
						//var $getheight = window.innerHeight;
						//alert('Width:' + $getwidth + 'Height:' + $getheight);
						
						//on resize start again
						$(window).resize(function() {
						"use strict";
	
							/**/
							//if  device is touchscreen do not resize
							if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) != true ) {
							StartAnimation();
							}
							
						
							//StartAnimation();
							mySelectUpdate();
						});
						
						
						// Listen for orientation changes
						window.addEventListener("orientationchange", function() {
							// Announce the new orientation number
							//alert(window.orientation);
							var $orientation = window.orientation;
							if ( $orientation == -90){
							StartAnimation();
							}
							if ( $orientation == 0){
							StartAnimation();
							}							
						}, false);
						
						
						
					 });
					//END OF JAVASCRIPT
	 

				}

		});

});
	 
	
	//------------------------------
//TAB CHANGES
//------------------------------
function changeAnimation1(){
"use strict";
	$('.girl').animate({'opacity': 0,'left': -400 +'px'});		
	$('.girl2').animate({'opacity': 0,'left': -400 +'px'});	
	$('.dubai').animate({'opacity': 0,'left': -200 +'px'});	
	$('.plane').animate({'opacity': 0,'left': -100 +'px'});		
	$('.dubai').animate({'opacity': 0,'left': -200 +'px'});	
	// $('.girl-car').animate({'opacity': 0,'left': -420 +'px'});	
	$('.girl-car').css({'display':'none'});				
	$('.road').animate({'opacity': 0,'right': -400 +'px'});			
	$('.car').animate({'opacity': 0,'left': -45 +'%'});	
	$('.girl-cruise').animate({'opacity': 0,'left': -420 +'px'});					
	$('.cruise').animate({'opacity': 0,'right': -100 +'px'});	
	
	var $cw = $('.couple').width();
	$('.couple').animate({'opacity': 1,'left': -$cw/5.6 +'px'});			
	$('.palmbgcontainer').animate({'opacity': 1,'left': -800 +'px'},{ duration: 200, queue: false });	
	}	
function changeAnimation2(){
"use strict";
	$('.couple').animate({'opacity': 0,'left': -220 +'px'});			
	$('.palmbgcontainer').animate({'opacity': 0,'left': -750 +'px'});
	$('.girl').animate({'opacity': 0,'left': -400 +'px'});	
	$('.plane').animate({'opacity': 0,'left': -100 +'px'});	
	$('.girl-car').animate({'opacity': 0,'left': -420 +'px'});					
	$('.road').animate({'opacity': 0,'right': -400 +'px'});	
	$('.car').animate({'opacity': 0,'left': -45 +'%'});		
	$('.girl-cruise').animate({'opacity': 0,'left': -420 +'px'});					
	$('.cruise').animate({'opacity': 0,'right': -100 +'px'});			
	
	var $gg2w = $('.girl2').width();
	$('.girl2').animate({'opacity': 1,'left': 0 +'px'});		
	var $gdw = $('.dubai').width();
	$('.dubai').animate({'opacity': 1,'left': -$gdw/6 +'px'},{ duration: 200, queue: false });	
	
}	
function changeAnimation3(){
"use strict";
	$('.couple').animate({'opacity': 0,'left': -220 +'px'});			
	$('.palmbgcontainer').animate({'opacity': 0,'left': -750 +'px'});		
	$('.girl2').animate({'opacity': 0,'left': -400 +'px'});	
	$('.dubai').animate({'opacity': 0,'left': -200 +'px'});	
	$('.girl-car').animate({'opacity': 0,'left': -420 +'px'});					
	$('.road').animate({'opacity': 0,'right': -400 +'px'});				
	$('.car').animate({'opacity': 0,'left': -45 +'%'});		
	$('.girl-cruise').animate({'opacity': 0,'left': -420 +'px'});					
	$('.cruise').animate({'opacity': 0,'right': -100 +'px'});			

	var $ggw = $('.girl').width();
	$('.girl').animate({'opacity': 1,'left': 0+'px'});						
	$('.plane').animate({'opacity': 1,'left': 0 +'px'},{ duration: 1000, queue: false });			
}	
function changeAnimation4(){
"use strict";
	$('.couple').animate({'opacity': 0,'left': -220 +'px'});
	$('.girl').animate({'opacity': 0,'left': -400 +'px'});			
	$('.girl2').animate({'opacity': 0,'left': -400 +'px'});				
	$('.palmbgcontainer').animate({'opacity': 0,'left': -750 +'px'});		
	$('.dubai').animate({'opacity': 0,'left': -200 +'px'});	
	$('.plane').animate({'opacity': 0,'left': -100 +'px'});
	$('.girl-cruise').animate({'opacity': 0,'left': -420 +'px'});					
	$('.cruise').animate({'opacity': 0,'right': -100 +'px'});			

	var $gc2w = $('.girl-car').width();
	$('.girl-car').animate({'opacity': 1,'left': -$gc2w/3.7 +'px'});	
	
	$('.car').animate({'opacity': 1,'left': 0+'%'});						
	$('.road').animate({'opacity': 1,'right': -200 +'px'},{ duration: 200, queue: false });			
}			
function changeAnimation5(){
"use strict";
	$('.couple').animate({'opacity': 0,'left': -220 +'px'});
	$('.girl').animate({'opacity': 0,'left': -400 +'px'});			
	$('.girl2').animate({'opacity': 0,'left': -400 +'px'});				
	$('.palmbgcontainer').animate({'opacity': 0,'left': -750 +'px'});		
	$('.dubai').animate({'opacity': 0,'left': -200 +'px'});	
	$('.plane').animate({'opacity': 0,'left': -100 +'px'});	
	$('.girl-car').animate({'opacity': 0,'left': -420 +'px'});					
	$('.road').animate({'opacity': 0,'right': -400 +'px'});				
	$('.car').animate({'opacity': 0,'left': -45 +'%'});							

	var $gcw = $('.girl-cruise').width();
	$('.girl-cruise').animate({'opacity': 1,'left': 0 +'px','width':'100%'});						
	$('.cruise').animate({'opacity': 1,'right': -200 +'px'},{ duration: 1000, queue: false });			
}
function changeAnimation6(){
"use strict";
	$('.couple').animate({'opacity': 0,'left': -220 +'px'});
	$('.girl').animate({'opacity': 0,'left': -400 +'px'});			
	$('.girl2').animate({'opacity': 0,'left': -400 +'px'});				
	$('.palmbgcontainer').animate({'opacity': 0,'left': -750 +'px'});		
	$('.dubai').animate({'opacity': 0,'left': -200 +'px'});	
	$('.plane').animate({'opacity': 0,'left': -100 +'px'});	
	$('.girl-car').animate({'opacity': 0,'left': -420 +'px'});					
	$('.road').animate({'opacity': 0,'right': -400 +'px'});				
	$('.car').animate({'opacity': 0,'left': -45 +'%'});							

	var $gcw = $('.some1').width();
	$('.some1').animate({'opacity': 1,'left': 0 +'px','width':'100%'});						
	$('.cruise').animate({'opacity': 1,'right': -200 +'px'},{ duration: 1000, queue: false });			
}


/** Home Page Hotel Child Age **/
$(document).on('change', '.child_act', function() {     
         if($(this).val() == 0 ) {
               $(this).parents(".rooms").find(".child1").hide();
               $(this).parents(".rooms").find(".child2").hide();
         }

         if($(this).val() == 1 ) {
               $(this).parents(".rooms").find(".child1").show();
               $(this).parents(".rooms").find(".child2").hide();
         }
         if($(this).val() == 2 ) {
               $(this).parents(".rooms").find(".child1").show();
               $(this).parents(".rooms").find(".child2").show();
         }
         if($(this).val() == 3 ) {
               $(this).parents(".rooms").find(".child1").show();
               $(this).parents(".rooms").find(".child2").show();
         }
    });

$(document).ready(function($){	
	var max_fields= 4;
var i = 1;
var add_room = $('.add_room_holder');
$('.add_room_act').click(function (e) {
    e.preventDefault();
    if(i < max_fields){
        i++;
$(add_room).append("<div class='room"+i+" rooms' >"
        +"<div class='w50percent'>"
          +"<div class='wh90percent textleft'>"
            +"<span class='opensans size13'><b>ROOM "+i+"</b></span><br/>"
            +"<input class='form-control hidden_input' name='room"+i+"' type='hidden' value='"+i+"' readonly='readonly' /> " 
          +"</div>"
        +"</div>"

        +"<div class='w50percentlast'>"  
          +"<div class='wh90percent textleft right'>"
           +"<div class='w50percent'>"
             +" <div class='wh90percent textleft left'>"
               +" <span class='opensans size13'><b>Adult</b></span>"
                +"<select class='form-control mySelectBoxClass' name='adults"+i+"'>"
                 +"<option>1</option>"
                  +"<option selected>2</option>"
                  +"<option>3</option>"
                  +"<option>4</option>"
                +"</select>"
              +"</div>"
            +"</div>"              
            +"<div class='w50percentlast'>"
              +"<div class='wh90percent textleft right'>"
              +"<span class='opensans size13'><b>Child</b></span>"
                +"<select class='form-control mySelectBoxClass child_act' name='childs"+i+"'>"
                  +"<option selected>0</option>"
                  +"<option>1</option>"
                 +" <option>2</option>"
                +"</select>"
              +"</div>"
            +"</div>"
          +"</div>"
            +"<div class='wh90percent textleft right'>"
            +"<div class='w50percent child1 none'>"
             +" <div class='wh90percent textleft left'>"
               +" <span class='opensans size13'><b>Child 1</b></span>"
                +"<select class='form-control mySelectBoxClass' name='childage1_"+i+"'>"
                  +"<option>1</option>"
                  +"<option>2</option>"
                  +"<option>3</option>"
                  +"<option>4</option>"
                  +"<option>5</option>"
                  +"<option>6</option>"
                  +"<option>7</option>"
                  +"<option>8</option>"
                  +"<option>9</option>"
                 +" <option>10</option>"
                  +"<option>11</option>"
                 +" <option>12</option>  "                            
               +" </select>"
              +"</div>"
            +"</div>   "           
            +"<div class='w50percentlast child2 none'>"
              +"<div class='wh90percent textleft right'>"
              +"<span class='opensans size13'><b>Child 2</b></span>"
                +"<select class='form-control mySelectBoxClass' name='childage2_"+i+"'>"
                  +"<option>1</option>"
                  +"<option>2</option>"
                  +"<option>3</option>"
                  +"<option>4</option>"
                  +"<option>5</option>"
                  +"<option>6</option>"
                  +"<option>7</option>"
                  +"<option>8</option>"
                  +"<option>9</option>"
                  +"<option>10</option>"
                  +"<option>11</option>"
                  +"<option>12</option>"
                +"</select>"
              +"</div>"
            +"</div>"
          +" </div>"
        +" </div>"
          +"<span class='orange remove_field'>Delete</span><div class='clearfix'></div><br/>   "   
       +"</div>");
}
    });
$(add_room).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parents('.rooms').remove(); i--;
    });
$('#searchBtn').click(function(){ 
    if($('.typeahead').val() == '') {
        $('.error_mgs_city').show();
        return false;
    }
    else if($('.startdate').val() == ''){
        $('.error_mgs_start_date').show();
        return false;
    }
    else if($('.enddate').val() == ''){
        $('.error_mgs_end_date').show();
        return false;
    }
    else if($('.adults').val() == ''){
        $('.error_mgs_adult').show();
        return false;
    }
    else if($('.child').val() == ''){
        $('.error_mgs_child').show();
        return false;
    }
    else if($('.child_age_1').val() == ''){
        $('.error_mgs_child_age1').show();
        return false;
    }
    else if($('.child_age_2').val() == ''){
        $('.error_mgs_child_age2').show();
        return false;
    }
    else{
        return true;
    }
});
$('#searchbus_return').click(function(){

            if($('.return').val() == '') {
                
                $('.error').show();
                return false;
              }    
            else{
                return true;
             }
             if($('.source').val() == '') {
                $('.error').show();
                return false;
              }  
              else{
                return true;
             }   
             if($('.destination').val() == '') {
                $('.error').show();
                return false;
              }  
              else{
                return true;
             }
             if($('.depart').val() == '') {
                $('.error').show();
                return false;
              }  
              else{
                return true;
             }
});



    });	
	
