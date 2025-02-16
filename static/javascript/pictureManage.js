$( document ).ready(function() {
    $("#startFilter").click(filterEvent);

});
function deleteEvent(targetId){
    $.ajax({
        type: 'POST',
        url: '/pictureEdit/delete',
        data:  JSON.stringify ({id: targetId.split("_")[1]}), // or JSON.stringify ({name: 'jonas'}),
        success: function(data) {  
            alert("刪除成功");
            window.location.href="/pictureManage";
        },
        contentType: "application/json",
        dataType: 'json'
    });
}
function clickFacePicture(facePictureId){
    window.location = "/pictureEdit?pictureId=" + facePictureId.split("_")[1];
}
function filterEvent(){
    $.ajax({
        type: 'POST',
        url: '/pictureManage',
        data:JSON.stringify ({
                    csrf_token: $("#csrf_token").val(),
                    lastName: $("#lastName").val(),
                    firstName:$("#firstName").val()}),
        success: createCard,
        contentType: "application/json",
        dataType: 'json'
    });
}
function createCard(data){
    var content = ""
 
    for(var i = 0;i < data.allMatchData.length;i++){

        var card = "<div class='panel panel-primary pucturePanel' style='width: 18rem;'>"+
                        " <div class='panel-heading'>"+
                            "<h5 class='panel-title'>"+data.allMatchData[i].lastname + data.allMatchData[i].firstname +"</h5>"+
                         "</div>"+
                        "<div class='panel-body'>"+    
                            "<img src='"+ data.allMatchData[i].pictureUrl +"' title='fuck you chrome' class='img-circle pictureManage' id='facePicture_"+data.allMatchData[i].id+"' onclick='clickFacePicture(id)'>"+   
                            "<a href='/pictureEdit?pictureId="+data.allMatchData[i].id+"' class='btn btn-primary my-btn'>編輯</a>"+ 
                            "<a href='#' id='delete_"+data.allMatchData[i].id +"' class='btn btn-primary my-btn' onclick='deleteEvent(id)'>刪除</a>"+
                        "</div>"+
                    "</div>";
        content+=card;
    }

    $("#renderPictureArea").html(content);
}
