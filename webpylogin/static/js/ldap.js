$(document).ready(function() {
    if (ldap == true) {
        $(".ldapRemove").remove();
        $("#ldapBtn").addClass("mt-5");
        $("#submitLoginBtn").addClass("my-1");
    }
});