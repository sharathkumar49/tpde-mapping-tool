$(document).ready(function () {
   var screen_type  = $("#screen_type").val()
   /* Success popup show start */
   var params = new URLSearchParams(window.location.search);
   var success = params.get("success")
   var update = params.get("update")
   if (success || update) {
      $("#success-popup").modal("show")
      if(success){
         $("#success-message").text("Feed is created successfully..!")
      }
      else{
         $("#success-message").text("Feed is updated successfully..!")
      }
   }
   /* Success popup show end */


   /* Adding pagination and searchables to table */
   $('#feed-table').DataTable({
      'columnDefs': [
         {
            "targets": 0, // first column 
            "className": "text-center",
         },
         {
            "targets": 1, // second column
            "className": "content-left",
         }
      ]
   })
   /* end */


   $("#submit-btn").click(function(){

   })


})