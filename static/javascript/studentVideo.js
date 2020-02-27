$( document ).ready(function() {
    fillinDate();
});
function filterEvent(){
    csrfVal = $("#csrf_token").val();
    studentIdVal = location.search.split("&")[0].split("=")[1];
    classIdVal = location.search.split("&")[1].split("=")[1];
    sdateVal = $("#sdate").val();
    edateVal = $("#edate").val();
    classNoVal = $("#classNo").val();
    $.ajax({
        type: 'POST',
        url: '/studentVideo',
        contentType: 'application/json',
        dataType: 'json',
        data:JSON.stringify({
                    csrf_token: csrfVal,
                    studentId : studentIdVal,
                    classId : classIdVal,
                    sdate: sdateVal,
                    edate: edateVal,
                    classNo: classNoVal}),
        success: createCard
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
        var card = "<div class='card' id='card_" + data.allMatchData[i].id + "' style='width:92%;max-width:300px;' onclick='CardClickedEvent(id)'>"+
            "<div class='card-header'>" + data.allMatchData[i].date + " " + data.allMatchData[i].name+"</div>"+
                "<img src='" + data.allMatchData[i].videoUrl +"' alt='Avatar' style='width:100%;opacity:0.85'>"+
            "<div class='container'>"+
                "<p>第" + data.allMatchData[i].classNo + "節</p>"+  
                " <button class='btn btn-primary my-btn' id='delete_" + data.allMatchData[i].id + "' onclick='deleteEvent(id)'>刪除影片</button>"+
            "</div>"+
        "</div>"
        content+=card;
    }
    $("#renderVideoArea").html(content);
}

function CardClickedEvent(id){
    window.location = "/videoEdit?videoId=" + id.split("_")[1];
}

