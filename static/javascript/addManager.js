function sentManagerData(){
    var formData = new FormData($('#addManagerForm')[0]);
    $.ajax({
        url: '/addManager',
        type: 'POST',
        cache: false,
        data:formData,
        processData: false,
        contentType: false
    }).done(function(data) {
        if (data.result){
            alert('新增完成!');
        }
        else{
            alert(data.result);
        }
    }).fail(function(res) { alert("發生異常，請檢察網路狀況!");});
}
