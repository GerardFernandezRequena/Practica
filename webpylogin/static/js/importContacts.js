$(document).ready(function() {
    $("#importBtn").click(function(e) {
        let dates = $("#formFile").val();
        let array = dates.split(".");
        if (array[array.length - 1] != "csv") {
            showAlert(13, 0, " l'arxiu no es vàlid! Ha de ser un arxiu csv");
            return;
        }
        if (dates != "") {
            $.ajax({
                url: 'importContacts/enviar',
                type: 'POST',
                data: new FormData($('form')[0]),
                cache: false,
                contentType: false,
                processData: false,
                xhr: function() {
                    var myXhr = $.ajaxSettings.xhr();
                    if (myXhr.upload) {
                        myXhr.upload.addEventListener('progress', function(e) {
                            if (e.lengthComputable) {
                                $('progress').attr({
                                    value: e.loaded,
                                    max: e.total,
                                });
                            }
                        }, false);
                    }
                    return myXhr;
                },
                success: function(data) {
                    if (data.result) {
                        showAlert(13, 0, " al importar les dades");
                    } else {
                        showAlert(15, 2);
                    }
                },
                fail: function(jqXHR, textStatus, errorNumber) {
                    console.log("Fallo " + errorNumber);
                    showAlert(13, 0, " al importar les dades");
                }
            });
        } else {
            showAlert(13, 0, " no has introduit cap arxiu");
        }
    });
});