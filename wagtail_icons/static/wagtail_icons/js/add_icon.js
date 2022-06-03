$(function() {

    // switch mode logic
    if(document.querySelector("#new_icon_mode") && document.querySelector("#existing_icon_mode")){
        document.querySelector("#new_icon_mode").addEventListener("click", (e)=>{
            if (document.querySelector("#new_icon_box").classList.contains("active")) return;
            document.querySelector("#new_icon_box").classList.add("active");
            document.querySelector("#existing_icon_box").classList.remove("active");
        })
        document.querySelector("#existing_icon_mode").addEventListener("click", (e)=>{
            if (document.querySelector("#existing_icon_mode").classList.contains("active")) return;
            document.querySelector("#existing_icon_box").classList.add("active");
            document.querySelector("#new_icon_box").classList.remove("active");
        })
    }

    let update_forms_listener = function(){
        document.querySelectorAll('.updateform').forEach((form)=>{
            form.addEventListener('submit', function(e){
                e.preventDefault();
                $.ajax({
                    type: 'POST',
                    url: '',
                    data: {
                        'title': e.target.querySelector(".update_title").value,
                        'action':e.target.submitted,
                        'icon_id':e.target.dataset.icon_id,
                        'csrfmiddlewaretoken': e.target.querySelector(".csrftoken").value,
                    },
                });

                // remove uploaded_icon from list
                document.querySelector("#uploaded_icons_list").removeChild(e.target.closest('.uploaded_icon'));
            })
        });
    };


    let upload_icon_form = function(uploaded_list, icon){
        let li = document.createElement("li");
        li.className = "uploaded_icon"
        let li_html_content = ``;
        if (! icon.code){
            li_html_content = `
                <div class="icon_box">
                    <img src="${icon.icon_url}" class="icon">
                </div>
                <div class="content_box">
                    <p class="message">Upload Successful. You can now update icon with new title or delete icon completely.</p>
                    <form class="updateform" method="POST" data-icon_id="${icon.icon_id}">
                        <input type="hidden" name="csrfmiddlewaretoken" class="csrftoken" value="${getCookie('csrftoken')}">
                        <div class="input_box">
                            <label for="update_title">Title</label>
                            <input class="update_title"  id="update_title" type="text" value="${icon.icon_title.replace(/\.[^/.]+$/, "")}">
                        </div>
                        <button class="update_btn" type="submit" onclick="this.form.submitted=this.value;" value="update">update</button>
                        <button class="delete_btn" type="submit" onclick="this.form.submitted=this.value;" value="delete"> delete </button>
                    </form>
                </div>
            `
        }else{
            li.classList.add("error")
            li_html_content = `
            <h3>${icon.code}</h3>
            <p>${icon.message}</p>
            `
            // remove error message from list after one second
            setTimeout(() => {
                uploaded_list.removeChild(li);
              }, 5000);
        }

        li.insertAdjacentHTML('beforeend', li_html_content);
        // li.appendChild()
        uploaded_list.appendChild(li)
    }



    // helper function for getting csrftoken value
    function getCookie(name) {
        let cookieValue = null;
    
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
    
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    
                    break;
                }
            }
        }
    
        return cookieValue;
    }


    document.querySelector("#fileinput").addEventListener("change",e=>{
        let file = $("#fileinput").prop('files');
        if (file.length > 1) {
            return;
        }else{
            file = file[0]
        }
        
        if (['png', 'svg'].includes(file.name.split('.')[1])){
            $("#previewIcon").attr("src", URL.createObjectURL(file))
            $("#previewIcon").css("display", "block")
            $("#wrong_format_info").css("display", "none")
            $(".previewIcon_box").css("background", "#fafafa")
        }else{
            $("#previewIcon").attr("src", "")
            $("#previewIcon").css("display", "none")
            $("#wrong_format_info").css("display", "block")
            $(".previewIcon_box").css("background", "#FB888A")
        }
    })


    $('#fileform').submit(function(e){
        e.preventDefault();    
        // add data to formData
        let formData = new FormData();
        let title = $("#titleinput").val()
        formData.append('title', $("#titleinput").val());
        formData.append('action','upload');
        formData.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        if (document.querySelector(".add_button").dataset.group_id){
            formData.append('group', document.querySelector(".add_button").dataset.group_id)
        }
        // add file to formData
        let files = $("#fileinput").prop('files');
        for (let i = 0; i < files.length; i++) {
            formData.append(`icons`, files[i]);
            formData.append(`urls`, URL.createObjectURL(files[i]));
        }
        // console.log( $("#fileinput").prop('files')[0])
        // formData.append('files', files),
        // send formData

        $.ajax({
            url: '',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {          

                // reset form fields and previewIcon after sending data
                $('#fileform')[0].reset();
                $("#previewIcon").attr("src", "")
                $("#previewIcon").css("display", "none")
                $("#wrong_format_info").css("display", "none")
                $(".previewIcon_box").css("background", "#fafafa")
        
                let uploaded_list = document.getElementById("uploaded_icons_list");
                
                // display uploaded icon
                for (let i = 0; i < response.length; i++) {
                    upload_icon_form(uploaded_list, response[i])
                }

                // add listeners to newly uploaded form
                update_forms_listener()

            },


        });

    });

});
