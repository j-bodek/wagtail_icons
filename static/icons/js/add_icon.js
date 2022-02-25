$(function() {
    document.getElementById("fileupload").onchange = function(e) {
        document.getElementById("fileform").submit();
        e.preventDefault()
    };
});
