/**
 * Created by miguelbarbosa on 10/23/14.
 */


$(document).ready(function() {
    $("#register").click(function () {

      mixpanel.identify($("#id_username").val());
      mixpanel.people.set({
            "$username": $("#id_username").val(),
            "$first_name":$("#id_first_name").val(),
            "$last_name": $("#id_last_name").val(),
            "$email": $("#id_email").val()
        });

    });
});



$(document).ready(function() {
    $("#like_this").click(function () {
        mixpanel.track("Like button clicked");
    });
});

$(document).ready(function() {
    $("#login").click(function () {
        mixpanel.track("Logged In");
    });
});

