$( document ).ready(function() {
    $("#startFilter").click(filterEvent);

    filterEvent();
});
function filterEvent(){
    var loader = createLoader();
    $("#renderClassGroupArea").empty().append(loader);

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
        dataType: 'json',
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
    var content = "";
    for(var i = 0;i < data.allMatchData.length;i++){

        var card = "<div class='card col-12 col-md-10 col-lg-8 p-0 mt-3'>"+
                        "<h5 class='card-header'>" + data.allMatchData[i].className + "</h5>"+
                        "<div class='card-body'>"+
                            "<p class='card-title'>學年: "+ data.allMatchData[i].classYear +" </p>"+
                            "<p class='card-text'>星期: "+ data.allMatchData[i].classDay +"</p>"+
                            "<div class='d-flex flex-row-reverse'>"+
                                "<a href='#' id='delete_"+ data.allMatchData[i].id +"' class='btn btn-danger my-btn' onclick='deleteEvent(id)'>刪除</a>"+
                                "<button type='button' class='btn btn-primary my-btn dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>"+
                                    "編輯"+
                                "</button>"+
                                "<div class='dropdown-menu'>"+
                                    "<li><a class='dropdown-item' href='/upload?classId="+ data.allMatchData[i].id +"'>上傳影片</a></li>"+
                                    "<li><a class='dropdown-item' href='/videoManage?classId="+ data.allMatchData[i].id +"'>管理影片</a></li>"+
                                    "<li><a class='dropdown-item' href='/studentsManage?classId="+ data.allMatchData[i].id +"'>管理學生</a></li>"+
                                    "<li><a class='dropdown-item' href='/addClassMember?classId="+ data.allMatchData[i].id +"'>加入學生</a></li>"+
                                "</div>"+
                            "</div>"+
                        "</div>"+ 
                    "</div>";
        
        content+=card;
    }

    $("#renderClassGroupArea").html(content);
}