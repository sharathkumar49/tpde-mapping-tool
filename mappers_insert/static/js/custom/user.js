$(document).ready(function(){
    console.log("user")
    var valid = true
    $('input[name="email"]').on("blur", function(){
        var email = this.value
        if(email)
        {
            var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            if(!regex.test(email)){

            }
        }
    })

    $('.success-confirm').click(function(){
        window.location.href = "/masters/user/list/"
    })

    $("#user-create").on("submit", function(e){
        e.preventDefault();
        console.log("submit")
        var password = $("input[name='password']").val()
        var confirm_password = $("input[name='confirm_password']").val()
        var email = this.value
        if(email)
        {
            var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            console.log(regex.test(email))
            if(!regex.test(email)){
                $("#warning-popup").modal("show")
                $("#warning-message").text("Please enter valid email ID..!")
                valid=false
            }
        }
        if (password != confirm_password)
        {
            $("#warning-popup").modal("show")
            $("#warning-message").text("Password and Confirm password should be same..!")
            valid=false
        }
        

        if(valid){
            var formActionUrl = $('#user-create').attr('action');
            $.ajax({
                url: formActionUrl,
                type: "POST",
                data: $(this).serialize(),
                success: function(data){
                    var status = data.status
                    if(!status){
                        $("#warning-popup").modal("show")
                        $("#warning-message").text(data.message)
                    }
                    else{
                        $("#success-popup").modal("show")
                        $("#success-message").text(data.message)
                    }
                }
            })

        }
    })
})