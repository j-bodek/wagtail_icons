$(function() {


    $('#fileform').submit(function(e){
        e.preventDefault();    
        // add data to formData
        let formData = new FormData();
        formData.append('title', $("#titleinput").val());
        formData.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        // add file to formData
        // let file = document.querySelector("#fileinput")
        formData.append('file', $("#fileinput").prop('files')[0]),
        // send formData
        $.ajax({
            url: '',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function () {
                
            },
        });

        // reset form fields after sending data
        $('#fileform')[0].reset()
    });

});
