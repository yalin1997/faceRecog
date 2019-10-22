
function deleteEvent(targetId){
    $.ajax({
        type: 'POST',
        url: '/studentsEdit/delete',
        data:  JSON.stringify ({id: targetId.split("_")[1]}), // or JSON.stringify ({name: 'jonas'}),
        success: function(data) {  
            alert("刪除成功");
            window.location.href="/pictureManage";
        },
        contentType: "application/json",
        dataType: 'json'
    });
}
function addClassMember(id){
    window.location = "/addClassMember?classId=" + id;
}
function clickFacePicture(facePictureId){
    window.location = "/studentsEdit?faceId=" + facePictureId.split("_")[1];
}
function filterEvent(id){
    $.ajax({
        type: 'POST',
        url: '/studentsManage',
        data:JSON.stringify ({
                    csrf_token: $("#csrf_token").val(),
                    classId: id,
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

        if(data.allMatchData[i].isDataComplete){
            var card = "<div class='panel panel-primary studentPanel' style='width: 18rem;'>"+
                        " <div class='panel-heading'>"+
                            "<h5 class='panel-title'>"+data.allMatchData[i].lastname + data.allMatchData[i].firstname +"</h5>"+
                         "</div>"+
                        "<div class='panel-body'>"+    
                            "<img src='"+ data.allMatchData[i].faceUrl +"' title='fuck you chrome' class='img-circle studentManage' id='facePicture_"+data.allMatchData[i].id+"' onclick='clickFacePicture(id)'>"+   
                            "<div class='btn-group'>"+
                            "<button type='button' class='btn btn-primary my-btn dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>"+
                                "功能"+
                            "</button>"
                            "<div class='dropdown-menu'>"+
                              "<li><a class='dropdown-item' href='/studentInfo?studentId={{ student.id }}'>查看資料</a></li>"+
                              "<li><a class='dropdown-item' href='/studentVideo?studentId={{ student.id }}&classId={{ classId }}'>上課影片</a></li>"+
                              "<li><div class='dropdown-divider'></div></li>"+
                              "<li><a href='#' id='delete_{{ student.id }}' class='btn btn-primary my-btn' onclick='deleteEvent(id)'>刪除</a></li>"+
                            "</div>"+
                        "</div>"+
                        "<a href='#' id='delete_{{ student.id }}' class='btn btn-danger my-btn' onclick='deleteEvent(id)'>刪除</a>"+
                        "</div>"+
                        "</div>";
        }
        else{
            var card = "<div class='panel panel-danger studentPanel' style='width: 18rem;'>"+
                        " <div class='panel-heading'>"+
                            "<h5 class='panel-title'>"+data.allMatchData[i].lastname + data.allMatchData[i].firstname +"(資料未齊全)</h5>"+
                         "</div>"+
                        "<div class='panel-body'>"+    
                            "<img src='"+ data.allMatchData[i].faceUrl +"' title='fuck you chrome' class='img-circle studentManage' id='facePicture_"+data.allMatchData[i].id+"' onclick='clickFacePicture(id)'>"+   
                            "<div class='btn-group'>"+
                            "<button type='button' class='btn btn-primary my-btn dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>"+
                                "功能"+
                            "</button>"
                            "<div class='dropdown-menu'>"+
                              "<li><a class='dropdown-item' href='/studentInfo?studentId={{ student.id }}'>查看資料</a></li>"+
                              "<li><a class='dropdown-item' href='/studentVideo?studentId={{ student.id }}&classId={{ classId }}'>上課影片</a></li>"+
                              "<li><div class='dropdown-divider'></div></li>"+
                              "<li><a href='#' id='delete_{{ student.id }}' class='btn btn-primary my-btn' onclick='deleteEvent(id)'>刪除</a></li>"+
                            "</div>"+
                        "</div>"+
                        "<a href='#' id='delete_{{ student.id }}' class='btn btn-danger my-btn' onclick='deleteEvent(id)'>刪除</a>"+
                        "</div>"+
                        "</div>";
        }
        content+=card;
    }

    $("#renderStudentsArea").html(content);
}