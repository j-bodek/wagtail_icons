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

    // sort form
    const sort_form = document.getElementById('group_sort_form')
    document.querySelectorAll(".group_sort_option").forEach(option=>{
        option.addEventListener("click", e=>{
            let ordering_parm = option.dataset.cur_ordering;
            if (ordering_parm.endsWith(option.dataset.ordering)){
                value = ordering_parm.startsWith("-") ? option.dataset.ordering : '-' + option.dataset.ordering
            }else{
                value = option.dataset.ordering
            }
            // create hidden input
            let input = document.createElement('input');
            input.setAttribute('name', 'ordering');
            input.setAttribute('value', value);
            input.setAttribute('type', 'hidden');
            sort_form.appendChild(input);
            sort_form.submit();
        })
    })

});
