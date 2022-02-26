$(function() {

    let uploaded_forms_listener = function(){
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



    $('#fileform').submit(function(e){
        e.preventDefault();    
        // add data to formData
        let formData = new FormData();
        let title = $("#titleinput").val()
        formData.append('title', $("#titleinput").val());
        formData.append('action','upload');
        formData.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
        // add file to formData
        let file = $("#fileinput").prop('files')[0];
        formData.append('file', file),
        // send formData
        $.ajax({
            url: '',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {             

                // reset form fields after sending data
                $('#fileform')[0].reset();
        
                let uploaded_list = document.getElementById("uploaded_icons_list");
                
        
                let li = document.createElement("li");
                li.className = "uploaded_icon"
                let li_html_content = `
                <div class="icon_box">
                    <img src="${URL.createObjectURL(file)}" class="icon">
                </div>
                <div class="content_box">
                    <p class="message">Upload Successful. You can now update icon with new title or delete icon completely.</p>
                    <form class="updateform" method="POST" data-icon_id="${response.icon_id}">
                        <input type="hidden" name="csrfmiddlewaretoken" class="csrftoken" value="${getCookie('csrftoken')}">
                        <div class="input_box">
                            <label for="update_title">Title</label>
                            <input class="update_title"  id="update_title" type="text" value="${title ? title : file.name.replace(/\.[^/.]+$/, "")}">
                        </div>
                        <button class="update_btn" type="submit" onclick="this.form.submitted=this.value;" value="update">update</button>
                        <button class="delete_btn" type="submit" onclick="this.form.submitted=this.value;" value="delete"> delete </button>
                    </form>
                </div>
                `
                li.insertAdjacentHTML('beforeend', li_html_content);
                // li.appendChild()
                uploaded_list.appendChild(li)

                // add listeners to newly uploaded form
                uploaded_forms_listener()
            },


        });

    });

});
