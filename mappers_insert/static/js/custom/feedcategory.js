
$(document).ready(function(){
   /* Success popup show start */
   var params = new URLSearchParams(window.location.search);
   var success = params.get("success")
   var update = params.get("update")
   if (success || update) {
      $("#success-popup").modal("show")
      if(success){
         $("#success-message").text("Feed Category is created successfully..!")
      }
      else{
         $("#success-message").text("Feed Category is updated successfully..!")
      }
   }
   /* Success popup show end */
   $('#feed-category-table').DataTable({
      'columnDefs': [
         {
             "targets": 0, // your case first column
             "className": "text-center",
        },
        {
             "targets": 1,
             "className": "content-left",
        }
      ]
   })
})