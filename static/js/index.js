$(document).ready(function(){
    $('select').material_select();
    $('#role').hide();
    $('#privilege').hide();
    $('#table').hide();
});

function user_submit() {
    let name = $('#name').val();
    let UName = $('#u-name').val();
    let address = $('#address').val();
    let phoneNo = $('#PhoneNo').val();
    let password = $('#password').val();

    $.ajax({
        type: "POST",
        url: "/user",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        dataType: 'json',
        data: "Name=" + name + "&UName=" + UName + "&Password=" + password + "&Address=" + address +
            "&PhoneNo=" + phoneNo,

        success: function (data) {
            console.log(data);

            if (data.Status_Code !== 200) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
            } else {
                $('#user').hide();
                $('#role').show();
            }
        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
    });
}

function role_submit() {
    let name = $('#RName').val();
    let Description = $('#Description').val();

    $.ajax({
        type: "POST",
        url: "/role",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        dataType: 'json',
        data: "RName=" + name + "&Description=" + Description,

        success: function (data) {
            console.log(data);
            if (data.Status_Code !== 200) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
            } else {
                $('#role').hide();
                $('#table').show();
            }
        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
    });
}

function table_submit() {
    let name = $('#Tname').val();

    $.ajax({
        type: "POST",
        url: "/table",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        dataType: 'json',
        data: "TName=" + name,

        success: function (data) {
            console.log(data);

            if (data.Status_Code !== 200) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
            } else {
                $('#table').hide();
                $('#privilege').show();
            }
        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
    });
}

function privilege_submit() {
    let name = $('#PName').val();
    let PrivilegeType = $('#PrivilegeType').val();

    $.ajax({
        type: "POST",
        url: "/privilege",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        dataType: 'json',
        data: "PName=" + name + '&PrivilegeType=' + PrivilegeType,

        success: function (data) {
            console.log(data);

            if (data.Status_Code !== 200) {
                Materialize.toast('An error occurred!' + data, 2000, 'red');
            } else {
                window.location.reload(true);
            }
        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
    });
}

function get_privilege_role() {
    let role = $('#select_role').val();

    $.ajax({
        type: "POST",
        url: "/get-privilege-role",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        dataType: 'json',
        data: "Role=" + role,

        success: function (data) {
            console.log(data);

            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"3\"><h6 class='center-align grey-text text-darken-2'>" +
                    "Nothing to display.</h6></td></tr>";
            }
            else {
                for(let i in data.Records) {
                    tr_list += "<tr>";
                    tr_list += "<td>" + data.Records[i].PID + "</td>";
                    tr_list += "<td>" + data.Records[i].PName + "</td>";
                    tr_list += "<td>" + data.Records[i].PrivilegeType + "</td>";
                    tr_list += "</tr>";
                }
            }
            $("#privilege_role").html(tr_list);
        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
    });
}

function get_privilege_user() {
    let username = $('#set_UName').val();

    $.ajax({
        type: "POST",
        url: "/get-privilege-user",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        dataType: 'json',
        data: "UName=" + username,

        success: function (data) {
            console.log(data);

            let tr_list = "";

            if (!data) {
                tr_list += "<tr><td colspan=\"3\"><h6 class='center-align grey-text text-darken-2'>" +
                    "Nothing to display.</h6></td></tr>";
            }
            else {
                for(let i in data.Records) {
                    tr_list += "<tr>";
                    tr_list += "<td>" + data.Records[i].PID + "</td>";
                    tr_list += "<td>" + data.Records[i].PName + "</td>";
                    tr_list += "<td>" + data.Records[i].PrivilegeType + "</td>";
                    tr_list += "</tr>";
                }
            }
            $("#privilege_user").html(tr_list);
        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
    });
}

function check_privilege_user() {
    let username = $('#select_UName').val();
    let PrivilegeType = $('#set_PrivilegeType').val();

    $.ajax({
        type: "POST",
        url: "/check-privilege-user",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        dataType: 'json',
        data: "UName=" + username + "&PrivilegeType=" + PrivilegeType,

        success: function (data) {
            console.log(data);

            let result = "";
            if (data.Result) {
                result += "<div class='chip green'>Permission Grant</div>";
            }
            else if (!data.Result){
                result += "<div class='chip red'>Permission Denied</div>";
            }
            else {
                result += "<div class='chip yellow'>Server Error</div>";
            }
            $("#check_privilege_user").html(result);
        },
        error: function (data) {
            Materialize.toast('An error occurred!' + data, 2000, 'red');
        }
    });
}
