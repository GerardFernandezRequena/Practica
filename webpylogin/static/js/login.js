$.when($.ready).then(function() {
    if (localStorage.getItem("alert") == 1) {
        showAlert(6, 0);
        localStorage.setItem("alert", -1);
    } else if (localStorage.getItem("alert") == 2) {
        showAlert(14, 2);
        localStorage.setItem("alert", -1);
    }
    $("#enterMail").hide();

    // Treu les dades dels inputs i desactiva el botó submit
    $(".form-control").val("");
    $("#submitLoginBtn").attr("disabled", "disabled");

    // Crida a la funció cambia()

    $("input").on('change', function() {
        change();
    });

    // Valida que els inputs estan escrits i fa que salti entre els inputs
    // pressionant enter.

    $("#login").on('submit', function(e) {
        if ($("#email").val() === "")
            $("#email").focus();
        else if ($("#pass").val() === "")
            $("#pass").focus();
        else
            login();
        e.preventDefault();
        e.stopPropagation();
    });


    $("#changePasswordandEmail").on('submit', function(e) {
        if ($("#email2").val() === "")
            $("#email2").focus();
        else
            changePasswordAndEmail('#email2');
        e.preventDefault();
        e.stopPropagation();
    });

    $("#createPasswordandEmail").on('submit', function(e) {
        if ($("#name2").val() === "")
            $("#name2").focus();
        else if ($("#email3").val() === "")
            $("#email3").focus();
        else
            createPasswordAndEmail('#email3');
        e.preventDefault();
        e.stopPropagation();
    });
});

// Mostra el form de canviar contrasenya
function viewMailRecovery() {
    $("#divLogin").toggle();
    $("#enterMail").toggle();
    $(".messageSent").html("");
}

// Mira si els inputs estan plens per passar al següent input,
// quan estan plens treu el disable al botó.
function change(e) {
    if ($("#email").val() === "")
        $("#email").focus();
    else if ($("#pass").val() === "")
        $("#pass").focus();
    else if ($("#email").focus() != "" && $("#pass").val() != "")
        $("button").removeAttr("disabled");
}

// Missatge d'error de credencials
function msg(int) {
    (int == 1)
    return "Has entrat malament les credencials";
}