
function deleteEvent(targetId){
    if(confirm("確定要刪除嗎?")){
        $.ajax({
            type: 'POST',
            url: '/studentsEdit/delete',
            data:  JSON.stringify ({id: targetId.split("_")[1]}), // or JSON.stringify ({name: 'jonas'}),
            success: function(data) {  
                alert("刪除成功");
                window.location.reload();
            },
            contentType: "application/json",
            dataType: 'json'
        });
    }
}
function addClassMember(id){
    window.location = "/addClassMember?classId=" + id;
}
function clickFacePicture(facePictureId){
    window.location = "/studentInfo?studentId=" + facePictureId.split("_")[1];
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
    var content = "";
 
    for(var i = 0;i < data.allMatchData.length;i++){

        if(data.allMatchData[i].isDataComplete){
            
            var card =  "<div class='card card-primary studentPanel col-12 col-md-5 col-lg-3'>"+
                            "<div class='card-body'>"+
                                "<img src='{{ student.faceUrl }}' title = '點擊畫面觀看細節' alt='Responsive image' class='img-circle studentManage' id='facePicture_{{ student.id }}' onclick='deleteEvent(id)'>"+
                                "<h5 class='card-title'>{{ student.lastname }}{{ student.firstname }}</h5>"+
                                "<div class='form-group d-flex flex-row-reverse'>"+
                                    "<button type='button' id='delete_{{ student.id }}' class='btn btn-danger m-1' onclick='deleteEvent(id)'>刪除</button>"+
                                    "<button type='button' class='btn btn-primary my-btn dropdown-toggle m-1' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>"+
                                        "功能"+
                                    "</button>"+
                                    "<div class='dropdown-menu'>"+
                                        "<li><a class='dropdown-item' href='/studentInfo?studentId={{ student.id }}'>查看資料</a></li>"+
                                        "<li><a class='dropdown-item' href='/studentVideo?studentId={{ student.id }}&classId={{ classId }}'>上課影片</a></li>"+
                                    "</div>"+
                                "</div>"+
                            "</div>"+ 
                        "</div>";
        }
        else{
            var card = "<div class='card card-danger studentPanel col-12 col-md-5 col-lg-3'>"+
                        "<div class='card-body'>"+
                            "<img src='{{ student.faceUrl }}' title = '點擊畫面觀看細節' alt='Responsive image' class='img-circle studentManage' id='facePicture_{{ student.id }}' onclick='deleteEvent(id)'>"+
                            "<h5 class='card-title'>{{ student.lastname }}{{ student.firstname }}  (資料未完善)</h5>"+
                            "<div class='form-group d-flex flex-row-reverse'>"+
                                "<button type='button' id='delete_{{ student.id }}' class='btn btn-danger m-1' onclick='deleteEvent(id)'>刪除</button>"+
                                "<button type='button' class='btn btn-primary my-btn dropdown-toggle m-1' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>"+
                                    "功能"+
                                "</button>"+
                                "<div class='dropdown-menu'>"+
                                    "<li><a class='dropdown-item' href='/studentInfo?studentId={{ student.id }}'>查看資料</a></li>"+
                                    "<li><a class='dropdown-item' href='/studentVideo?studentId={{ student.id }}&classId={{ classId }}'>上課影片</a></li>"+
                                "</div>"+
                            "</div>"+
                        "</div>";
        }
        content+=card;
    }

    $("#renderStudentsArea").html(content);
}