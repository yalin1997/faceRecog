$( document ).ready(function() {
   $("#login").click(loginEvent);
});
function loginEvent(){
    var formData = new FormData($('#loginForm')[0]);
    $.ajax({
        url: '/login',
        type: 'POST',
        cache: false,
        data:formData,
        processData: false,
        contentType: false
    }).done(function(res) {
        console.log(res);
    }).fail(function(res) { console.log(res);});
}