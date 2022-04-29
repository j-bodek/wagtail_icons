$(function() {


    // submit form
    $('.main_button').click(e=>{
        form = document.getElementById("group_form")
        $(".type_input").val(e.target.dataset.type)
        if (e.target.dataset.group_id){
            $(".group_input").val(e.target.dataset.group_id)
        }
        form.action = e.target.value
        form.submit()
    })

    // style icon choice after choosing it
    document.querySelectorAll('.icon').forEach(icon_choice=>{
        icon_choice.addEventListener('click', e=>{
            icon_choice.classList.toggle('icon_active')
            if (icon_choice.closest('.icon_choice_box')){
                let input = icon_choice.closest('.icon_choice_box').querySelector(".icon_input");
                if (input.checked) {
                    input.checked = false;
                }else{
                    input.checked = true;
                }
            }
        })
    })
});
