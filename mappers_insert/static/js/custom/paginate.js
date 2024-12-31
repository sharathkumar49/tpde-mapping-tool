var Paginate = function(url) {
  this.init(url);
}

$.extend(Paginate.prototype, {
   url: '',
   first:'',
   last:'',
   previous:'',
   next:'',

   init: function(url) {
      this.widget_name = widget_name;


   },
   
   fetch_data: function(url){
      console.log(url)
   },

   doSomething: function() {
     console.log('my name is '+this.widget_name);
   }
});



// $(document).ready(function(){


//   var total_records = 100
//   var records_per_page = 1
//   var page_button_count = 4
//   var previous_url = ""
//   var next_url = ""
//   var first_url = ""
//   var last_url = ""

//   var total_pages = total_records / records_per_page
//   console.log("total pages", total_pages)
//   $('.pagination-container').append('<div class="row text-center py-2">\
//   <div class="col-4 mx-auto">\
//     <ul class="pagination pagination-primary m-4">\
//     </ul>\
//   </div>\
// </div>')

//   var first_button = '<li class="page-item">\
//   <a class="page-link" href="#" aria-label="Previous" data-id="first">\
//     <span aria-hidden="true"><i class="fa fa-angle-double-left" aria-hidden="true"></i></span>\
//   </a>\
// </li>'

//   var previous = '<li class="page-item">\
//   <a class="page-link" href="javascript:;" data-id="previous"><i class="fa fa-angle-left"></i></a>\
// </li>'

//   var next = '<li class="page-item">\
//       <a class="page-link" href="javascript:;" data-id="next"><i class="fa fa-angle-right"></i></a>\
//     </li>'
//   var last_button = '<li class="page-item">\
//   <a class="page-link" href="#" aria-label="Next" data-id="last">\
//     <span aria-hidden="true"><i class="fa fa-angle-double-right" aria-hidden="true"></i></span>\
//   </a>\
// </li>'
// var array_length = page_button_count
// if (total_pages < page_button_count)
// {
//     array_length = total_pages
// }
// console.log (array_length)
// var pageitems = ""
// var current_page = 1
// for(var i=1;i<=array_length;i++)
// {
//   if (i == current_page)
//   {
//     pageitems+='<li class="page-item active">\
//       <button class="page-link"  data-id="'+i+'">'+i+'</button>\
//     </li>'
//   }
//   else{
//     pageitems+='<li class="page-item">\
//       <button class="page-link"  data-id="'+i+'">'+i+'</button>\
//     </li>'
//   }
  
// }
// $('.pagination').append(first_button)
// $('.pagination').append(previous)
// $('.pagination').append(pageitems)
// $('.pagination').append(next)
// $('.pagination').append(last_button)



// $('.page-link').on('click', function(){
//   $('li.page-item.active').removeClass("active")
//   $($(this)[0].parentElement).addClass('active')
//   var page_choose = $(this).attr('data-id')
//   var url = (window.location.href).split('')
//   FetchData(url, page_choose)
// })

// })


// function create_pagination_array(current_page, first_button, ){

// }

// function FetchData(url, page_number, filter){
//     var response = ""
//     if(page_number && page_number > 0)
//     {
//       url = url+ "?page="+page_number
//     }
//     $.ajax({
//       url: url,
//       method: "GET",
//       type: "json",
//       async: false,
//       success: function(data){
//         console.log(data)
//         response = data
//       }
//     })
//     return response
//   }


// function create_pagination(){
//   $('.dt-end').html("")
//   $('.dt-end').html('<div class="row text-center py-2">\
//   <div class="col-4 mx-auto">\
//     <ul class="pagination pagination-primary m-4">\
//       <li class="page-item">\
//         <a class="page-link" href="javascript:;" aria-label="Previous">\
//           <span aria-hidden="true"><i class="fa fa-angle-double-left" aria-hidden="true"></i></span>\
//         </a>\
//       </li>\
//       <li class="page-item">\
//         <a class="page-link" href="javascript:;" aria-label="Next">\
//           <span aria-hidden="true"><i class="fa fa-angle-double-right" aria-hidden="true"></i></span>\
//         </a>\
//       </li>\
//     </ul>\
//   </div>\
// </div>')
// }