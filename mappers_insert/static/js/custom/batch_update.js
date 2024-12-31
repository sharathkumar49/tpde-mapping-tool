$(document).ready(function () {
    // $('#success-popup').modal('show')
    if ($('#message').val()) {
        $('#success-popup').modal('show')
        $("#success-message").text($('#message').val())
    }
    var datatable_options = {
        ordering: false,
        columnDefs: [
            { targets: 0, ordering: false },
        ],
        fnDrawCallback: function () {
            var select_all = $('#select-all').is(":checked")
            if (select_all) {
                $('#batch-record-table tbody tr').css("background-color", "antiquewhite")
                $('#batch-record-table tbody .select-record').prop('checked', true)
            } else {
                $('#batch-record-table tbody tr').css("background-color", "#fff")
                $('#batch-record-table tbody .select-record').prop('checked', false)
            }
        }
    }
    $("#batch-record-table").DataTable(datatable_options)
    var string_json = $("#mapping_ids").val()
    var total_ids = []
    if (string_json) {
        total_ids = JSON.parse(string_json)
    }

    var mapping_ids = []
    var check_all = false
    var columns = []
    $('.search-input').on('input', function () {
        var val = this.value
        var col_name = $(this).attr('id')
        var feed_id = $('#feed_id').val()
        var category_id = $('#feed_category_id').val()
        var csrf_token = getCookie('csrftoken')
        var search_cols = $('.search-input')
        var client_id = $('#client_id').val()
        var search_filter = {}
        for (var i = 0; i < search_cols.length; i++) {
            console.log(search_cols[i].value)
            if (search_cols[i].value) {
                search_filter[search_cols[i].id] = search_cols[i].value
            }
        }

        $.ajax({
            url: '/batches/batch/record/search/filter/',
            type: 'POST',
            data: {
                'filter': JSON.stringify(search_filter),
                'col_name': col_name,
                'feed_id': feed_id,
                'feed_category_id': category_id,
                'client_id': client_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                var response_data = data.data
                var headers = data.headers
                total_ids = JSON.parse(data.mapping_ids)
                var tbody = ""
                for (var i = 0; i < response_data.length; i++) {
                    var tr = '<tr>'
                    tr += '<td><input type="checkbox" class="select-record"></td>'
                    for (var j = 0; j < headers.length; j++) {
                        tr += '<td class="text-uppercase text-center text-secondary text-xxs font-weight-bolder opacity-7" id="' + response_data[i]['MappingID'] + '">' + response_data[i][headers[j]] + '</td>'
                    }
                    tr += '</tr>'
                    tbody += tr

                }
                if ($.fn.DataTable.isDataTable('#batch-record-table')) {
                    $('#batch-record-table').DataTable().clear().destroy();
                }
                $('#batch-record-table tbody').html(tbody)

                $("#batch-record-table").DataTable(datatable_options)
                $("#" + col_name).focus()
            }
        })
    })

    $('#batch-record-table tbody').on('click', 'tr td input.select-record', function () {
        var checked = $(this).is(":checked")
        var row = $(this).closest("tr")
        var mappers_id = $(row).attr("id")
        var length = $("#batch_record_view tbody > tr").length
        if (checked) {
            $(row).css("background-color", "antiquewhite")
            mapping_ids.push(mappers_id)
        }
        else {
            $('#select-all').prop("checked", false)
            $(row).css("background-color", "#fff")
            mapping_ids.splice($.inArray(mappers_id, mapping_ids), 1);
        }
        if (total_ids.length == mapping_ids.length) {
            $('#select-all').prop("checked", true)
            mapping_ids = []
            mapping_ids = $.merge(mapping_ids, total_ids)
        }
    });

    $('#update-btn').click(function () {
        var update_type = $('#update_type').val()
        if (mapping_ids.length > 0) {
            if (update_type == 'bulk') {
                $("#column-popup").modal('show')
                $('.column-box').css("background-color", "#fff")
                columns = []
                $('#ids').val(JSON.stringify(mapping_ids))
            }
            else {
                $('#ids').val(JSON.stringify(mapping_ids))
                $('#update-form').submit()
            }

        }
        else {
            $("#warning-popup").modal("show")
            $("#warning-message").text("Please select atleast one record")
        }

    })

    $('#select-all').on('click', function () {
        $('#batch-record-table tbody .select-record').prop('checked', this.checked)
        $('#batch-record-table tbody tr').css("background-color", "#fff")
        var checked = $(this).is(":checked")
        mapping_ids = []
        if (checked) {
            $('#batch-record-table tbody tr').css("background-color", "antiquewhite")
            mapping_ids = $.merge(mapping_ids, total_ids)
        }

    })

    $("#column-confirm-btn").on('click', function () {
        if (columns.length > 0) {
            columns = JSON.stringify(columns)
            $('#columns').val(columns)
            $('#update-form').submit()
        } else {
            $("#column-popup").modal('hide')
            $("#warning-popup").modal("show")
            $("#warning-message").text("Please select atleast one column")
        }
    })

    $('.column-box').click(function () {
        var val = $(this).text()
        if (columns.indexOf(val) >= 0) {
            $(this).css("background-color", "#fff")
            columns.splice(columns.indexOf(val), 1)
        } else {
            $(this).css("background-color", "antiquewhite")
            columns.push(val)
        }
    })


})