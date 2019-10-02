$( document ).ready(function() {
    $("#videoDelete").click(deleteVideoEvent);
    $("#videoEdit").click(editEvent);
    $("#EditSubmit").click(editSubmitEvent);
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
    if( $("#videoEdit").text() == "編輯"){
        $("#editPanel").show();
        $("#videoEdit").text("取消修改");
    }
    else{
        $("#editPanel").hide();
        $("#videoEdit").text("編輯");
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