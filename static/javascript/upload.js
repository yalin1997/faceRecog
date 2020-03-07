$( document ).ready(function() {
    $("#uploaded_file").change(uploadFileChange);
    $("#confirm").click(function(){
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
        }).fail(function(res) { console.log(res);});
    });
});
function uploadFileChange(){
    var picType =  ['jpg', 'png', 'jpeg'];
    var videoType =  ['avi','mp4' ,'MOV' , 'MTS'];
    var fileType = getFileExtension3($("#uploaded_file").val());
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
}
function getFileExtension3(filename) {
    return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
}

