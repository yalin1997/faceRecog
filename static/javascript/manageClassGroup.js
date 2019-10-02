$( document ).ready(function() {
    $("#startFilter").click(filterEvent);
});
function filterEvent(){
    $.ajax({
        type: 'POST',
        url: '/manageClassGroup',
        data:JSON.stringify ({
                    csrf_token: $("#csrf_token").val(),
                    className: $("#className").val(),
                    classDepartment:$("#classDepartment").val(),
                    classYear:$("#classYear").val(),
                    classDay:$("#classDay").val()
                }),
        success: createCard,
        contentType: "application/json",
        dataType: 'json'
    });
}
function deleteEvent(targetId){
    $.ajax({
        type: 'POST',
        url: '/editClassGroup/delete',
        data:  JSON.stringify ({id: targetId.split("_")[1]}),
        success: function(data) {
            alert("刪除成功");
            window.location.href="/manageClassGroup";
        },
        contentType: "application/json",
        dataType: 'json'
    });
}

function createCard(data){
    var content = ""
 
    for(var i = 0;i < data.allMatchData.length;i++){

        var card = "<div class='panel panel-primary classGroupPanel' style='width: 18rem;'>"+
                        " <div class='panel-heading'>"+
                            "<h5 class='panel-title'>"+data.allMatchData[i].className +"</h5>"+
                         "</div>"+
                        "<div class='panel-body'>"+
                            "<a href='/editClassGroup?classGroupId="+data.allMatchData[i].id+"' class='btn btn-primary my-btn'>編輯</a>"+ 
                            "<a href='#' id='delete_"+data.allMatchData[i].id +"' class='btn btn-primary my-btn' onclick='deleteEvent(id)'>刪除</a>"+
                        "</div>"+
                    "</div>";
        content+=card;
    }

    $("#renderClassGroupoArea").html(content);
}