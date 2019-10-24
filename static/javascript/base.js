
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

function createLoader(){
    return $('<div class="lds-ring"><div></div><div></div><div></div><div></div></div>');
}