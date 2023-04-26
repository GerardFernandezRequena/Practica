var usrlvl = "";
$(document).ready(() => {
    if (localStorage.getItem("alert") == 0) {
        showAlert(1, 2);
        localStorage.setItem("alert", -1);
    }

    // Si el userlvl és admin (2) es traurà el hidden als enllaços a les taules
    usrlvl = $.cookie("ulvl");
    if ($.cookie("ulvl") == 3) {
        $(".navHide1").append('<a class="dropdown-item tablelogs" onclick="navTaulLog()" href="/registerUsr"><i class="fas fa-file-alt"></i> Registres</a>');
        $(".navHide2").append('<a class="dropdown-item tableUsers" onclick="navTaulaUsr()" href="/registerUsr" style=""><i class="fas fa-users"></i> Usuaris</a>');
    } else if ($.cookie("ulvl") == 1) {
        $("#editPhoneUser").remove();
        $("#buttonOpenDelete").remove();
        $("#deleteModal").remove();
    } else if (ldap == true) {
        console.log("Ldap option On");
    }

    $('.collapse').on('show.bs.collapse', function() {
        $(".navHide1 a").removeClass("dropdown-item");
        $(".navHide2 a").removeClass("dropdown-item");
        $(".navHide1 a").addClass("nav-link");
        $(".navHide2 a").addClass("nav-link");

    })

    // Mostra la informació de la taula "list"
    let tablelogs = $("#table").DataTable({
        scrollCollapse: false,
        paging: true,
        retrieve: true,
        responsive: true,
        deferRender: true,
        scrollY: "629px",
        aaSorting: [],
        lengthMenu: [
            [15, 25, 50, 100],
            [15, 25, 50, 100]
        ],
        language: {
            url: "https://sekhmet.enginy.eu/vendor/datatables/datatables.ca.json"
        },
        columns: [{
                title: "Nom",
                data: "1",
                responsivePriority: 1,
                className: "align-middle"
            },
            {
                title: "Empresa",
                data: "3",
                responsivePriority: 1,
                className: "align-middle"
            },
            {
                title: "Telèfon fix",
                data: "7",
                responsivePriority: 2,
                className: "align-middle",
                render: function(data, _type, _row, _meta) {
                    data == data[7];
                    if (data == 0) {
                        return "";
                    } else {
                        return data;
                    }
                }
            },
            {
                title: "Telèfon mòbil",
                data: "8",
                responsivePriority: 3,
                className: "align-middle",
                render: function(data, _type, _row, _meta) {
                    data == data[8];
                    if (data == 0) {
                        return " ";
                    } else {
                        return data;
                    }
                }
            },
            {
                title: "Correu electrònic",
                data: "10",
                responsivePriority: 4,
                className: "align-middle"
            },
            {
                data: "0",
                orderable: false,
                responsivePriority: 2,
                render: function(data, _type, _row, _meta) {
                    if (usrlvl == 1) {
                        return "<button type='button' class='btn btn-primary editarLista' value='" + data + "' data-bs-toggle='modal' data-bs-target='#editList'><i class='fas fa-eye'></i></button>"
                    } else if (usrlvl == 2 || usrlvl == 3 || ldap == true) {
                        return "<button type='button' class='btn btn-primary editarLista' value='" + data + "' data-bs-toggle='modal' data-bs-target='#editList'><i class='fas fa-edit'></i></button>";
                    } else {
                        return ""
                    }
                }
            }
        ],
        infoCallback: function() {
            return "";
        },
        "fnCreatedRow": function(nRow, aData, iDataIndex) {
            $(nRow).attr('id', aData[0]);
            $(nRow).attr('class', "trBtn");
        },
        drawCallback: function(settings) {
            if (usrlvl == 2 || usrlvl == 3 || ldap == true) {
                $("button[data-bs-target='#addNewPhone']").remove();
                $("<button type='button' class='btn btn-primary mx-3 my-1' data-bs-toggle='modal' data-bs-target='#addNewPhone'><i class='fas fa-plus 2px'></i></button>").appendTo("#table_length");
            }
        },
        ajax: {
            url: "/contact/list",
            method: 'POST',
            dataSrc: function(data) {
                if (data.result) {
                    console.log(data.result);
                    localStorage.setItem("alert", 1);
                    location.reload();
                }
                return data;
            },
        }
    });

    // Recarrega la taula
    $(document).on("click", ".editarLista", function() {
        $.post("/contact/show_one", {
            uid: $(this).attr("value")
        }, (data, textStatus, jqXHR) => {
            if (data.result) {
                localStorage.setItem("alert", 1);
                location.reload();
            }
            for (let index = 1; index < data[0].length; index++) {
                if (data[0][index] == null || data[0][index] == 0) {
                    $("#modalPhone" + index).val("");
                } else {
                    $("#modalPhone" + index).val(data[0][index]);
                }
            }

            $("#uidModalEdit").val($(this).attr("value"));
        }, "json").fail((jqXHR, textStatus, errorNumber) => {
            console.log("Fallo " + errorNumber);
            showAlert(13, 0, " de BBDD al mostrar contacte. Contacta a l'administrador");
        });
    });

    // Filtra per cercar a la taula "list"
    $('#filtro').on('keyup', function() {
        tablelogs.search(this.value).draw();
    });


    // Edita la informació d'un Usuari de "list"
    $("#editPhoneUser").click(function() {
        let array = [];
        let y = 1;
        for (let i = 0; i < 11; i++) {
            array[i] = $("#modalPhone" + y).val();
            y++;
        }
        let datos = {
            nom: array[0],
            cognoms: array[1],
            empresa: array[2],
            carrer: array[3],
            poblacio: array[4],
            cp: KillSpaces(array[5]),
            telfix: KillSpaces(array[6]),
            telmovil: KillSpaces(array[7]),
            fax: KillSpaces(array[8]),
            correu: array[9],
            nif: array[10],
            id: $("#uidModalEdit").val()
        }

        if (datos.nom != "") {
            $.post("/contact/edit", datos, (data, textStatus, jqXHR) => {
                if (data.result) {
                    showAlert(8, 0);
                } else {
                    tablelogs.ajax.reload();
                    $("#editList").modal('toggle');
                    showAlert(7, 2);
                }
            }, "json").fail((jqXHR, textStatus, errorNumber) => {
                console.log("Fallo " + errorNumber);
                showAlert(13, 0, " de BBDD al editar contacte. Contacta a l'administrador");
            });
        } else {
            showAlert(9, 0, ". Introduexi un nom vàlid");
        }
    });

    // Afegeix la informació d'un Usuari a la taula "list"
    $("#addUserPhoneSave").click(function(e) {
        e.preventDefault();
        let array = [];
        let y = 1;
        for (let i = 0; i < 11; i++) {
            array[i] = $("#modalAddTel" + y).val();
            y++;
        }

        let datos = {
            nom: array[0],
            cognoms: array[1],
            empresa: array[2],
            carrer: array[3],
            poblacio: array[4],
            cp: KillSpaces(array[5]),
            telfix: KillSpaces(array[6]),
            telmovil: KillSpaces(array[7]),
            fax: KillSpaces(array[8]),
            correu: array[9],
            nif: array[10]
        }
        if (datos.nom != "") {
            $.post("/contact/add", datos,
                function(data, textStatus, jqXHR) {
                    if (data.result) {
                        showAlert(13, 0, " al afegir contacte");
                    }
                    tablelogs.ajax.reload();
                    $("#addNewPhone").modal('toggle');
                    y = 0;
                    for (let i = 0; i < 12; i++) {
                        $("#modalAddTel" + y).val("");
                        y++;
                    }
                    showAlert(10, 2);
                }, "json").fail((jqXHR, textStatus, errorNumber) => {
                console.log("Fallo " + errorNumber);
                showAlert(13, 0, " de BBDD al afegir contacte. Contacta a l'administrador");
            });
        } else {
            showAlert(9, 0, ". Introduexi un nom vàlid");
        }
    });

    $("#deletePhoneButton").click(function(e) {
        data = { id: $("#uidModalEdit").val() }
        $.post("/contact/delete", data,
            function(data, textStatus, jqXHR) {
                tablelogs.ajax.reload();
                $("#deleteModal").modal('toggle');
                showAlert(11, 2);
            },
            "json"
        ).fail((jqXHR, textStatus, errorNumber) => {
            console.log("Fallo " + errorNumber);
            showAlert(12, 0, " el contacte.");
        });
    });
    $("#returnEditPhone").click(function() {
        $("#deleteModal").modal('toggle');
        $("#editList").modal('toggle');
    });

    function KillSpaces(phrase) {
        if (phrase != "") {
            var totalPhrase = "";
            for (i = 0; i < phrase.length; i++) {
                if (isNaN(phrase[i])) {
                    return 0;
                }
                if (phrase[i] != " ") {
                    totalPhrase += phrase[i];
                }
            }
        } else {
            return 0;
        }
        return parseInt(totalPhrase);
    }

});