function sentManagerData(){
    var formData = new FormData($('#addManagerForm')[0]);
    $.ajax({
        type: 'POST',
        url: '/addManager',
        data: formData,
        success: function(data){
            if (data.result == true){
                alert('新增完成!');
            }
            else{
                alert(data.result)
            }
        },
        contentType: "application/json",
        dataType: 'json'
    });
}
