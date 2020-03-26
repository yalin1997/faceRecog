$( document ).ready(function() {
    var task_id = WebUploader.Base.guid(); // 產生 task_id
    var list = $('#thelist');
    var uploader = WebUploader.create({
        swf: './static/webuploader/Uploader.swf',
        server: '/uploadApart', // 上傳 URL
        pick: '#picker',
          // 只允許圖片影片。
        /*accept: {
            title: 'imageVideo',
            extensions: 'jpg,jpeg,bmp,png,avi,mp4,mov,MTS',
            mimeTypes: 'image/*,video/*'
        },*/
        chunked: true,
        chunkSize: 20 * 1024 * 1024,
        chunkRetry: 3,
        threads: 1,
        duplicate: true,
        formData: { // 每次上傳附帶的資料
            task_id: task_id
        },
    });
    // 選好文件之後觸發
    uploader.on( 'fileQueued', function( file ) {
        var picType =  ['jpg', 'png', 'jpeg'];
        var videoType =  ['avi','mp4' ,'MOV' , 'MTS'];
        var fileType = getFileExtension3(file.name);
        list.append( '<div id="' + file.id + '" class="item">' +
        '<h4 class="info">' + file.name + '</h4>' +
        '<p class="state">等待上傳...</p>' +
        '</div>' );
        if(fileType != ""){
            if(picType.indexOf(fileType) != -1){
                $("#picUploadMsg").show();
                $("#videoUploadMsg").hide();
                $("#lastName").prop("required",true);
                $("#firstName").prop("required",true);
                $("#className").prop("required",false);
                $("#date").prop("required",false);
                $("#time").prop("required",false);
            }
            else if(videoType.indexOf(fileType) != -1){
                $("#videoUploadMsg").show();
                $("#picUploadMsg").hide();
                $("#lastName").prop("required",false);
                $("#firstName").prop("required",false);
                $("#className").prop("required",true);
                $("#date").prop("required",true);
                $("#time").prop("required",true);
            }
        }
    });
    uploader.on('uploadProgress', function(file, percentage) {
        $('.progress-bar').css('width', percentage * 100 - 1 + '%');
        $('.progress-bar').text(Math.floor(percentage * 100 - 1) + '%');
    });

    uploader.on('uploadSuccess', function(file) { // 整個文件成功上傳觸發
        var data = { 
            'task_id': task_id,
            'filename': file.source['name'],
            'lastName': $("#lastName").val(),
            'firstName':  $("#firstName").val(),
            'classId':  $("#classId").val(),
            'videoName':  $("#videoName").val(),
            'className':  $("#className").val(),
            'dateTime':  $("#dateTime").val(),
            'classNo':  $("#classNo").val() 
        };
        $.get('/uploadSuccess', data);
        $('.progress-bar').css('width', '100%');
        $('.progress-bar').text('100%');
        $('.progress-bar').addClass('progress-bar-success');
        $('.progress-bar').text('上傳成功');
        alert("上傳成功");
        window.location.reload();
    });
    uploader.on('uploadError', function(file) { // 上傳失敗事件
        alert("上傳失敗，請確認網路狀態或聯絡管理人員");
    });

    $("#confirm").click(function() {
        $("#confirm").hide();
        uploader.upload();
    });
    $("#confirm_user").click(function(){
        var formData = new FormData($('#uploadForm')[0]);
        $("#uploadPanel").html("<div class='lds-spinner' style='width:100%;height:100%'><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>")
        $.ajax({
            url: '/upload',
            type: 'POST',
            cache: false,
            data:formData,
            processData: false,
            contentType: false
        }).done(function(res) {
            if(res.result == true){
                alert("上傳成功");
                window.location.reload(); 
            }
            else{
                alert(res.result);
            }
        }).fail(function(res){
            console.log(res);
        });  
    });   
});

function getFileExtension3(filename) {
    return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
}

