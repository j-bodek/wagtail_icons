$(function() {
    $('#fileform').submit(function(e){
        e.preventDefault();    
        // add data to formData
        let formData = new FormData();
        let title = $("#titleinput").val()
        formData.append('title', $("#titleinput").val());
        formData.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        // add file to formData
        let file = $("#fileinput").prop('files')[0]
        formData.append('file', file),
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
        $('#fileform')[0].reset();

        // console.log(JSON.parse("{{data|escapejs}}"))
        let uploaded_list = document.getElementById("uploaded_icons_list");

        let li = document.createElement("li");
        li.className = "uploaded_icon"
        let li_html_content = `
        <div class="icon_box">
            <img src="${URL.createObjectURL(file)}" class="icon">
        </div>
        <div class="content_box">
            <p class="message">Upload Successful. You can now update icon with new title or delete icon completely.</p>
            <form id="updateform">
                <div class="input_box">
                    <label for="update_title">Title</label>
                    <input  id="update_title" type="text" value="${title ? title : file.name.replace(/\.[^/.]+$/, "")}">
                </div>
                <button class="update_btn" type="submit" name="send" value="update">update</button>
                <button class="delete_btn" type="submit" name="send" value="delete"> delete </button>
            </form>
        </div>
        `
        li.insertAdjacentHTML('beforeend', li_html_content);
        // li.appendChild()
        uploaded_list.appendChild(li)
    });

});
