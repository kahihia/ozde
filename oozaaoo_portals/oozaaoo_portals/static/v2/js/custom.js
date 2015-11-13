"use strict";

//code by muthu ***move to intro.js***
// $('#oneway').click(function(){
//     $('#oneway').attr('checked',true);
//     $('#round').removeattr('checked');
// });

// $('#round').click(function(){
//     $('#round').attr('checked',true);
//     $('#oneway').removeattr('checked');
// });
//*************


$(window).scroll(function() {
  var test = jQuery(window).scrollTop();


if (test >= 504) {
  $('.hotel-details-rightside').addClass("on_scroll_pos");
}
else {
  $('.hotel-details-rightside').removeClass("on_scroll_pos");
}



 });

$('.datepicker').datepicker({
    format: 'yyyy/mm/dd',
    startDate: '-3d'
});



$('.slide').click(function(){
        var par = $(this).parent().parent().parent().parent().parent();
        $(".seatLayoutHolder").remove();
        $(par).find('.seat_map').slideDown("slow");
        //$(par).find('.seat_map').html("Loading");
        var pare = $(this).parent();
        var skey= $('input[name=skey]',pare).val();
        var arri_time= $('input[name=dept_time]',pare).val();
        var dept_time= $('input[name=arri_time]',pare).val();
        var skey= $('input[name=skey]',pare).val();
        var travels_name= $('input[name=travels]',pare).val();
        var route_type= $('input[name=route_type]',pare).val();
        var bus_type= $('input[name=bus_type]',pare).val();
        $(par).find("#wait").css("display", "block");
        $.ajax({
        type: 'POST',
        url: '/seat_v2/',
        dataType: 'html',
        data: {"skey":skey,"bus_type":bus_type,"route_type":route_type,"arri_time":arri_time,"dept_time":dept_time,"travels_name":travels_name}, // or JSON.stringify ({name: 'jonas'}),
        success: function(data) {

            $(par).find('.seat_map').html(data);
            $(par).find("#wait").css("display", "none");

        },
        //contentType: "application/json",

        });
    });
// code by priya ***move to intro js***

// $('.return_date').hide();

// $('input:radio[name=trip]').change(function() {
//     if (this.value == 'oneway') {
//         $('.return_date').hide();
//     }
//     else if (this.value == 'round') {
//         $('.return_date').show();
//     }
// });
// *************



function getCookie(name) {
    // alert("getCookie");
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i=0; i<cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // alert(cookie);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length+1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// $('.slide').click(function(){
//     var par = $(this).parent();
//     $('.seat_map',par).slideDown("slow");
//     var skey= $('input[name=skey]',par).val();
// $.ajax({
//           url: 'http://pp.goibibobusiness.com/api/bus/seatmap/',
//           type: 'GET',
//           data: {"skey":skey},
//           dataType: 'json',
//           success: function(data) {
//             $('.seat_map',par).html(data);
//             alert(JSON.stringify(data.data)); },
//           error: function() { alert('boo!'); },
//           contentType: "application/json",
//           beforeSend: setHeader
//         });
// });
//       function setHeader(xhr) {
//         xhr.setRequestHeader('authorization', 'Basic YXBpdGVzdGluZ0Bnb2liaWJvLmNvbTp0ZXN0MTIz');
//       }

$(function() {
    $("#filterkeywordtxt,#filter_bus,#filter_bus_des" ).autocomplete({
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

$(function() {
    $("#f_source" ).autocomplete({
    source: function (request, response) {
        $.getJSON("/iata_code?code=" + request.term, function (data) {
            response($.map(data, function (value, key) {
                return {
                    label: value.label,
                    value: value.value,
                    extra: value.citycode
                };
            }));
        });
    },
    select : function(event, ui) {
            $('#iata_code_source').val(ui.item.extra);
    },
    minLength: 2,
    delay: 100
    });
});

$(function() {
    $("#f_destination" ).autocomplete({
    source: function (request, response) {
        $.getJSON("/iata_code?code=" + request.term, function (data) {
            response($.map(data, function (value, key) {
                return {
                    label: value.label,
                    value: value.value,
                    extra: value.citycode
                };
            }));
        });
    },
    select : function(event, ui) {
            $('#iata_code_destination').val(ui.item.extra);
    },
    minLength: 2,
    delay: 100
    });
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


//$('.btn').button();

//$("[rel='tooltip']").tooltip();

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

// for date pic
  // $('input.date-pick, .input-daterange, .date-pick-inline, .mySelectCalendar2').datepicker({
 //       todayHighlight: true,
  // });


  // $('input.date-pick, .input-daterange input[name="start"],.input-daterange .depart').datepicker('setDate', 'today');

  // $('.input-daterange input[name="end"]','.input-daterange .return').datepicker('setDate', '+7d');

  // $('input.time-pick').timepicker({
 //     minuteStep: 15,
 //     showInpunts: false
  // });

  // $('input.date-pick-years').datepicker({
 //    startView: 2
  // });





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
      if($('.featured_list_find').text()==""){
        $('.featured_list_find').html("<h2>Sorry , No Result Found</h2>")
      }
  //   var mapCanvas = document.getElementById('map_canvas');

  //   var mapOptions = {
  //     center: new google.maps.LatLng(11.9421943409,79.8288596119 ),
  //     zoom: 8,
  //     mapTypeId: google.maps.MapTypeId.ROADMAP
  //   }

  //   // var map = new google.maps.Map(map_canvas, map_options);
  //   function initialize() {

  //   var mapCanvas = document.getElementById('map_canvas');

  //   var mapOptions = {
  //     center: new google.maps.LatLng(11.9421943409, 79.8288596119 ),
  //     zoom: 8,
  //     mapTypeId: google.maps.MapTypeId.ROADMAP
  //   }

  //   var map = new google.maps.Map(map_canvas, map_options);
  // }

    // default Value assigned //
    $('#selectedrpc').val($(this).find(':selected').data('rpc'));
    $('#selectedrtc').val($(this).find(':selected').data('rtc'));
    $('#mp').val($(this).find(':selected').data('mp'));
    $('#totalprice').val($(this).find(':selected').data('tp'));
    $('#totaltax').val($(this).find(':selected').data('ttc'));
    $('#totalprice_wt').val($(this).find(':selected').data('tp_alltax'));


    // $('.mp').html($('#mp').val());
    // $('.subtotal').html($('#totalprice').val());

    $('.mp').append($('#mp').val());
    $('.subtotal').html($('#totalprice').val());

    $('#roomname').val($(this).find(':selected').text());
    // $("#yourdropdownid option:selected").text();





    // OnChange the Value assigned //
    $('.selectroomtypes').change(function(){
      $('#selectedrpc').val($(this).find(':selected').data('rpc'));
      $('#selectedrtc').val($(this).find(':selected').data('rtc'));
      $('#mp').val($(this).find(':selected').data('mp'));
      $('#totalprice').val($(this).find(':selected').data('tp'));
      $('#totaltax').val($(this).find(':selected').data('ttc'));
      $('#totalprice_wt').val($(this).find(':selected').data('tp_alltax'));


    //   $('.mp').html($('#mp').val());

      $('.mp').text($('#mp').val());
      $('.subtotal').html($('#totalprice').val());
      $('#roomname').val($(this).find(':selected').text());
    })


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




   //  // footer always on bottom
   //  var docHeight = $(window).height();
   // var footerHeight = $('#main-footer').height();
   // var footerTop = $('#main-footer').position().top + footerHeight;

   // if (footerTop < docHeight) {
   //  $('#main-footer').css('margin-top', (docHeight - footerTop) + 'px');
   // }


   // $(document).on('change', '.child_age_act', function() {
   //        if($(this).val() == 0 ) {
   //             $(this).parent().siblings(".child-1-act").hide();
   //             $(this).parent().parent().siblings(".child-2-act").hide();
   //       }

   //       if($(this).val() == 1 ) {
   //             $(this).parent().parent().siblings(".child-1-act").show();
   //             $(this).parent().parent().siblings(".child-2-act").hide();
   //       }
   //       if($(this).val() == 2 ) {
   //             $(this).parent().parent().siblings(".child-1-act").show();
   //             $(this).parent().parent().siblings(".child-2-act").show();
   //       }
   //       if($(this).val() == 3 ) {
   //             $(this).parent().parent().siblings(".child-1-act").show();
   //             $(this).parent().parent().siblings(".child-2-act").show();
   //       }
   //  });

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


    /************************ Hotel Sort ********************/
    var $divs = $("form.sorthotellist");
    $('#sprice').on('click', function () {
      var alphabeticallyOrderedDivs = $divs.sort(function (a, b) {
        return $(a).find(".sort_price").text() > $(b).find(".sort_price").text();
      });
      $("#price > .hotel-list-vertical").html(alphabeticallyOrderedDivs);
    });

    $('#sstar').on('click', function () {
      var numericallyOrderedDivs = $divs.sort(function (a, b) {
        return $(a).find(".sort_star").text() > $(b).find(".sort_star").text();
      });
      $("#stars > .hotel-list-vertical").html(numericallyOrderedDivs);
    });

    $('#sratings').on('click', function () {
      var numericallyOrderedDivs = $divs.sort(function (a, b) {
        return $(a).find(".text-muted").text() > $(b).find(".text-muted").text();
      });
      $("#rating > .hotel-list-vertical").html(numericallyOrderedDivs);
    });

    $('#srecommended').on('click', function () {
      var numericallyOrderedDivs = $divs.sort(function (a, b) {
        return $(a).find(".sort_recommended").text() > $(b).find(".sort_recommended").text();
      });
      $("#recommended > .hotel-list-vertical").html(numericallyOrderedDivs);
    });

    // Custom Tooltip for Hotelsearch list Page
    $('.custom_tooltip').tipsy({gravity: 'n'});
      $('.custom_tooltip').click(function(){
        $('.custom_tooltip').addClass("menu_active")
    });

});
// end of document ready



// $("#price-slider").ionRangeSlider({
//     min: 130,
//     max: 575,
//     type: 'double',
//     prefix: "$",
//     // maxPostfix: "+",
//     prettify: false,
//     hasGrid: true
// });

// $( "#slider-range" ).slider({       ********replacing filter.js.********
//       range: true,
//       min: 1000,
//       max: 10000,
//       values: [ 1000, 10000 ],
//       slide: function( event, ui ) {
//         $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
//         $( "#amount_min" ).val(ui.values[ 0 ]);
//         $( "#amount_max" ).val(ui.values[ 1 ]);
//         var stars=($('input[name="star[]"]:checked').map(function() { return this.value; }).get().join(', ')) ;
//         if (stars==''){
//             var star=[5,4,3,2,1];
//         }
//         else{
//             var star=stars;
//         }
//         var location=($('input[name="location[]"]:checked').map(function() { return this.value; }).get().join(', '));

//         $.ajax({
//             type: 'POST',
//             url:'/get_results_by_price/',
//             data:"get=1&val_min="+ui.values[ 0 ]+"&val_max="+ui.values[ 1 ]+"&star="+star+"&location="+location,
//             success: function(data){
//             // alert(data);
//             var res = eval("("+data+")");
//             var elements = "<li>";
//             // alert("elements1" +elements);
//             jQuery.each(res, function(i,val) {
//                 // alert(i+"--"+JSON.stringify(val.hotelname));
//                 // $("#description").append("<tr onmouseover=\"this.style.backgroundColor='#ffff66';\" onmouseout=\"this.style.backgroundColor='#d4e3e5';\"><td>"+val+"</td></tr>");

//         // if (val.ibp){
//                     elements += "<form id='hoteldetails' method='POST' action ='/gethoteldetails/' name='hoteldetails'>\
//                     <input type='hidden' value=" + getCookie('csrftoken') + " " + "name='csrfmiddlewaretoken'>\
//                     <a class='booking-item' href='#'>\
//                                 <div class='row'>\
//                                     <div class='col-md-3'>\
//                                         <div class='booking-item-img-wrap'>\
//                                             <img src=" + val.hotelimage + " alt='Image Alternative text' title='LHOTEL PORTO BAY SAO PAULO suite lhotel living room' />\
//                                             <div class='booking-item-img-num'>\
//                                             <i class='fa fa-picture-o'></i>\
//                                             29\
//                                             </div>\
//                                         </div>\
//                                     </div>\
//                                     <div class='col-md-6'>\
//                                         <div class='booking-item-rating'>\
//                                             <span class='booking-item-rating-number'><b >";
//                     // alert("elements2" +elements);
//                     if (val.hotelrating == 1){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                         // alert("elements3" +elements);
//                     }
//                     else if (val.hotelrating == 2){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements4" +elements);
//                     }
//                     else if (val.hotelrating == 3){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements5" +elements);
//                     }
//                     else if (val.hotelrating == 4){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements6" +elements);
//                     }
//                     else if (val.hotelrating == 5){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements7" +elements);
//                     }
//                     elements+="</b></span>\
//                                 </div>\
//                                 <h5 class='booking-item-title'>" + val.hotelname + "</h5>\
//                                 <p class='booking-item-address'><i class='fa fa-map-marker'></i>" + val.location + "</p>\
//                                 <small class='booking-item-last-booked'> </small>\
//                                 </div>\
//                                 <div class='col-md-3'>\
//                                         <span class='booking-item-price-from'>from</span>\
//                                         <span class='booking-item-price'>&#8377;" + parseFloat(val.price) + "</span>\
//                                         <span>/night</span>\
//                                         <input type='submit' name='moredetails' value='MoreDetails' class='btn btn-primary' id='more'/>\
//                                         <p>" + val.goibiborating + "/5 Reviews</p>\
//                                     </div>\
//                                 </div>\
//                             </a>\
//                         </form>";
//                         // alert("elements8" +elements);
//                // }
//             });
//             elements += "</li>";
//             // alert("elements9" +elements);
//             $(".hotel-list-vertical").html(elements);
//             }
//         });
// }
// });
// $( '.star' ).click(
//     function( ) {
//         var amount_min= $( "#amount_min" ).val();
//         var amount_max= $( "#amount_max" ).val();
//         var star=($('input[name="star[]"]:checked').map(function() { return this.value; }).get().join(', '))== null ? '5' :($('input[name="star[]"]:checked').map(function() { return this.value; }).get().join(', '));
//         var location=($('input[name="location[]"]:checked').map(function() { return this.value; }).get().join(', '));
//         $.ajax({
//             type: 'POST',
//             url:'/get_results_by_price/',
//             data:"get=1&val_min="+amount_min+"&val_max="+amount_max+"&star="+star+"&location="+location,
//             success: function(data){
//             // alert(data);
//             var res = eval("("+data+")");
//             var elements = "<li>";
//             // alert("elements1" +elements);
//             jQuery.each(res, function(i,val) {
//                 // alert(i+"--"+JSON.stringify(val.hotelname));
//                 // $("#description").append("<tr onmouseover=\"this.style.backgroundColor='#ffff66';\" onmouseout=\"this.style.backgroundColor='#d4e3e5';\"><td>"+val+"</td></tr>");

//             if (val.ibp){
//                     elements += "<form id='hoteldetails' method='POST' action ='/gethoteldetails/' name='hoteldetails'>\
//                     <input type='hidden' value=" + getCookie('csrftoken') + " " + "name='csrfmiddlewaretoken'>\
//                     <a class='booking-item' href='#'>\
//                                 <div class='row'>\
//                                     <div class='col-md-3'>\
//                                         <div class='booking-item-img-wrap'>\
//                                             <img src=" + val.hotelimage + " alt='Image Alternative text' title='LHOTEL PORTO BAY SAO PAULO suite lhotel living room' />\
//                                             <div class='booking-item-img-num'>\
//                                             <i class='fa fa-picture-o'></i>\
//                                             29\
//                                             </div>\
//                                         </div>\
//                                     </div>\
//                                     <div class='col-md-6'>\
//                                         <div class='booking-item-rating'>\
//                                             <span class='booking-item-rating-number'><b >";
//                     // alert("elements2" +elements);
//                     if (val.hotelrating == 1){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                         // alert("elements3" +elements);
//                     }
//                     else if (val.hotelrating == 2){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements4" +elements);
//                     }
//                     else if (val.hotelrating == 3){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements5" +elements);
//                     }
//                     else if (val.hotelrating == 4){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements6" +elements);
//                     }
//                     else if (val.hotelrating == 5){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements7" +elements);
//                     }
//                     elements+="</b></span>\
//                                 </div>\
//                                 <h5 class='booking-item-title'>" + val.hotelname + "</h5>\
//                                 <p class='booking-item-address'><i class='fa fa-map-marker'></i>" + val.location + "</p>\
//                                 <small class='booking-item-last-booked'> </small>\
//                                 </div>\
//                                 <div class='col-md-3'>\
//                                         <span class='booking-item-price-from'>from</span>\
//                                         <span class='booking-item-price'>&#8377;" + parseFloat(val.price) + "</span>\
//                                         <span>/night</span>\
//                                         <input type='submit' name='moredetails' value='MoreDetails' class='btn btn-primary' id='more'/>\
//                                         <p>" + val.goibiborating + "/5 Reviews</p>\
//                                     </div>\
//                                 </div>\
//                             </a>\
//                         </form>";
//                         // alert("elements8" +elements);
//              }
//             });
//             elements += "</li>";
//             // alert("elements9" +elements);
//             $(".booking-list").html(elements);
//             }
//         });

// });
// $( '.location' ).click(
//     function( ) {
//         var amount_min= $( "#amount_min" ).val();
//         var amount_max= $( "#amount_max" ).val();
//         var stars=($('input[name="star[]"]:checked').map(function() { return this.value; }).get().join(', ')) ;
//         if (stars==''){
//             var star=[5,4,3,2,1];
//         }
//         else{
//             var star=stars;
//         }
//         var location=($('input[name="location[]"]:checked').map(function() { return this.value; }).get().join(', '));
//         $.ajax({
//             type: 'POST',
//             url:'/get_results_by_price/',
//             data:"get=1&val_min="+amount_min+"&val_max="+amount_max+"&star="+star+"&location="+location,
//             success: function(data){
//             // alert(data);
//             var res = eval("("+data+")");
//             var elements = "<li>";
//             // alert("elements1" +elements);
//             jQuery.each(res, function(i,val) {
//                 // alert(i+"--"+JSON.stringify(val.hotelname));
//                 // $("#description").append("<tr onmouseover=\"this.style.backgroundColor='#ffff66';\" onmouseout=\"this.style.backgroundColor='#d4e3e5';\"><td>"+val+"</td></tr>");

//             if (val.ibp){
//                     elements += "<form id='hoteldetails' method='POST' action ='/gethoteldetails/' name='hoteldetails'>\
//                     <input type='hidden' value=" + getCookie('csrftoken') + " " + "name='csrfmiddlewaretoken'>\
//                     <a class='booking-item' href='#'>\
//                                 <div class='row'>\
//                                     <div class='col-md-3'>\
//                                         <div class='booking-item-img-wrap'>\
//                                             <img src=" + val.hotelimage + " alt='Image Alternative text' title='LHOTEL PORTO BAY SAO PAULO suite lhotel living room' />\
//                                             <div class='booking-item-img-num'>\
//                                             <i class='fa fa-picture-o'></i>\
//                                             29\
//                                             </div>\
//                                         </div>\
//                                     </div>\
//                                     <div class='col-md-6'>\
//                                         <div class='booking-item-rating'>\
//                                             <span class='booking-item-rating-number'><b >";
//                     // alert("elements2" +elements);
//                     if (val.hotelrating == 1){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                         // alert("elements3" +elements);
//                     }
//                     else if (val.hotelrating == 2){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements4" +elements);
//                     }
//                     else if (val.hotelrating == 3){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements5" +elements);
//                     }
//                     else if (val.hotelrating == 4){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements6" +elements);
//                     }
//                     else if (val.hotelrating == 5){
//                         elements+= "<i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>\
//                                     <i class='fa fa-star icon-group booking-item-rating-stars'></i>";
//                          // alert("elements7" +elements);
//                     }
//                     elements+="</b></span>\
//                                 </div>\
//                                 <h5 class='booking-item-title'>" + val.hotelname + "</h5>\
//                                 <p class='booking-item-address'><i class='fa fa-map-marker'></i>" + val.location + "</p>\
//                                 <small class='booking-item-last-booked'> </small>\
//                                 </div>\
//                                 <div class='col-md-3'>\
//                                         <span class='booking-item-price-from'>from</span>\
//                                         <span class='booking-item-price'>&#8377;" + parseFloat(val.price) + "</span>\
//                                         <span>/night</span>\
//                                         <input type='submit' name='moredetails' value='MoreDetails' class='btn btn-primary' id='more'/>\
//                                         <p>" + val.goibiborating + "/5 Reviews</p>\
//                                     </div>\
//                                 </div>\
//                             </a>\
//                         </form>";
//                         // alert("elements8" +elements);
//                 }
//             });
//             elements += "</li>";
//             // alert("elements9" +elements);
//             $(".booking-list").html(elements);
//             }
//         });

// });

// $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
// " - $" + $( "#slider-range" ).slider( "values", 1 ) );

// var val_min = $( "#slider-range" ).slider( "values", 0 );
// // alert(val_min);
// var val_max = $( "#slider-range" ).slider( "values", 1 );
// // alert(val_max);
// $.ajax({
//     type: 'POST',
//     url:"/get_results_by_price/",
//     data:"get=1&val_min="+val_min+"&val_max="+val_max,
//     success: function(data){
//     var res = eval("("+data+")");
//     $("#description").empty();
//     jQuery.each(res, function(i,val) {//alert(i+"--"+val);
//         $("#description").append("<tr onmouseover=\"this.style.backgroundColor='#ffff66';\" onmouseout=\"this.style.backgroundColor='#d4e3e5';\"><td>"+val+"</td></tr>");
//     });
// }
// });

$('.travele').click(function(){
  $('.need_round').hide();
  var tra=$(this).text();
  $('.need_round:contains("'+tra+'")').show();
});
$('.bustype_sort').click(function(){
  $('.need_round').hide();
  var bus_type=$(this).text();
  $('.need_round:contains("'+bus_type+'")').show();
});
$('.bpoint').click(function(){
  $('.need_round').hide();
  var bpoint=$(this).text();
  $('.need_round:contains("'+bpoint+'")').show();
});
$('.dpoint').click(function(){
  $('.need_round').hide();
  var dpoint=$(this).text();
  $('.need_round:contains("'+dpoint+'")').show();
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




if ($('#map-canvas').length) {
    var map,
        service;

    jQuery(function($) {
        $(document).ready(function() {
            var latlng = new google.maps.LatLng(11.9421943409, 79.8288596119);
            // alert( $.cookie("la") );

            // var latlng = new google.maps.LatLng(request.COOKIES.la, request.COOKIES.lo);
            var myOptions = {
                zoom: 8,
                center: latlng,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                scrollwheel: false
            };

            map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);


            var marker = new google.maps.Marker({
                position: latlng,
                map: map
            });
            marker.setMap(map);


            $('a[href="#google-map-tab"]').on('shown.bs.tab', function(e) {
                google.maps.event.trigger(map, 'resize');
                map.setCenter(latlng);
            });
        });
    });
}


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


$('.form-group-select-plus').each(function() {
    var self = $(this),
        btnGroup = self.find('.btn-group').first(),
        select = self.find('select');
    btnGroup.children('label').last().click(function() {
        btnGroup.addClass('hidden');
        select.removeClass('hidden');
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
//    var max_fields= 4;
// var i = 1;
// var add_room = $('.add_room_holder');
// $('.add_room_act').click(function (e) {
//     e.preventDefault();
//     if(i < max_fields){
//         i++;
// $(add_room).append("<div class='room"+i+" rooms' >"
//         +"<div class='w50percent'>"
//           +"<div class='wh90percent textleft'>"
//             +"<span class='opensans size13'><b>ROOM "+i+"</b></span><br/>"
//             +"<input class='form-control hidden_input' name='room"+i+"' type='hidden' value='"+i+"' readonly='readonly' /> "
//           +"</div>"
//         +"</div>"

//         +"<div class='w50percentlast'>"
//           +"<div class='wh90percent textleft right'>"
//            +"<div class='w50percent'>"
//              +" <div class='wh90percent textleft left'>"
//                +" <span class='opensans size13'><b>Adult</b></span>"
//                 +"<select class='form-control mySelectBoxClass' name='adults"+i+"'>"
//                  +"<option>1</option>"
//                   +"<option selected>2</option>"
//                   +"<option>3</option>"
//                   +"<option>4</option>"
//                 +"</select>"
//               +"</div>"
//             +"</div>"
//             +"<div class='w50percentlast'>"
//               +"<div class='wh90percent textleft right'>"
//               +"<span class='opensans size13'><b>Child</b></span>"
//                 +"<select class='form-control mySelectBoxClass child_act' name='childs"+i+"'>"
//                   +"<option selected>0</option>"
//                   +"<option>1</option>"
//                  +" <option>2</option>"
//                 +"</select>"
//               +"</div>"
//             +"</div>"
//           +"</div>"
//             +"<div class='wh90percent textleft right'>"
//             +"<div class='w50percent child1 none'>"
//              +" <div class='wh90percent textleft left'>"
//                +" <span class='opensans size13'><b>Child 1</b></span>"
//                 +"<select class='form-control mySelectBoxClass' name='childage1_"+i+"'>"
//                   +"<option>1</option>"
//                   +"<option>2</option>"
//                   +"<option>3</option>"
//                   +"<option>4</option>"
//                   +"<option>5</option>"
//                   +"<option>6</option>"
//                   +"<option>7</option>"
//                   +"<option>8</option>"
//                   +"<option>9</option>"
//                  +" <option>10</option>"
//                   +"<option>11</option>"
//                  +" <option>12</option>  "
//                +" </select>"
//               +"</div>"
//             +"</div>   "
//             +"<div class='w50percentlast child2 none'>"
//               +"<div class='wh90percent textleft right'>"
//               +"<span class='opensans size13'><b>Child 2</b></span>"
//                 +"<select class='form-control mySelectBoxClass' name='childage2_"+i+"'>"
//                   +"<option>1</option>"
//                   +"<option>2</option>"
//                   +"<option>3</option>"
//                   +"<option>4</option>"
//                   +"<option>5</option>"
//                   +"<option>6</option>"
//                   +"<option>7</option>"
//                   +"<option>8</option>"
//                   +"<option>9</option>"
//                   +"<option>10</option>"
//                   +"<option>11</option>"
//                   +"<option>12</option>"
//                 +"</select>"
//               +"</div>"
//             +"</div>"
//           +" </div>"
//         +" </div>"
//           +"<span class='orange remove_field'>Delete</span><div class='clearfix'></div><br/>   "
//        +"</div>");
// }
//     });
// $(add_room).on("click",".remove_field", function(e){ //user click on remove text
//         e.preventDefault(); $(this).parents('.rooms').remove(); i--;
//     });
//  var max_fields= 4;
//     var i = 1;
//     var add_room = $('.add_room_holder');
//     $('.add_room_act').click(function (e) {
//         e.preventDefault();
//         if(i < max_fields){
//             i++;
//     $(add_room).append("<div class='clonedInput' id='clonedInput0'><div class='col-md-3'><div class='form-group form-group-lg form-group-select-plus'><label>Rooms</label>"
//         +"<input class='form-control hidden_input room_"+i+"' name='room"+i+"' type='text' value="+i+" readonly='readonly' />"
//         +"</div></div><div class='col-md-2'><div class='form-group form-group-lg form-group-select-plus'>"
//         +"<label>Adults</label><select class='form-control adults_"+i+"' name='adults"+i+"'>"
//         +"<option selected='selected' value='0' >0</option><option value='1' >1</option><option value='2' >2</option><option value='3' >3</option><option value='4' >4</option>"
//         +"</select></div></div><div class='col-md-2'><div class='form-group form-group-lg form-group-select-plus'>"
//         +"<label>Children</label><select class='form-control child_age_act childs_"+i+"' name='childs"+i+"'><option selected='selected' value='0' >0</option>"
//         +"<option value='1' >1</option><option value='2' >2</option></select></div></div>"
//         +"<div class='col-md-2 child-1-act dn' id='test1'><div class='form-group form-group-lg form-group-select-plus'>"
//         +"<label>Child-1 age</label><select class='form-control child1_"+i+"' name='childage1_"+i+"'>"
//         +"<option selected='selected' value='0' >0</option>"
//         +"<option value='1' >1</option>"
//         +"<option value='2' >2</option>"
//         +"<option value='3' >3</option>"
//         +"<option value='4' >4</option>"
//         +"<option value='5' >5</option>"
//         +"<option value='6' >6</option>"
//         +"<option value='7' >7</option>"
//         +"<option value='8' >8</option>"
//         +"<option value='9' >9</option>"
//         +"<option value='10' >10</option>"
//         +"<option value='11' >11</option>"
//         +"<option value='12' >12</option>"
//         +"</select>"
//         +"</div>"
//         +"</div>"
//         +"<div class='col-md-2 child-2-act dn'>"
//         +"<div class='form-group form-group-lg form-group-select-plus'>"
//         +"<label>Child-2 age</label>"
//         +"<select class='form-control child2_"+i+"' name='childage2_"+i+"'>"
//         +"<option selected='selected' value='0' >0</option>"
//         +"<option value='1' >1</option>"
//         +"<option value='2' >2</option>"
//         +"<option value='3' >3</option>"
//         +"<option value='4' >4</option>"
//         +"<option value='5' >5</option>"
//         +"<option value='6' >6</option>"
//         +"<option value='7' >7</option>"
//         +"<option value='8' >8</option>"
//         +"<option value='9' >9</option>"
//         +"<option value='10' >10</option>"
//         +"<option value='11' >11</option>"
//         +"<option value='12' >12</option>"
//         +"</select>"
//         +"</div>"
//         +"</div>"
//         +"<div class='col-md-1'>"
//         +"<span class='remove remove_field'>Remove</span>"
//         +"</div>");
// }
//     });


// code by priya move to into.js
// hotels //
// $('#searchBtn').click(function(){
//     if($('.typeahead').val() == '') {
//         // alert("enter the destination");
//         $('.error_mgs').show();
//         return false;
//         if($('.startdate').val() == ''){
//             $('.error_mgs').show();
//                 return false;
//             if($('.enddate').val() == ''){
//                 $('.error_mgs').show();
//                 return false;
//                 if($('.child_age').val() == ''){
//                     $('.error_mgs').show();
//                     return false;
//                 }
//             }
//         }
//     }
//     else{
//         return true;
//     }
// });
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

// $('#payment').on('click', function() {
//       // alert("enter");
//
//
//     if($('#fname').val() == ''){
//             // alert("please enter the last name");
//             $('.errormgs').show();
//           }
//     else{
//           $('.errormgs').hide();
//     }
//    if ($('.lname').val() == '') {
//              $('.errormgs1').show();
//     }
//   else{
//         $('.errormgs1').hide();
//     }
//   if ($('.age').val() == '') {
//              $('.errormgs2').show();
//    }
//   else{
//       $('.errormgs2').hide();
//     }
//   if ($('.mobileno').val() == '') {
//              $('.errormgs4').show();
//       }
//   else{
//       $('.errormgs4').hide();
//     }
//
//   if ($('.email').val() == '') {
//              $('.errormgs3').show();
//   }
//   else{
//       $('.errormgs3').hide();
//     }
//   $('.payment').show();
//
//
//   });



$('.login').click(function(){
    if($('input[name="username"]').val() == ''){
            // alert("please enter the first name");
            $('.errormgs').show();
            return false;
        if($('input[name="password"]').val() == ''){
            // alert("please enter the last name");
             $('.errormgs').show();
             return false;
         }
    }
    else{
       return true;
    }
});
//  var CheckinDate=new Date();
//  var CheckoutDate=new Date();
//  var diff=new Date();
//  $('#checkin').datepicker({
//        todayHighlight: true,
//        format: 'yyyy/mm/dd',
//        onSelect: function(dateText, inst) {
//        CheckinDate=datetext;
//     }
//     });

// $('#checkout').datepicker({
//    todayHighlight: true,
//    format: 'yyyy/mm/dd',
//    onSelect: function(dateText, inst) {
//    CheckoutDate=datetext;
//    diff=(CheckoutDate.getTime() - CheckinDate.getTime())/(1000*60*60*24);
// }
// });
// *********************
$('.temp').hide();
$('.temp_onward').hide();
$('.temp_return').hide();
$('.onward_book').click(function(){
    var par2=$(this).parents('li');
    var skey= $('input[name=travels]',par2).val();
    alert(skey);
});

//********* popup for cancel policy,refund,booking status,refund status hotel and bus**********//

$('.toggleModal').on('click', function (e) {

  $('.modal').show();
  $('.bus-payment ').hide();
});
$('.close').click(function(){
  $('.modal').hide();

  $('.bus-payment ').show();
})
$('.refund').click(function(){

  $('.modal_refund').show();
  $('.bus-payment ').hide();
});
$('.close_btn').click(function(){

  $('.modal_refund').hide();
  $('.bus-payment ').show();
});





$('#refund_hotel').click(function(){

  $('.modal_refundstatus').show();
  $('.bus-payment ').hide();
  $('.modal_refund').hide();
});

//******************end of popup******************//
//map for hotels//
$("#map_canvas").hide();
$(".map").click(function(){
  initialize();
  addMarker();
  $("#map_canvas").toggle();
});
// end map

  if($('.selectroomtypes option').length==0){

    $('.for_soldout').show();
    $('.for_buynow').hide();
  }


$(".change").click(function(){
  alert("enter");
  if($('input[name="password"]').val() == ''){
            // alert("please enter the last name");
             $('.mgs').show();
             return false;
         }

 });
//*********** for rating tab in hotel listing **********//

// var ascending = false;

// $('.tab-content').on('click','#sratings',function(){

//     var sorted = $('.results-row').sort(function(a,b){
//         return (ascending ==
//                (convertToNumber($(a).find('.rating').html()) <
//                 convertToNumber($(b).find('.rating').html()))) ? 1 : -1;
//     });
//     ascending = ascending ? false : true;

//     $('.results').html(sorted);
// });

// var convertToNumber = function(value){
//      return parseFloat(value.replace('$',''));
// }

//*******************Flights.........................//
//this is round trip form POST
$('.round_flight_act').click(function(){
    $('#round_trip_flight_form').submit();
});
//this is round trip form POST
$('.oneway_flight_act').click(function(){
    $('#oneway_flight_form').submit();
});
var nowDate = new Date();
var today = new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate(), 0, 0, 0, 0)
$( "#datepicker9" ).datepicker({
    format: 'dd/mm/yyyy',
    orientation: "bottom auto",
    autoclose: true,
});

$('.datepicker').datepicker({
    format: 'yyyy/mm/dd',
    startDate: '-3d'
});


 $(".login_circle1_hover, .login_circle2_hover, .login_circle3_hover").hide();

$(".login").click(function(){
    $(".login_circle1_hover").show();
});