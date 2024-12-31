
$(document).ready(function () {
    var screen_type = $("#screen_type").val()
    var status = $("#status").val()
    if(!status){status = 0}
    console.log(status)
    var params = new URLSearchParams(window.location.search);
    var success = params.get("success")
    var action = params.get("action")
    var update = params.get("update")
    console.log(success)
    if(success && update){
      $("#success-popup").modal("show")
      $("#success-message").text("Batch validated successfully..!")
    }
    
    else if(success){
        if(action)
        {
            $("#success-popup").modal("show")
            if(action == "approve")
            {
                $("#success-message").text("Batch is approved successfully..!")
            }
            else if(action == "reject"){
                $("#success-message").text("Batch is rejected successfully..!")
            }
            else if(action == "update"){
              $("#success-message").text("Batch is updated successfully..!")
          }
        }else{
            $("#success-popup").modal("show")
            $("#success-message").text("Batch created successfully..!")
        }
    }
    $('#batch-table').DataTable(
      {
        columnDefs: [
        {
            targets: 0,
            className: 'dt-body-center'
        }
      ]
      }
    );
    $('#batch_record_view').DataTable()
    if(screen_type == 'list_view'){
        console.log("inside list veiw")
      $('.dt-search > input').remove()
      $('.dt-search').append('<select type="search" class="dt-input" id="dt-search-0 search_filter" onchange="StatusFilter(this)" placeholder="" aria-controls="feed-table">\
        <option value="">--Search Filter--</option>\
        <option value="0">Waiting for Approval</option>\
        <option value="1">Approved</option>\
        <option value="2">Rejected</option>\
        </select>')
        $($('.dt-search')[0].lastElementChild).val(status)
    }
    
    $('.error-data').click(function(){
      $('#message-popup').modal('show')
    })

    $('#popup-close').click(function(){
      $('#message-popup').modal('hide')
      $('#reject-popup').modal('hide')
    })

    $('#reject').click(function(){
      $('#reject-popup').modal('show')
    })


    $('#validate-btn').on("click",function(e){
      action = 'validate'
      $("#confirm-popup").modal("show")
      $("#confirm-message").text("Are you sure. Do you want to validate the batch..!")
      
    })

    $('#approve-btn').on("click",function(e){
        action = "approve"
        $("#confirm-popup").modal("show")
        $("#confirm-message").text("Are you sure. Do you want to approve the batch..!")
    })

    $('#reject-btn').on("click",function(e){
        action = "reject"
        $('#reject-popup').modal("hide")
        $("#confirm-popup").modal("show")
        $("#confirm-message").text("Are you sure. Do you want to reject the batch..!")
    })

    $('#update-btn').on("click",function(e){
      action = "update"
      $("#confirm-popup").modal("show")
      $("#confirm-message").text("Are you sure. Do you want to update the batch..!")
  })

    $("#confirm-btn").on("click", function(){
        console.log(action)
        if (action == "approve"){
            $("#approve-form").submit()
        }
        else if(action == "reject"){
            $("#reject-confirm-form").submit()
        }
        else if(action == 'update'){
          $("#update-form").submit()
        }
        else if(action == 'validate'){
          $.blockUI({
            message: '<div class="page-content page-container" id="page-content"><div class="padding" style="background-color:unset!important"><div class="row container d-flex justify-content-center"><div class="loader-demo-box"><div class="bar-loader"><span></span><span></span><span></span><span></span></div></div></div></div></div>' });
            console.log(action)
          $("#validate-form").submit()
        }
        $("#confirm-popup").modal("hide")
    })
  })


  function DetailView(mappers_obj) {
    console.log($(mappers_obj).attr("data-url"))
    var url = $(mappers_obj).attr("data-url")
    var validation_type = $('#validation_type').val()
    var csrf_token = getCookie("csrftoken")
    var anchor_tag = $(document.createElement('a')).prop({
      href: $(mappers_obj).attr("data-url"),
      innerText: 'Techie Delight'
    })
    // $.ajax({
    //   url : url,
    //   method: "POST",
    //   data: {'validation_type': validation_type, 'csrfmiddlewaretoken': csrf_token},
    //   success: function(data){
    //     console.log('success')
    //   },
    //   error: function(error){
    //     console.log('error')
    //   }
    // })
    console.log(anchor_tag)
    window.location = anchor_tag[0].href

  }

  function StatusFilter(statusobj){
      $("#status_value").val(statusobj.value)
      $('#status_filter_form').submit()
  }