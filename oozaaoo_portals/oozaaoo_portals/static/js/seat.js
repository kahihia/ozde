"use strict";

$('input[name="seat"]').change(function() {
   var total_span = 0;
    $('input[name="seat"]').each(function() {
        if ($(this).is(':checked')) {
            total_span += parseInt($(this).prop('value'));
        }
    });
    $(".amount").html(total_span);
});
confirmbook/