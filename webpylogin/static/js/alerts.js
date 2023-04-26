/* 
Fitxer per mostrar alerts:
    Requeriments:
        - jquery: 3.6.0
        - bootstrap: 5.1 js i css
*/

const ALERTARRAY = [
    "Error de credencials, el mail o la contrasenya són incorrectes.",
    "Estàs registrat.",
    "S'ha enviat el missatge al correu electrònic!",
    "El correu electrònic no és vàlid!!!",
    "Aquest correu ja existeix!",
    "El correu electrònic o el nom no són vàlids!!!",
    "Error d'autenticació. Introdueix les teves dades",
    "Editat correctament",
    "Error a l'editar",
    "Dades incorrectes",
    "Afegit correctament",
    "Eliminat correctament",
    "Error a l'eliminar",
    "Error",
    "Contrasenya canviada correctament",
    "Dades importades correctament",
];

const COLORARRAY = [
    "danger",
    "warning",
    "success"
];

/**
 *  @name showAlert
 * @description Mostra alerts de bootstrap segons els codis donats
 * @param {int} errorCode 0: Error credencials.
 * 1: Registrat correctament.
 * 2: Missatge enviat al correu. 3: El correu no és vàlid.
 * 4: Correu ja existeix. 5: El correu o el nom no són vàlids.
 * 6: Error d'autenticació. 7: Editat correctament. 8: Error a l'editar.
 * 9: Dades incorrectes. 10: Afegit correctament.
 * 11: Eliminat correctament. 12: Error a l'eliminar
 * 13: Error. 14: Contrasenya canviada correctament
 * 15: Dades importades correctament
 * @param {int} colorCode 0: vermell (danger). 1: groc (warning). 2: verd (success).
 * @param {str} msg Per si vols posar text extra.
 */
function showAlert(errorCode, colorCode, msg = "") {

    $(".alert-" + COLORARRAY[colorCode]).remove();
    $("html").prepend(`
        <div class="alert alert-` + COLORARRAY[colorCode] + ` alert-dismissible fade show" role="alert" style="position:absolute; left: 0; right:0; margin-left: auto; margin-right:auto; margin-top: 0.5%; width: 500px; z-index: 9999 !important; text-align: justify;">
            ` + ALERTARRAY[errorCode] + msg + `
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `);
    if (colorCode == 2) {
        setTimeout(function() {
            $(".alert-" + COLORARRAY[colorCode]).remove();
        }, 1500);
    }
}