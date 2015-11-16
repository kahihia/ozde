jQuery(document).ready(function($) {
  
  $('#price_filter').val('1000-9999');
  $("#price_slider").slider({
    range:true,
    min: 1000,
    max: 9999,
    values:[1000, 9999],
    step: 5,
    slide: function(event, ui) {
      $(".price_range_label_min").html('Rs. ' + ui.values[ 0 ]);
      $(".price_range_label_max").html('Rs. ' + ui.values[ 1 ]);

      $('#price_filter').val(ui.values[0] + '-' + ui.values[1]).trigger('change');
    }
  });

  //$('#starcount :checkbox').prop('checked', true);

  FilterJS(services, "#service_list", {
    template: '#template',
    criterias:[
      {field: 'amount', ele: '#price_filter', type: 'range'},
      {field: 'starcount', ele: '#starcount :checkbox'},
      {field: 'location', ele: '#location :checkbox'},
      {field: 'status', ele: '#status :checkbox'}
    ],
    search: { ele: '#search_box' }
  });

});
