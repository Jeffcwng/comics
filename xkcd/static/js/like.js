$(document).ready(function () {

    $('#like_this').on('click', function () {
       var checkin = "True";
        console.log('making ajax post');

        $.ajax({
            url: "/random_search/",
            type: "POST",
            dataType: "json",
            data: checkin,
            success: function(response) {
                console.log(response);
                url = response[0]['url'];
                window.location.href = url;
            },
            error: function(response){
                console.log(response);
            }

        });


    });

        function Refresh() {
        window.parent.location = window.parent.location.href;
         }

       $('#find_new_cartoon').on('click', function () {
       var checkin = "True";
        console.log('finding a new cartoon');
        Refresh();


    });


});