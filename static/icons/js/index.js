$(function() {

    // display or hide action buttons
    let display_buttons = function() {
        let checked = []
        document.querySelectorAll('.icon_input').forEach(icon_choice=>checked.push(icon_choice.checked))
        if (checked.includes(true)){
            document.querySelector(".button_box").style.display = 'block'
        }else{
            document.querySelector(".button_box").style.display = 'none'
        }
    }


    // submit form
    $('.main_button').click(e=>{
        form = document.getElementById("choose_icons_form")
        form.action = e.target.value
        form.submit()
    })


    $("#choose_icons_form").submit(function(e) {
        e.preventDefault()
        let icons_ids = []
        document.querySelectorAll('input[name=checkbox]:checked').forEach(input=>icons_ids.push(input.value))
    });

    // style icon choice after choosing it
    document.querySelectorAll('.icon_choice').forEach(icon_choice=>{
        icon_choice.addEventListener('click', e=>{
            icon_choice.classList.toggle('icon_active')
            let input = icon_choice.closest('.icon_choice_box').querySelector(".icon_input");
            if (input.checked) {
                input.checked = false;
            }else{
                input.checked = true;
            }

            display_buttons()
        })
    })



});
