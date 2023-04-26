$.when($.ready).then(function() {

    $("input").on('change', function() {
        change();
    });

    $("#createPassword").on('submit', function(e) {
        if ($("#pass").val() === "")
            $("#pass").focus();
        else if ($("#repass").val() === "")
            $("#repass").focus();
        else {
            createPassword('createPssword');
        }
        e.preventDefault();
        e.stopPropagation();
    });

    $("#changePassword").on('submit', function(e) {
        if ($("#pass").val() === "")
            $("#pass").focus();
        else if ($("#repass").val() === "")
            $("#repass").focus();
        else {
            createPassword('regenPass');
        }
        e.preventDefault();
        e.stopPropagation();
    });
});


function change() {
    if ($("#pass").val() === "")
        $("#pass").focus();
    else if ($("#repass").val() === "")
        $("#repass").focus();
}