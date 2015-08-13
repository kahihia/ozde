"use strict";


$(function() {    
    $( "#filterkeywordtxt" ).autocomplete({
    source: function (request, response) {
        $.getJSON("/getcity?term=" + request.term, function (data) {             
            response($.map(data, function (value, key) {                            
                return {
                    label: value.label,
                    value: value.value,
                    extra: value.cityid
                };
            }));
        });
    },
    select : function(event, ui) {
            // $('#filterkeywordtxt').val(ui.item.label);
            $('#filterkeyword').val(ui.item.extra);                
    },
    minLength: 2,
    delay: 100
    });
});


$('ul.slimmenu').slimmenu({
    resizeWidth: '992',
    collapserTitle: 'Main Menu',
    animSpeed: 250,
    indentChildren: true,
    childrenIndenter: ''
});


// Countdown
$('.countdown').each(function() {
    var count = $(this);
    $(this).countdown({
        zeroCallback: function(options) {
            var newDate = new Date(),
                newDate = newDate.setHours(newDate.getHours() + 130);

            $(count).attr("data-countdown", newDate);
            $(count).countdown({
                unixFormat: true
            });
        }
    });
});


$('.btn').button();

$("[rel='tooltip']").tooltip();

$('.form-group').each(function() {
    var self = $(this),
        input = self.find('input');

    input.focus(function() {
        self.addClass('form-group-focus');
    })

    input.blur(function() {
        if (input.val()) {
            self.addClass('form-group-filled');
        } else {
            self.removeClass('form-group-filled');
        }
        self.removeClass('form-group-focus');
    });
});

// $('.typeahead').typeahead({
//     hint: true,
//     highlight: true,
//     minLength: 3,
//     limit: 8,
// }, {
//     source: function(q, cb) {
//         return $.ajax({
//             dataType: 'json',
//             type: 'get',
//             url: '/getcity/',
//             chache: false,
//             success: function(data) {
//                 var result = [];                 
//                 $.each(data, function(index, val) {
//                     result.push({
//                         value: cityname
//                     });
//                 });
//                 cb(result);
//             }
//         });
//     }
// });


$('input.date-pick, .input-daterange, .date-pick-inline').datepicker({
    todayHighlight: true,
    format: 'yyyy/mm/dd'
});



$('input.date-pick, .input-daterange input[name="start"]').datepicker('setDate', 'today');
$('.input-daterange input[name="end"]').datepicker('setDate', '+7d');

$('input.time-pick').timepicker({
    minuteStep: 15,
    showInpunts: false
})

$('input.date-pick-years').datepicker({
    startView: 2
});




$('.booking-item-price-calc .checkbox label').click(function() {
    var checkbox = $(this).find('input'),
        // checked = $(checkboxDiv).hasClass('checked'),
        checked = $(checkbox).prop('checked'),
        price = parseInt($(this).find('span.pull-right').html().replace('$', '')),
        eqPrice = $('#car-equipment-total'),
        tPrice = $('#car-total'),
        eqPriceInt = parseInt(eqPrice.attr('data-value')),
        tPriceInt = parseInt(tPrice.attr('data-value')),
        value,
        animateInt = function(val, el, plus) {
            value = function() {
                if (plus) {
                    return el.attr('data-value', val + price);
                } else {
                    return el.attr('data-value', val - price);
                }
            };
            return $({
                val: val
            }).animate({
                val: parseInt(value().attr('data-value'))
            }, {
                duration: 500,
                easing: 'swing',
                step: function() {
                    if (plus) {
                        el.text(Math.ceil(this.val));
                    } else {
                        el.text(Math.floor(this.val));
                    }
                }
            });
        };
    if (!checked) {
        animateInt(eqPriceInt, eqPrice, true);
        animateInt(tPriceInt, tPrice, true);
    } else {
        animateInt(eqPriceInt, eqPrice, false);
        animateInt(tPriceInt, tPrice, false);
    }
});


$('div.bg-parallax').each(function() {
    var $obj = $(this);
    if($(window).width() > 992 ){
        $(window).scroll(function() {
            var animSpeed;
            if ($obj.hasClass('bg-blur')) {
                animSpeed = 10;
            } else {
                animSpeed = 15;
            }
            var yPos = -($(window).scrollTop() / animSpeed);
            var bgpos = '50% ' + yPos + 'px';
            $obj.css('background-position', bgpos);

        });
    }
});



$(document).ready(
    function() {


    $(".cl_glry_hver_act> span").click(function(){
        $(this).siblings('div:visible').hide();
        $(this).next().fadeIn('fast');
        return false
        }, function(){
    });

    $(".cl_glry_hver_act> span").hover(function(){
        $(this).addClass('color_tab_mouseover');

        return false
        }, function(){
        $(this).removeClass('color_tab_mouseover');
    });

    $(".cl_glry_hver_act> span").click(function(){
        $('.view_glry_act> div').hide();
        $(this).addClass('color_tab_hover');
        $(this).siblings().removeClass('color_tab_hover');
        
    });
    
    
    $(".view_glry_act> span").hover(function(){ 
        $('.cl_glry_hver_act> div').hide(); 
        $(this).addClass('view_glallery_opacity');
        $(this).siblings().removeClass('view_glallery_opacity');
    });
    
    $(".view_glry_act> span").hover(function(){
        $(this).siblings('div:visible').hide();
    
        $(this).next().fadeIn('fast');
        return false
        }, function(){
    });
    
    $(".cl_glry_hver_act span").click(function () {
    //     $("li.cl_info_bg_act").effect("highlight", {color: 'grey'}, 3000);
    $("li.cl_info_bg_act").stop().css("background-color", "#ccc")
.animate({ backgroundColor: "#fff"}, 1000);
    });        
   
  
        // jQuery.support.cors = true;
         var username = 'apitesting@goibibo.com';
         var password = 'test123';   

        function make_base_auth(user, password) {
            var tok = user + ':' + password;
            var hash = btoa(tok);
            alert('her');
            return "Basic " + hash;
        }        

         // $.ajax({
         //     type: "GET",
         //     url: "/getcity/",
         //     dataType: 'json',
         //     contentType: "application/json",            
         //     beforeSend: function (xhr){ 
         //         xhr.setRequestHeader('Access-Control-Allow-Origin','*');
         //         // xhr.setRequestHeader('Authorization', make_base_auth(username, password)); 
         //     },
         //    success: function(json) {
         //         console.log(json);
         //     },
         //    error: function(e) {
         //        console.log(e.message);
         //     },           
         //    complete: function(response) {                   
         //         console.log( "JSON Data: " + JSON.stringify(response.data));
         //    }
            
         // });        
     



    $('html').niceScroll({
        cursorcolor: "#000",
        cursorborder: "0px solid #fff",
        railpadding: {
            top: 0,
            right: 0,
            left: 0,
            bottom: 0
        },
        cursorwidth: "10px",
        cursorborderradius: "0px",
        cursoropacitymin: 0.2,
        cursoropacitymax: 0.8,
        boxzoom: true,
        horizrailenabled: false,
        zindex: 9999
    });


        // Owl Carousel
        var owlCarousel = $('#owl-carousel'),
            owlItems = owlCarousel.attr('data-items'),
            owlCarouselSlider = $('#owl-carousel-slider'),
            owlNav = owlCarouselSlider.attr('data-nav');
        // owlSliderPagination = owlCarouselSlider.attr('data-pagination');

        owlCarousel.owlCarousel({
            items: owlItems,
            navigation: true,
            navigationText: ['', '']
        });

        owlCarouselSlider.owlCarousel({
            slideSpeed: 300,
            paginationSpeed: 400,
            // pagination: owlSliderPagination,
            singleItem: true,
            navigation: true,
            navigationText: ['', ''],
            transitionStyle: 'fade',
            autoPlay: 4500
        });


    // footer always on bottom
    var docHeight = $(window).height();
   var footerHeight = $('#main-footer').height();
   var footerTop = $('#main-footer').position().top + footerHeight;
   
   if (footerTop < docHeight) {
    $('#main-footer').css('margin-top', (docHeight - footerTop) + 'px');
   }

  
   $(document).on('change', '.child_age_act', function() {     
          if($(this).val() == 0 ) {
               $(this).parent().siblings(".child-1-act").hide();
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
    });

    // var count = 0;
    // $(document).on('click', '.add_room_act', function() {
    //     // count++; 
    //     // $(".clone_add_room_act").clone().appendTo(".add_room_holder"); 
    //     // $(".clone_add_room_act").filter('[class]').each(function() { // For each new item with an ID
    //     //     this.class = this.class + '_' + count; // Append the counter to the ID
    //     // }); 

    //     // $(".clone_add_room_act").clone().attr('id', 'test' + (parseInt(/test(\d+)/.exec($(this).parent().parent().parent().find(".child-1-act").attr('id'))[1], 10)+1) ).appendTo('.add_room_holder')
    //     var html_1 = $(".clone_add_room_act").attr('id', 'test' + (parseInt(/test(\d+)/.exec($(this).parent().parent().parent().find(".child-1-act").attr('id'))[1], 10)+1) )
    //     $(".add_room_holder").append(html_1)
    // });

    // $(document).on('click', '.remove_room_act', function() {        
    //     $(this).closest(".clone_add_room_act").remove();
    //     e.preventDefault();   
    // });
   

}); 
// end of document ready

$('.nav-drop').dropit();


$("#price-slider").ionRangeSlider({
    min: 130,
    max: 575,
    type: 'double',
    prefix: "$",
    // maxPostfix: "+",
    prettify: false,
    hasGrid: true
});

$('.i-check, .i-radio').iCheck({
    checkboxClass: 'i-check',
    radioClass: 'i-radio'
});



$('.booking-item-review-expand').click(function(event) {
    console.log('baz');
    var parent = $(this).parent('.booking-item-review-content');
    if (parent.hasClass('expanded')) {
        parent.removeClass('expanded');
    } else {
        parent.addClass('expanded');
    }
});


$('.stats-list-select > li > .booking-item-rating-stars > li').each(function() {
    var list = $(this).parent(),
        listItems = list.children(),
        itemIndex = $(this).index();

    $(this).hover(function() {
        for (var i = 0; i < listItems.length; i++) {
            if (i <= itemIndex) {
                $(listItems[i]).addClass('hovered');
            } else {
                break;
            }
        };
        $(this).click(function() {
            for (var i = 0; i < listItems.length; i++) {
                if (i <= itemIndex) {
                    $(listItems[i]).addClass('selected');
                } else {
                    $(listItems[i]).removeClass('selected');
                }
            };
        });
    }, function() {
        listItems.removeClass('hovered');
    });
});



$('.booking-item-container').children('.booking-item').click(function(event) {
    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
        $(this).parent().removeClass('active');
    } else {
        $(this).addClass('active');
        $(this).parent().addClass('active');
        $(this).delay(1500).queue(function() {
            $(this).addClass('viewed')
        });
    }
});


// $('.form-group-cc-number input').payment('formatCardNumber');
// $('.form-group-cc-date input').payment('formatCardExpiry');
// $('.form-group-cc-cvc input').payment('formatCardCVC');




// if ($('#map-canvas').length) {
//     var map,
//         service;

//     jQuery(function($) {
//         $(document).ready(function() {
//             var latlng = new google.maps.LatLng(40.7564971, -73.9743277);
//             var myOptions = {
//                 zoom: 16,
//                 center: latlng,
//                 mapTypeId: google.maps.MapTypeId.ROADMAP,
//                 scrollwheel: false
//             };

//             map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);


//             var marker = new google.maps.Marker({
//                 position: latlng,
//                 map: map
//             });
//             marker.setMap(map);


//             $('a[href="#google-map-tab"]').on('shown.bs.tab', function(e) {
//                 google.maps.event.trigger(map, 'resize');
//                 map.setCenter(latlng);
//             });
//         });
//     });
// }


$('.card-select > li').click(function() {
    self = this;
    $(self).addClass('card-item-selected');
    $(self).siblings('li').removeClass('card-item-selected');
    $('.form-group-cc-number input').click(function() {
        $(self).removeClass('card-item-selected');
    });
});
// Lighbox gallery
$('#popup-gallery').each(function() {
    $(this).magnificPopup({
        delegate: 'a.popup-gallery-image',
        type: 'image',
        gallery: {
            enabled: true
        }
    });
});

// Lighbox image
$('.popup-image').magnificPopup({
    type: 'image'
});

// Lighbox text
$('.popup-text').magnificPopup({
    removalDelay: 500,
    closeBtnInside: true,
    callbacks: {
        beforeOpen: function() {
            this.st.mainClass = this.st.el.attr('data-effect');
        }
    },
    midClick: true
});

// Lightbox iframe
$('.popup-iframe').magnificPopup({
    dispableOn: 700,
    type: 'iframe',
    removalDelay: 160,
    mainClass: 'mfp-fade',
    preloader: false
});


$('.form-group-select-plus').each(function() {
    var self = $(this),
        btnGroup = self.find('.btn-group').first(),
        select = self.find('select');
    btnGroup.children('label').last().click(function() {
        btnGroup.addClass('hidden');
        select.removeClass('hidden');
    });
});
// Responsive videos
// $(document).ready(function() {
//     $("body").fitVids();
// });

// $(function($) {
//     $("#twitter").tweet({
//         username: "remtsoy", //!paste here your twitter username!
//         count: 3
//     });
// });

// $(function($) {
//     $("#twitter-ticker").tweet({
//         username: "remtsoy", //!paste here your twitter username!
//         page: 1,
//         count: 20
//     });
// });

// $(document).ready(function() {
//     var ul = $('#twitter-ticker').find(".tweet-list");
//     var ticker = function() {
//         setTimeout(function() {
//             ul.find('li:first').animate({
//                 marginTop: '-4.7em'
//             }, 850, function() {
//                 $(this).detach().appendTo(ul).removeAttr('style');
//             });
//             ticker();
//         }, 5000);
//     };
//     ticker();
// });
$(function() {
    $('#ri-grid').gridrotator({
        rows: 4,
        columns: 8,
        animType: 'random',
        animSpeed: 1200,
        interval: 1200,
        step: 'random',
        preventClick: false,
        maxStep: 2,
        w992: {
            rows: 5,
            columns: 4
        },
        w768: {
            rows: 6,
            columns: 3
        },
        w480: {
            rows: 8,
            columns: 3
        },
        w320: {
            rows: 5,
            columns: 4
        },
        w240: {
            rows: 6,
            columns: 4
        }
    });

});


$(function() {
    $('#ri-grid-no-animation').gridrotator({
        rows: 4,
        columns: 8,
        slideshow: false,
        w1024: {
            rows: 4,
            columns: 6
        },
        w768: {
            rows: 3,
            columns: 3
        },
        w480: {
            rows: 4,
            columns: 4
        },
        w320: {
            rows: 5,
            columns: 4
        },
        w240: {
            rows: 6,
            columns: 4
        }
    });

});

var tid = setInterval(tagline_vertical_slide, 2500);

// vertical slide
function tagline_vertical_slide() {
    var curr = $("#tagline ul li.active");
    curr.removeClass("active").addClass("vs-out");
    setTimeout(function() {
        curr.removeClass("vs-out");
    }, 500);

    var nextTag = curr.next('li');
    if (!nextTag.length) {
        nextTag = $("#tagline ul li").first();
    }
    nextTag.addClass("active");
}

function abortTimer() { // to be called when you want to stop the timer
    clearInterval(tid);
}

 // var regex = /^(.*)(\d)+$/i;
 //    var cloneIndex = $(".clonedInput").length;

 //    function clone(){
 //        alert(cloneIndex)
 //        $(this).parents(".clonedInput").clone()
 //            .appendTo(".add_room_holder")
 //            .attr("id", "clonedInput" +  cloneIndex)
 //            .find("*")
 //            .each(function() {
 //                var id = this.id || "";

 //                var match = id.match(regex) || [];
 //                if (match.length == 3) {
 //                    this.id = match[1] + (cloneIndex);

 //                }
 //            })
 //            .on('click', '.add_room_act', clone)
 //            .on('click', '.remove_room_act', remove);
 //        cloneIndex++;
 //    }
 //    function remove(){
 //        $(this).parents(".clonedInput").remove();
 //    }
 //    $(".add_room_act").on("click", clone);

 //    $(".remove_room_act").on("click", remove);
    
 var max_fields      = 4;
    var i = 1;
    var add_room = $('.add_room_holder');
    $('.add_room_act').click(function (e) {
        e.preventDefault();
        if(i < max_fields){
            i++;
    $(add_room).append("<div class='clonedInput' id='clonedInput0'><div class='col-md-3'><div class='form-group form-group-lg form-group-select-plus'><label>Rooms</label>"
        +"<input class='form-control hidden_input room_"+i+"' name='room"+i+"' type='text' value="+i+" readonly='readonly' />"
        +"</div></div><div class='col-md-2'><div class='form-group form-group-lg form-group-select-plus'>"
        +"<label>Adults</label><select class='form-control adults_"+i+"' name='adults"+i+"'>"
        +"<option selected='selected' value='0' >0</option><option value='1' >1</option><option value='2' >2</option><option value='3' >3</option><option value='4' >4</option>"
        +"</select></div></div><div class='col-md-2'><div class='form-group form-group-lg form-group-select-plus'>"
        +"<label>Children</label><select class='form-control child_age_act childs_"+i+"' name='childs"+i+"'><option selected='selected' value='0' >0</option>"
        +"<option value='1' >1</option><option value='2' >2</option></select></div></div>"
        +"<div class='col-md-2 child-1-act dn' id='test1'><div class='form-group form-group-lg form-group-select-plus'>"
        +"<label>Child-1 age</label><select class='form-control child1_"+i+"' name='childage1_"+i+"'>"
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
        +"</div>"
        +"</div>"
        +"<div class='col-md-2 child-2-act dn'>"
        +"<div class='form-group form-group-lg form-group-select-plus'>"
        +"<label>Child-2 age</label>"     
        +"<select class='form-control child2_"+i+"' name='childage2_"+i+"'>"
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
        +"</div>"
        +"</div>"
        +"<div class='col-md-1'>"
        +"<span class='remove remove_field'>Remove</span>"
        +"</div>");
}
    });
$(add_room).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parents('.clonedInput').remove(); i--;
    });


// hotels //
$('#searchBtn').click(function(){
        if($('.typeahead').val() == '') {
            // alert("enter the destination");
            $('.error_mgs').show();
            return false;
            if($('.startdate').val() == ''){
                $('.error_mgs').show();
                return false;
            if($('.enddate').val() == ''){
                $('.error_mgs').show();
                return false;
            if($('.child_age').val() == ''){
                $('.error_mgs').show();
            
            return false;
        }
    }
    }
    }
        else{
            return true;
        }

    });
$('#paynow').click(function(){
    if($('.fname').val() == ''){
            // alert("please enter the first name");
            $('.errormgs').show();
        if($('.lname').val() == ''){
            // alert("please enter the last name");
             $('.errormgs').show();
         if($('.mobileno').val() == ''){
            // alert("please enter the mobile number");
             $('.errormgs').show();
             if($('.email').val() == ''){
            // alert("please enter the email");
             $('.errormgs').show();
            return false;
                }
            }
         }
    }
    else{
       return true; 
    }
});

$('.map').click(function(){
    $('.google_map').toggle();
});

// bus//
$('#searchbus').click(function(){
        if($('.source').val() == '') {
            // alert("enter the destination");
            $('.error').show();
            if($('.destination').val() == '') {
               $('.error').show(); 
            return false;
        }
    }
        else{
            return true;
        }

    });

var nowTemp = new Date();
var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
 
var checkin = $('#dpd1').datepicker({
onRender: function(date) {
return date.valueOf() < now.valueOf() ? 'disabled' : '';
}
}).on('changeDate', function(ev) {
if (ev.date.valueOf() > checkout.date.valueOf()) {
var newDate = new Date(ev.date)
newDate.setDate(newDate.getDate() + 1);
checkout.setValue(newDate);
}
checkin.hide();
$('#dpd2')[0].focus();
}).data('datepicker');