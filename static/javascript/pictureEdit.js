$( document ).ready(function() {
    $('#file-selector').change(getUploadPicture);
    $('#confirm').click(confirmEvent);
    $('#deletePicture').click(deleteEvent);
});
function confirmEvent(){
    var formData = new FormData($('#editForm')[0]);
    $.ajax({
        url: '/pictureEdit',
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

function deleteEvent(){
    $.ajax({
        type: 'POST',
        url: '/pictureEdit/delete',
        data:  JSON.stringify ({id: $("#id").val()}), // or JSON.stringify ({name: 'jonas'}),
        success: function(data) {  
            alert("刪除成功");
            window.location.href="/pictureManage";
        },
        contentType: "application/json",
        dataType: 'json'
    });
}

function getUploadPicture(event){
    window.fileList = event.target.files;
    var file = fileList[0];
    // 解析檔案
    var reader = new FileReader();
    reader.onload = (function(file){
        return function(event){
            var pictureUrl = event.target.result	// 圖片的編碼 , 格式為base64
            // 到這邊 , 我們已經能後用js存取圖片並顯示了
            $('#targetPicture').attr("src",pictureUrl);
        };
    })(file);

    reader.readAsDataURL(file);
}