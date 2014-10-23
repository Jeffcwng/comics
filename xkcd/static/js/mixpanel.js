/**
 * Created by miguelbarbosa on 10/23/14.
 */

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