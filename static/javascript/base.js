
function logout(){
    $.ajax({
        type: 'POST',
        url: '/logout',
        success: function(data){
            if (data){
                window.location.replace("/login");
            }
        },
        contentType: "application/json",
        dataType: 'json'
    });
}