$( document ).ready(function() {
    $("#addNewClass").click(addNewClassEvent);
});

function addNewClassEvent(){
    className = $('#newClassName').val()
    $.ajax({
        type: 'POST',
        url: '/addClassName',
        data:JSON.stringify ({
                    newClassName: className
                }),
        success: function(data){
            if (data.result){
                window.location.reload();
            }
        },
        contentType: "application/json",
        dataType: 'json'
    });
}