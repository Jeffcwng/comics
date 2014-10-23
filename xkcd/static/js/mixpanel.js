/**
 * Created by miguelbarbosa on 10/23/14.
 */


$(document).ready(function() {
    $("#register").click(function () {
      mixpanel.identify("13487");
      mixpanel.people.set({
            "$username": "Joe",
            "$first_name": "Joe",
            "$last_name": "Joe",
            "$email": "joe.doe@example.com",
            "$created": "2013-04-01T09:02:00"
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

