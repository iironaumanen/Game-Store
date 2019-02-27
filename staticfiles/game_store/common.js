$(document).ready(function() {
    $('#search-button').click(function(e) {
        var site = $('#search-field').val();
        window.location.href = "/game/?game_title=" + site;
    });

    $('search-field').keypress(function (e) {
        alert("testi");
        if (e.which == 13) {
            var site = $('#search-field').val();
            window.location.href = "/game/?game_title=" + site;
            e.preventDefault();
        }
    });
});