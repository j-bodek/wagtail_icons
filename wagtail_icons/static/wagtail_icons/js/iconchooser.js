
$(document).ready(function(){
    const select_box = document.querySelector(".select-box")
    const selected = document.querySelector(".selected");
    const OptionsContainer = document.querySelector(".options-container");
    const arrowIcon = document.getElementById("arrow_icon")
    
    const optionsList = document.querySelectorAll(".option");
    const selected_text = document.querySelector(".selected_text")
    
    // close or open optionslist after clicking on selected
    selected.addEventListener("click",(e)=>{
        OptionsContainer.classList.toggle("active");
        selected.classList.toggle("active");
        arrowIcon.classList.toggle("rotated");
    })

    // after clicking in option
    optionsList.forEach(option=>{
        option.addEventListener("click",(e)=>{
            // remove active class from all options
            optionsList.forEach(option=>{
                option.classList.remove('active')
            })
            // add active class to option, close dropdown list and change selected value
            option.classList.toggle("active");
            selected_text.innerHTML = option.querySelector(".icon_option").innerHTML;
            OptionsContainer.classList.remove("active");
            selected.classList.remove("active");
            arrowIcon.classList.remove("rotated");
            // check input
            e.target.checked = true;
        })
    })

    // close dropdown list after clicking outside
    document.body.addEventListener('click', function (event) {
        if (! select_box.contains(event.target)) {
            OptionsContainer.classList.remove("active");
            selected.classList.remove("active");
            arrowIcon.classList.remove("rotated");
        }
    });
});





