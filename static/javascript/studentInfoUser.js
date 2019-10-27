$( document ).ready(function() {
    $(".flexslider").flexslider({
        slideshowSpeed: 5000, //展示时间间隔ms
        animationSpeed: 500, //滚动时间ms
        touch: true //是否支持触屏滑动
    });
});

(function(){
    var editArray = [];
    var editInput = [];
    $("#btnEditInfo").click(function(){
        //var nameContainer = $("<div>名: <input id='editLastName'/> 姓:<input id='editFirstName' class='ml-1' /></div>");
        var editEmail = $("<input id='editEmail' type='email' />");
        //editInput.push(nameContainer);
        editInput.push(editEmail);

        /*var infoName = $("#infoName");
        infoName.children().hide();
        infoName.append(nameContainer);*/

        var infoEmail = $("#infoEmail");
        infoEmail.children().hide();
        infoEmail.append(editEmail);

        //editArray.push(infoName);
        editArray.push(infoEmail);

        $("#btnCancelEditInfo").show();
        $("#btnSubmitInfo").show();
        $(this).hide();
    });


    $("#btnCancelEditInfo").click(function(){
        for (index = 0; index < editInput.length; ++index){
            editInput[index].remove();
        }
        for (index = 0; index < editArray.length; ++index){
            editArray[index].children().show();
        }

        editInput = [];
        editArray = [];

        $("#btnEditInfo").show();
        $("#btnSubmitInfo").hide();
        $(this).hide();
    });

}());

(function(){
    $("#btnEditPassword").click(function(){
        $("#editPassword").show();

        $("#btnEditCancelPassword").show();
        $(this).hide();
    });

    $("#btnEditCancelPassword").click(function(){
        $("#editPassword").hide();
        $("#editPassword").find("input").val("");
        $("#newPasswordConfirmMsg").text("");

        $("#btnEditPassword").show();
        $(this).hide();
    });

    $("#newPasswordConfirm,#newPassword").change(function(){
        if($("#newPassword").val() != $("#newPasswordConfirm").val()){
            $("#newPasswordConfirmMsg").text("與新密碼不相同");
            $("#newPasswordConfirm").css({"border-color": "red"});
        }
        else if($("#newPasswordConfirm").val().length > 0){
            $("#newPasswordConfirmMsg").text("");
            $("#newPasswordConfirm").css({"border-color": "green"});
        }else{
            $("#newPasswordConfirmMsg").text("");
            $("#newPasswordConfirm").css({"border-color": ""});
        }
    });
})();

(function(){
    $("#btnSubmitInfo").click(function(){
        $.ajax({
            type: 'POST',
            url: '/studentInfo',
            data:JSON.stringify ({
                studentId : location.search.split("=")[1],
                email : $('#editEmail').val()
                        }),
            success: function(data){
                if (data.result == true){
                    alert("修改成功");
                    location.reload();
                }
                else{
                    alert( "失敗! 原因 : " + data.result );
                }
            },
            contentType: "application/json",
            dataType: 'json'
        });
    });

    $("#btnSubmitEditPassword").click(function(){
        $.ajax({
            type: 'POST',
            url: '/studentInfo',
            data:JSON.stringify ({
                studentId : location.search.split("=")[1],
                newPassword : $('#newPassword').val(),
                newPasswordConfirm : $('#newPasswordConfirm').val()
                        }),
            success: function(data){
                if (data.result == true){
                    alert("修改成功");
                    location.reload();
                }
                else{
                    alert( "失敗! 原因 : " + data.result );
                }
            },
            contentType: "application/json",
            dataType: 'json'
        });
    });
})();
