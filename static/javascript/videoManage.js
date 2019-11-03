$( document ).ready(function() {
    fillinDate();
});

function pustInRecogQueue(videoId){
    $("#"+videoId).hide();
    $.ajax({
        type: 'POST',
        url: '/videoRecog',
        data:JSON.stringify ({
            videoId : videoId
                    }),
        success: function(data){
            if (data.result == true){
                alert("已經加入辨識，請耐心等待");
            }
            else{
                alert( "失敗! 原因 : " + data.result );
            }
        },
        contentType: "application/json",
        dataType: 'json'
    });
}

function deleteEvent(targetId){
    if(confirm("確定要刪除嗎?")){
        $.ajax({
            type: 'POST',
            url: '/videoEdit/delete',
            data:  JSON.stringify ({id: targetId.split("_")[1]}),
            success: function() {  
                alert("刪除成功");
                window.location.reload();
            },
            contentType: "application/json",
            dataType: 'json'
        });
    }
}
function filterEvent(id){
    csrfVal = $("#csrf_token").val() == ""? "0" : $("#csrf_token").val();
    lastNameVal =  $("#lastName").val() == ""?  "0" : $("#lastName").val();
    firstNameVal = $("#firstName").val() == ""?  "0" : $("#firstName").val();
    sdateVal = $("#sdate").val() == ""?  "0" : $("#sdate").val();
    edateVal = $("#edate").val() == ""?  "0" : $("#edate").val();
    classNoVal = $("#classNo").val() == ""? "0" : $("#classNo").val();
    $.ajax({
        type: 'POST',
        url: '/videoManage',
        data:JSON.stringify ({
                    csrf_token: csrfVal,
                    classId: id,
                    lastName: lastNameVal,
                    firstName: firstNameVal,
                    sdate: sdateVal,
                    edate: edateVal,
                    classNo: classNoVal}),
        success: createCard,
        contentType: "application/json",
        dataType: 'json'
    });
}
function fillinDate(){
    var Today=new Date().toISOString().slice(0,10);
    $("#sdate").val(Today);
    $("#edate").val(Today);
}
function createCard(data){
    var content = ""

    for(var i = 0;i < data.allMatchData.length;i++){
        if(data.allMatchData[i].isRecoged == 1){
            var card = "<div class='card' id='card_" + data.allMatchData[i].id + "' style='width:92%;max-width:300px;' onclick='CardClickedEvent(id)'>"+
                "<div class='card-header'>" + data.allMatchData[i].date + "</div>"+
                    "<img src='" + data.allMatchData[i].videoUrl +"' alt='Avatar' style='width:100%;opacity:0.85'>"+
                "<div class='container'>"+
                    "<p>第" + data.allMatchData[i].classNo + "節</p>"+  
                    " <button class='btn btn-primary my-btn' id='delete_" + data.allMatchData[i].id + "' onclick='deleteEvent(id)'>刪除影片</button>"+
                "</div>"+
            "</div>"
        }
        else if(data.allMatchData[i].isRecoged == 2){
            var card = "<div class='card bg-warning text-white' id='card_" + data.allMatchData[i].id + "' style='width:92%;max-width:300px;' onclick='CardClickedEvent(id)'>"+
                            "<div class='card-header'>" + data.allMatchData[i].date +" (辨識中)"+ "</div>"+
                                "<img src='" + data.allMatchData[i].videoUrl +"' alt='Avatar' style='width:100%;opacity:0.85'>"+
                            "<div class='container'>"+
                                "<p>第" + data.allMatchData[i].classNo + "節</p>"+  
                            "</div>"+
                        "</div>"
        }
        else{

            var card = "<div class='card text-white bg-danger' id='card_" + data.allMatchData[i].id + "' style='width:92%;max-width:300px;' onclick='CardClickedEvent(id)'>"+
                            "<div class='card-header'>" + data.allMatchData[i].date +" (尚未辨識)"+ "</div>"+
                                "<img src='" + data.allMatchData[i].videoUrl +"' alt='Avatar' style='width:100%;opacity:0.85'>"+
                            "<div class='container'>"+
                                "<p>第" + data.allMatchData[i].classNo + "節</p>"+  
                                " <button class='btn btn-primary my-btn' id='" + data.allMatchData[i].id + "' onclick='pustInRecogQueue(id)'>執行辨識</button>"+
                                " <button class='btn btn-primary my-btn' id='delete_" + data.allMatchData[i].id + "' onclick='deleteEvent(id)'>刪除影片</button>"+
                                "</div>"+
                        "</div>"
        }
        content+=card;
    }
    $("#renderVideoArea").html(content);
}
function CardClickedEvent(id){
    window.location = "/videoEdit?videoId=" + id.split("_")[1];
}

