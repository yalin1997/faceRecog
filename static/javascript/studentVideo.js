$( document ).ready(function() {
    $("#startFilter").click(filterEvent);
    fillinDate();
});
function filterEvent(){
    csrfVal = $("#csrf_token").val();
    studentId = location.search.split("&")[0].split("=")[1];
    classId = location.search.split("&")[1].split("=")[1];
    sdateVal = $("#sdate").val();
    edateVal = $("#edate").val();
    classNo = $("#classNo").val();
    $.ajax({
        type: 'POST',
        url: '/studentVideo',
        contentType: "application/json",
        dataType: 'json',
        data:JSON.stringify ({
                    csrf_token: csrfVal,
                    studentId : studentId,
                    classId : classId,
                    sdate: sdateVal,
                    edate: edateVal,
                    classNo: classNo}),
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
        coverPath = "/upload/others/img_avatar.jpg"
        if(data.allMatchData[i].pictureUrl != ""){
            coverPath = data.allMatchData[i].pictureUrl
        }
        
        var card = "<div class='card' id='card_"+data.allMatchData[i].id+"' style='width:92%;max-width:300px;' onclick='CardClickedEvent(id)'>"+
                        "<img src='"+coverPath+"' alt='Avatar' style='width:100%;opacity:0.85'>"+
                        "<div class='container'>"+
                            "<h5><b>"+data.allMatchData[i].date+"</b></h5>"+    
                            "<p>"+data.allMatchData[i].classNo+"</p>"+   
                        "</div>"+ 
                    "</div>";
        content+=card;
    }

    $("#renderVideoArea").html(content);
}
function CardClickedEvent(id){
    //window.location = "/videoEdit?videoId=" + id.split("_")[1];
}

