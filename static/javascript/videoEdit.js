$( document ).ready(function() {
    $("#videoDelete").click(deleteVideoEvent);
    $("#videoEdit").click(editEvent);
    $("#EditSubmit").click(editSubmitEvent);
    $('#btnDownload').click(download)
});

function deleteVideoEvent(){
    $.ajax({
        type: 'POST',
        url: "/videoEdit/delete",
        data:JSON.stringify ({
            id:$("#id").val()
        }),
        success: function(data){
            if(data.result){
                alert("刪除成功")
                window.location.href="/videoManage"
            }
        },
        contentType: "application/json",
        dataType: 'json'
    });
}

function editEvent(){
    if( $("#videoEdit").text() == "編輯資料"){
        $("#editPanel").show();
        $("#videoEdit").text("取消修改");
    }
    else{
        $("#editPanel").hide();
        $("#videoEdit").text("編輯資料");
    }
}
function editSubmitEvent(){
    var formData = new FormData($('#editForm')[0]);
    $.ajax({
        url: '/videoEdit',
        type: 'POST',
        cache: false,
        data:formData,
        processData: false,
        contentType: false
    }).done(function(res) {
        if(res.result){
            alert("更新成功");
            window.location.reload();
        }
    }).fail(function(res) { console.log(res);});
}

function download(id){
    filename = id.split('/')[2]
    $.ajax({
        url: '/download/' + filename,
        type: 'GET',
        cache: false,
        processData: false,
        contentType: false
    });
}

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