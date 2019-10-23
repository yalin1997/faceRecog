$( document ).ready(function() {
    $("#startFilter").click(filterEvent);
    fillinDate();
});

function pustInRecogQueue(videoId){
    $.ajax({
        type: 'POST',
        url: '/videoRecog',
        data:JSON.stringify ({
            videoId : videoId
                    }),
        success: function(data){
            if (data.result == true){
                alert("已經加入辨識");
                location.reload();
            }
            else{
                alert( "失敗! 原因 : " + data.result );
            }
        },
        contentType: "application/json",
        dataType: 'json'
    });
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
        coverPath = "/upload/others/img_avatar.jpg"
        if(data.allMatchData[i].pictureUrl != ""){
            coverPath = data.allMatchData[i].pictureUrl
        }
        
        var card = "<div class='card' id='card_"+data.allMatchData[i].id+"' style='width:92%;max-width:300px;' onclick='CardClickedEvent(id)'>"+
                        "<img src='"+coverPath+"' alt='Avatar' style='width:100%;opacity:0.85'>"+
                        "<div class='container'>"+
                            "<h5><b>"+data.allMatchData[i].title+"</b></h5>"+    
                            "<p>"+data.allMatchData[i].people+"</p>"+   
                        "</div>"+ 
                    "</div>";
        content+=card;
    }

    $("#renderVideoArea").html(content);
}
function CardClickedEvent(id){
    window.location = "/videoEdit?videoId=" + id.split("_")[1];
}

