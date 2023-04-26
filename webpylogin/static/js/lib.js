const ENLACE_WEB = "/";
let uid = "";
let ldap = false;
getUid();

// ParseUri és una funció que fa un split de la Url

try {
    var my_url = parseUri(document.location);
} catch {

}


function navTaulaUsr() {
    localStorage.setItem("navTaula", 1);
}

function navTaulLog() {
    localStorage.setItem("navTaula", 2);
}

// Agafa la user ID

function getUid() {
    $.ajax({
        type: "post",
        url: "/getUid",
        datatype: "json",
        async: false,
        success: function(data) {
            try {
                if (data.result == "ldap-user") {
                    ldap = true;
                    return true;
                }
                uid = data[0];
            } catch {}
        }
    }, "json").fail((jqXHR, textStatus, errorNumber) => {
        console.log("Fallo" + errorNumber);
        showAlert(13, 0, " de BBDD getUid(). Contacta a l'administrador");
    });
}

// Esborra la galeta i torna a login.

function logout() {
    $.post("/sessio/remove", (data, textStatus, jqXHR) => {}).then(() => {
        console.log("APP: Error de BBDD a la funció expire_session()");
        returnToLogin();
    });
}

// Recarrega la pàgina actual

function recharge() {
    location.reload();
}

// Canvia de pàgina sense que vagi o torni

function noLoop(html) {
    (html != location.pathname) && window.location.assign(html);
}

// Redirigeix ​​a la pàgina principal, recarrega l'actual i bloqueja els inputs

function returnToLogin() {
    $("input").prop("disabled", true);
    recharge();
    setTimeout(noLoop, 100, ENLACE_WEB);
}

// Envia la informació del login

function login() {

    let post_data;
    var regex = /[\w-\.]{2,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}/;
    let email = $("#email").val();

    if (email == "" && $("#pass").val() == "") {
        return console.log("falten camps per omplir");
    }

    if (regex.test(email)) {
        post_data = {
            mail: email,
            pass: hex_md5($("#passwd").val())
        };
    } else {
        post_data = {
            mail: email,
            pass: $("#passwd").val()
        };
    }

    $.post("/sessio/login", post_data, (data, textStatus, jqXHR) => {
        console.log(data);
        if (data.hasOwnProperty('result')) {
            $("#passwd").val("");
            showAlert(0, 0);
        } else {
            localStorage.setItem("alert", 0);
            recharge();
        }


    }, "json").fail((jqXHR, textStatus, errorNumber) => {
        console.log("Fallo " + errorNumber);
        showAlert(13, 0, " de BBDD login(). Consulta a l'administador");
    });
}

// S'assegura que el correu enviat sigui el correcte al modal d'autoeditar-se

function check_email() {
    $("#emailModalSelfEdit").prop("disabled", true);
    loadAuto();
    setTimeout(() => {
        changePasswordAndEmail("#emailModalSelfEdit");
        $("#emailModalSelfEdit").prop("disabled", false);
        loadAuto();
    }, 1000);
}

// Comprova que el correu sigui correcte i envia a token la informació
// necessària per crear el correu electrònic (Email per canviar la Contrasenya).

function changePasswordAndEmail(selector) {
    var regex = /[\w-\.]{2,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}/;

    if (regex.test($(selector).val().trim())) {

        let post_data = {
            mail: $(selector).val(),
            htmlcorreo: "changePasswordEmail"
        };
        $.post("/sendMail/sendmail1", post_data, (data, textStatus, jqXHR) => {
            if (data.result == 'enviat') {
                showAlert(2, 2);
            } else {
                showAlert(13, 0, " al enviar el correu electrònic");
            }
        }, "json").fail((jqXHR, textStatus, errorNumber) => {
            console.log("Fallo " + errorNumber);
            showAlert(13, 0, " de BBDD changePasswordAndEmail(). Contacta a l'administrador");
        });
    } else {
        showAlert(3, 0);
    }
    $(selector).val("");
}


// Mira si les contrasenyes coincideixen i informa si s'ha creat la contrasenya,
// en acabar et reenvia al login. (Canviar la contrasenya)

function createPassword(ruta = "") {
    if ($("#pass").val() == $("#repass").val() && $("#pass").val() != "") {
        let token = my_url.relative.split("/");
        let post_data = {
            newpass: hex_md5($("#pass").val()),
            token: token[2]
        };
        $("input").prop('disabled', true);
        $.post("/" + ruta, post_data, (data, textStatus, jqXHR) => {
            localStorage.setItem("alert", 2);
        }, "json").fail((jqXHR, textStatus, errorNumber) => {
            console.log("Fallo " + errorNumber);
            showAlert(13, 0, " de BBDD. Consulta a l'administador");
        }).then(() => {
            recharge()
        });
    } else {
        showAlert(13, 0, ". Les contrasenyes no coincideixen!");
    }

}

// Posa les dades de cada usuari als inputs quan li donis a Profile

function loadAuto() {
    $.post("/user/show_one", {
        uid: uid
    }, (data, textStatus, jqXHR) => {
        if (data == "sessio_err") {
            location.reload();
        }
        $("#nameModalSelfEdit").val(data[0][1]);
        $("#emailModalSelfEdit").val(data[0][5]);
        $("#uidModalSelfEdit").val(data[0][0]);
        emailEdit = data[0][5];
    }, "json").fail((jqXHR, textStatus, errorNumber) => {
        console.log("Fallo " + errorNumber);
        showAlert(13, 0, " de BBDD loadAuto(). Contacta a l'administrador");
    });
}

// Botó per autoeditar les teves dades

$(document).on("click", "#selfEditBtn", function(e) {
    if ($("#nameModalSelfEdit").val() != "" && $("emailModalSelfEdit") != "") {
        let mail = $("#emailModalSelfEdit").val();
        let datos;
        if (mail != emailEdit) {
            datos = {
                nom: $("#nameModalSelfEdit").val(),
                mail: mail,
                uid: $("#uidModalSelfEdit").val(),
                option: "0"
            };
        } else {
            datos = {
                nom: $("#nameModalSelfEdit").val(),
                mail: mail,
                uid: $("#uidModalSelfEdit").val(),
                option: "1"
            };
        }
        $.post("/user/auto_edit", datos, (data, textStatus, jqXHR) => {
            if (data.result == "mail-exists") {
                showAlert(4, 0);
            } else {
                $("#selfEdit").modal('toggle');
                showAlert(7, 2);
            }
        }, "json").fail((jqXHR, textStatus, errorNumber) => {
            console.log("Fallo " + errorNumber);
            showAlert(13, 0, "de BBDD al autoeditar-se. Contacta a l'administrador");
        });
        e.preventDefault();
    } else {
        showAlert(9, 0);
    }
});

$(document).ready(function() {
    if (getUid() == -1) {
        $("#perfilBtn").remove();
    }
});