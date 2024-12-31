$(document).ready(function () {
    var params = new URLSearchParams(window.location.search);
    var success = params.get("success")
    console.log(success)
    if (success == 'false') {
        $("#success-popup").modal("show")
        $("#success-message").text("File has no data or having all duplicates. Please check the file and try again ..!")
    }
    
    $('.datatable').DataTable();
    $("#data-form").submit(function (e) {
        e.preventDefault();
        var extensions = ['csv', 'xlsx']
        var file = $('#file_data')[0].files[0]
        var filename = file.name
        if (extensions.indexOf(filename.split('.')[1]) >= 0) {
            $.blockUI({
                message: '<div class="page-content page-container" id="page-content"><div class="padding" style="background-color:unset!important"><div class="row container d-flex justify-content-center"><div class="loader-demo-box"><div class="bar-loader"><span></span><span></span><span></span><span></span></div></div></div></div></div>' });
            this.submit()
        }
        else {
            $("#warning-popup").modal("show")
            $("#warning-message").text("Please upload valid file format ..!")
        }
    })
})