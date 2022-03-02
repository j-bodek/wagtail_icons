$(function() {

    let display_buttons = function() {
        let checked = []
        document.querySelectorAll('.icon_input').forEach(icon_choice=>checked.push(icon_choice.checked))
        if (checked.includes(true)){
            document.querySelector(".button_box").style.display = 'block'
        }else{
            document.querySelector(".button_box").style.display = 'none'
        }
    }

    $("#choose_icons_form").submit(function(e) {
        let icons_ids = []
        document.querySelectorAll('input[name=checkbox]:checked').forEach(input=>icons_ids.push(input.value))
        $.ajax({
            type: 'POST',
            url: '',
            data: {
                'type': e.target.submitted,
                'icons': icons_ids,
                'csrfmiddlewaretoken': e.target.querySelector("input[name=csrfmiddlewaretoken]").value,
            },
        });
    });

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
