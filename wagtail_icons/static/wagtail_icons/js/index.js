$(function() {

    // after submiting search form add parameter to url
    let search_form = document.querySelector(".search-form");
    search_form.addEventListener("submit", form=>{
        form.preventDefault();

        url = new URL(window.location.href);
        
        for (let key of url.searchParams.keys()) {
            // append new hidden input
            if (key == 'q') continue;
            let input = document.createElement('input');
            input.setAttribute('name', key);
            input.setAttribute('value', url.searchParams.get(key));
            input.setAttribute('type', 'hidden')
            search_form.appendChild(input);
        }
    
        search_form.submit();//send with added input
    })

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
        $(".type_input").val(e.target.dataset.type)
        if (e.target.dataset.group_id){
            $(".group_input").val(e.target.dataset.group_id)
        }
        form.action = e.target.value
        form.submit()
    })


    $("#choose_icons_form").submit(function(e) {
        e.preventDefault()
        let icons_ids = []
        document.querySelectorAll('input[name=checkbox]:checked').forEach(input=>icons_ids.push(input.value))
    });

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

                display_buttons()
            }
        })
    })


    // // display icon title after hover on it
    // document.querySelectorAll('.icon_choice').forEach(icon_choice=>{
    //     icon_choice.addEventListener('mouseover', e=>{
    //         // get coordinates of icon_choice
    //         let container_coordinates = document.getElementById("main").getBoundingClientRect();
    //         let icon_coordinates = icon_choice.getBoundingClientRect();
    //         let icon_title = document.getElementById(`icon_title_${icon_choice.dataset.id}`)
    //         icon_title.style.display = 'inline-block'
    //         icon_title.style.left = `${icon_coordinates.left-container_coordinates.left}px`
    //         icon_title.style.top = `${icon_coordinates.top-container_coordinates.top-20}px`
    //         // e.target.closest('.icon_title').style.display = 'block'
    //         // icon_choice.classList.toggle('icon_active')
    //         // let input = icon_choice.closest('.icon_choice_box').querySelector(".icon_input");
    //         // if (input.checked) {
    //         //     input.checked = false;
    //         // }else{
    //         //     input.checked = true;
    //         // }

    //         // display_buttons()
    //     })
    // })

    // document.querySelectorAll('.icon_choice').forEach(icon_choice=>{
    //     icon_choice.addEventListener('mouseout', e=>{
    //         // get coordinates of icon_choice
    //         let coordinates = icon_choice.getBoundingClientRect();
    //         let icon_title = document.getElementById(`icon_title_${icon_choice.dataset.id}`)
    //         icon_title.style.display = 'none'
    //         // e.target.closest('.icon_title').style.display = 'block'
    //         // icon_choice.classList.toggle('icon_active')
    //         // let input = icon_choice.closest('.icon_choice_box').querySelector(".icon_input");
    //         // if (input.checked) {
    //         //     input.checked = false;
    //         // }else{
    //         //     input.checked = true;
    //         // }

    //         // display_buttons()
    //     })
    // })



});
