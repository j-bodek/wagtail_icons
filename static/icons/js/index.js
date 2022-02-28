$(function() {

    $("#choose_icons_form").submit(function(e) {
        let icons_ids = []
        document.querySelectorAll('input[name=checkbox]:checked').forEach(input=>icons_ids.push(input.value))
        $.ajax({
            type: 'POST',
            url: '',
            data: {
                'icons_ids': icons_ids,
                'csrfmiddlewaretoken': e.target.querySelector("input[name=csrfmiddlewaretoken]").value,
            },
        });
    });

});
