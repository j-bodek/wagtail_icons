$(function() {


    // submit form
    document.querySelector(".group_button").addEventListener("click", e=>{
        form = document.getElementById("groups_form")
        $(".group_form_type").val(e.target.dataset.type)
        form.action = e.target.value
        form.submit()
    })


    // $("#choose_icons_form").submit(function(e) {
    //     e.preventDefault()
    //     let icons_ids = []
    //     document.querySelectorAll('input[name=checkbox]:checked').forEach(input=>icons_ids.push(input.value))
    // });

    // display delete btn if group is checked
    document.querySelectorAll('.group-checkbox').forEach(group_checkbox=>{
        group_checkbox.addEventListener('click', e=>{
            let checked = []
            document.querySelectorAll('.group-checkbox').forEach(choice=>checked.push(choice.checked))
            if (checked.includes(true)){
                document.querySelector(".delete-btn-box").style.display = 'block'
            }else{
                document.querySelector(".delete-btn-box").style.display = 'none'
            }
        });
    })

});
