$(function() {


    document.querySelectorAll('.editform').forEach((form)=>{
        form.addEventListener('submit', function(e){
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: '',
                data: {
                    'title': e.target.querySelector("input[name='update_title']").value,
                    'type': e.target.submitted,
                    'icon_id': e.target.querySelector("input[name='icon_id']").value,
                    'csrfmiddlewaretoken': e.target.querySelector("input[name='csrfmiddlewaretoken']").value,
                },
            });

            // remove uploaded_icon from list
            document.querySelector("#uploaded_icons_list").removeChild(e.target.closest('.uploaded_icon'));
        })
    });


});
