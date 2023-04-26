var usrlvl = $.cookie("ulvl");
var emailEdit = "";
let msg = '<b class="mb-2" class="errorPass" style="color: #E44660 !important;">Les contrasenyes no coincideixen</b>';
let table;

$(document).ready(function() {
    if (usrlvl > 3) {
        recharge("/");
        localStorage.setItem("alert", 1);
    }
    // Canvi de taules
    $(".tablelogs").click(function(e) {
        $("#table-log-actions").show();
        $("#users-table").hide();
        tableLogActions();
    });
    $(".tableUsers").click(function(e) {
        $("#table-log-actions").hide();
        $("#users-table").show();
        tableUsers();
    });

    // Selecciona la taula a mostrar des de fora de la pàgina
    if (localStorage.getItem("navTaula") == 1) {
        $("#table-log-actions").toggle();
        $("#users-table").toggle();
        $("#switchTables").text("Tabla de usuarios");
        tableUsers();
    } else if (localStorage.getItem("navTaula") == 2) {
        $("#switchTables").text("Tabla de registros");
        tableLogActions();
    }
    // Crea la taula amb les accions que es fan dins de la pàgina
    function tableLogActions() {
        let tableRecords = $("#table").DataTable({
            scrollCollapse: false,
            paging: true,
            retrieve: true,
            responsive: true,
            deferRender: true,
            lengthMenu: [
                [15, 25, 50, 100],
                [15, 25, 50, 100]
            ],
            language: {
                url: "https://sekhmet.enginy.eu/vendor/datatables/datatables.ca.json"
            },
            columns: [{
                title: "Acció",
                data: "0",
                responsivePriority: 1,
                className: "align-middle",
                render: function(data, _type, _row, _meta) {
                    if (data == 1) {
                        return "<i class='fas fa-sign-in-alt'><p hidden>Entrada</p></i>";
                    } else if (data == 2) {
                        return "<i class='fas fa-sign-out-alt'><p hidden>Sortida</p></i>";
                    } else if (data == 4) {
                        return "<i class='fas fa-key'><p hidden>Cambiar contrasenya</p></i>";
                    } else if (data == 5) {
                        return "<i class='fas fa-pencil-alt'><p hidden>Usuari editat</p></i>";
                    } else if (data == 6) {
                        return "<i class='fas fa-user-edit'><p hidden>Auto editat</p></i>";
                    } else if (data == 7) {
                        return "<i class='fas fa-user-plus'><p hidden>Usuari afegit</p></i>";
                    } else if (data == 8) {
                        return "<i class='fas fa-edit' ><p hidden>Telefon editat</p></i>";
                    } else if (data == 9) {
                        return "<i class='fas fa-address-book'><p hidden>Telefon afegit</p></i>";
                    } else if (data == 10) {
                        return "<i class='fas fa-phone-slash'><p hidden>Telefon eliminat</p></i>";
                    } else {
                        return "<i class='fas fa-user-alt-slash'><p hidden>Invalid</p></i>";
                    }
                }
            }, {
                title: "Hora",
                data: "1",
                responsivePriority: 4,
                className: "align-middle"
            }, {
                title: "IP",
                data: "2",
                responsivePriority: 3,
                className: "align-middle",
                render: function(data, _type, _row, _meta) {
                    if (data) {
                        return intToIP(data);
                    }
                }

            }, {
                title: "Nom",
                data: "3",
                responsivePriority: 2,
                className: "align-middle"
            }, {
                title: "Correu electrònic",
                data: "4",
                responsivePriority: 5,
                className: "align-middle"
            }, {
                title: "Nivell d'usuari",
                data: "5",
                orderable: false,
                className: "align-middle",
                responsivePriority: 6,
                render: function(data, _type, _row, _meta) {
                    if (data == 1) {
                        return "Usuari";
                    } else if (data == 2) {
                        return "Operador";
                    } else if (data == 3) {
                        return "Administrador";
                    } else {
                        return "Deshabilitat";
                    }
                }
            }],
            infoCallback: function() {
                return "";
            },
            drawCallback: function(settings) {},
            order: [
                [1, 'desc']
            ],
            ajax: {
                url: "/log/list",
                method: 'POST',
                dataSrc: function(data) {
                    if (data.result) {
                        localStorage.setItem("alert", 1);
                        location.reload();
                    }
                    return data;
                },
            }
        });

        $('#filtro').on('keyup', function() {
            tableRecords.search(this.value).draw();
        });

        $('button').on('click', function() {
            tableRecords.search(this.value).draw();
        });
    }

    // Crea la taula per administrar els usuaris existents a l'aplicació
    function tableUsers() {
        $.fn.dataTable.ext.search.push(
            function(settings, searchData, index, rowData, counter) {
                if (searchData[2] == 'Deshabilitat') {
                    return false;
                }
                return true;
            });

        table = $("#table2").DataTable({
            scrollCollapse: false,
            paging: true,
            retrieve: true,
            responsive: true,
            deferRender: true,
            lengthMenu: [
                [15, 25, 50, 100],
                [15, 25, 50, 100]
            ],
            order: [
                [0, "asc"]
            ],
            language: {
                url: "https://sekhmet.enginy.eu/vendor/datatables/datatables.ca.json"
            },
            columns: [{
                title: "Nom:",
                data: "1",
                responsivePriority: 1,
                className: "align-middle"
            }, {
                title: "Data de creació:",
                data: "3",
                responsivePriority: 5,
                className: "align-middle"
            }, {
                title: "Nivell d'usuari:",
                data: "4",
                responsivePriority: 4,
                className: "align-middle",
                render: function(data, _type, _row, _meta) {
                    if (data == 1) {
                        return "Usuari";
                    } else if (data == 2) {
                        return "Operador";
                    } else if (data == 3) {
                        return "Administrador";
                    } else {
                        return "Deshabilitat";
                    }
                }
            }, {
                title: "Correu electrònic:",
                data: "5",
                responsivePriority: 3,
                className: "align-middle"
            }, {
                data: "0",
                orderable: false,
                responsivePriority: 2,
                render: function(data, _type, _row, _meta) {
                    if (usrlvl == 3) {
                        return "<button type='button' class='btn btn-primary editarUsr' value='" + data + "' data-bs-toggle='modal' data-bs-target='#editUser'><i class='fas fa-edit'></i></button>"
                    } else {
                        return "";
                    }
                }
            }],
            infoCallback: function() {
                return "";
            },
            drawCallback: function(settings) {
                if (usrlvl == 3) {
                    $('#table2_filter').html('')
                        .append("<button type='button' class='btn btn-primary' style='width:40px;height:40px;display:flex;justify-content:center;align-items: center;'data-bs-toggle='modal' data-bs-target='#addUser'><li class='fas fa-user-plus'></li></button>");
                } else {
                    $('#table2_filter').html('').append('<p class="mt-5"></p>');
                }
            },
            ajax: {
                url: "/user/list",
                method: 'POST',
                dataSrc: function(data) {
                    if (data.result) {
                        localStorage.setItem("alert", 1);
                        location.reload();
                    }
                    return data;
                },
            }
        });

    }
    // Truca als missatges d'error
    $("#rePassModal").keyup(function() {
        errorPass($("#passModal").val(), $("#rePassModal").val(), "#error")
    });

    $("#passModal").keyup(function() {
        errorPass($("#passModal").val(), $("#rePassModal").val(), "#error")
    });

    $("#addUserBtn").click(function() {
        if ($("#passModal").val() == $("#rePassModal").val() && $("#modalname").val() != "" && $("#mailModal").val() != "") {
            $.post("/user/add", {

                nom: $("#modalname").val(),
                pass: hex_md5($("#passModal").val()),
                mail: $("#mailModal").val(),
                lvl: $("#modalpermissions").val()

            }, (data, textStatus, jqXHR) => {
                if (data.result == "mail-exists") {
                    showAlert(4, 0);
                } else {
                    $("#modalname").val("");
                    $("#passModal").val("");
                    $("#rePassModal").val("");
                    $("#mailModal").val("");
                    $("#addUser").modal('toggle');
                    table.ajax.reload();
                    showAlert(10, 2);
                }
            }, "json").fail((jqXHR, textStatus, errorNumber) => {
                console.log("Fallo " + errorNumber);
                showAlert(13, 0, " de BBDD al afegir un usuari. Contacta a l'administrador");
            });
        } else {
            showAlert(9, 0);
        }
    });

    // Posa les dades de cada usuari als inputs quan cliques editar
    $(document).on("click", ".editarUsr", function() {
        $.post("/user/show_one", {
            uid: $(this).attr("value")
        }, (data, textStatus, jqXHR) => {
            if (data.result == "sessio_err") {
                localStorage.setItem("alert", 1);
                location.reload();
            }
            $("#modalNameEdit").val(data[0][1]);
            $("#mailModalEdit").val(data[0][5]);
            $("#permissionsModalEdit").val(data[0][4]);
            $("#uidModalEdit").val(data[0][0]);
            emailEdit = data[0][5];
        }, "json").fail((jqXHR, textStatus, errorNumber) => {
            console.log("Fallo " + errorNumber);
            showAlert(13, 0, "de BBDD al mostrar un usuari. Contacta a l'administrador");
        });
    });

    // Botó per editar un usuari(Només admin), envia les dades a canviar
    $("#editUserBtn").click(function() {
        if ($("#modalNameEdit").val() != "" && $("#mailModalEdit").val() != "") {
            let email = $("#mailModalEdit").val();
            let datos;
            if (email != emailEdit) {
                datos = { nom: $("#modalNameEdit").val(), mail: email, lvl: $("#permissionsModalEdit").val(), uid: $("#uidModalEdit").val(), option: "0" };
            } else {
                datos = { nom: $("#modalNameEdit").val(), mail: email, lvl: $("#permissionsModalEdit").val(), uid: $("#uidModalEdit").val(), option: "1" };
            }
            $.post("/user/edit", datos, (data, textStatus, jqXHR) => {
                if (data.result && email != emailEdit) {
                    showAlert(4, 0);
                } else if (data.result) {
                    showAlert(8, 0);
                } else {
                    $("#editUser").modal('toggle');
                    table.ajax.reload();
                    showAlert(7, 2);
                }
            }, "json").fail((jqXHR, textStatus, errorNumber) => {
                console.log("Fallo " + errorNumber);
                showAlert(13, 0, " de BBDD al editar un usuari. Contacta a l'administrador");
            });
        } else {
            showAlert(9, 0);
        }
    });

    // Treu les dades del modal i reinicia l'error
    $("#closeAddBtn").click(function() {
        $("#modalname").val("");
        $("#passModal").val("");
        $("#rePassModal").val("");
        $("#mailModal").val("");
    });
});

// Missatges d'errors
function errorPass(contr, recontr, error) {
    if (contr != recontr) {
        $(error).html(msg);
        $(error).show();
    } else if (recontr == "") {
        $(error).hide();
    } else if (contr == recontr) {
        $(error).hide();
    }
}
// Torna la IP en nombre enter (int) del servidor a una IP
// per mostrar - la en la taula.
function intToIP(int) {
    let part1 = int & 255;
    let part2 = ((int >> 8) & 255);
    let part3 = ((int >> 16) & 255);
    let part4 = ((int >> 24) & 255);

    return part4 + "." + part3 + "." + part2 + "." + part1;
}