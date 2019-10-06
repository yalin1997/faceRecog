var studentCounter = 1;
function addClassMemberList(){
    var table = document.getElementById("classMemberTable");
    var newRow = table.insertRow(table.rows.length);
    var newCell  = newRow.insertCell(0);
    var newCell2  = newRow.insertCell(1);
    var newCell3  = newRow.insertCell(2);
    var newCell4  = newRow.insertCell(3);
    var newCell5  = newRow.insertCell(4);
    var newCell6  = newRow.insertCell(5);
    newCell.innerHTML = studentCounter
    studentCounter++;
    newCell2.innerHTML = $('input[name="lastName"]').val();
    newCell3.innerHTML = $('input[name="firstName"]').val();
    newCell4.innerHTML = $('input[name="account"]').val();
    newCell5.innerHTML = $('input[name="email"]').val();
    newCell6.innerHTML = "<button class='btn btn-primary'></button>"
}
function sentConfirmClassMember(){
    $.ajax({
        type: 'POST',
        url: '/addClassMember',
        data:JSON.stringify ({'data':getTableData()}),
        success: function(data){
            if (data.result){
                alert('新增完成!');
            }
        },
        contentType: "application/json",
        dataType: 'json'
    });
}
function getTableData(){
    var table = document.getElementById("classMemberTable");
    dataList = [];
    table.find('tr').each(function (i) {
        var $tds = $(this).find('td'),
            lastName = $tds.eq(0).text(),
            firstName = $tds.eq(1).text(),
            account = $tds.eq(2).text(),
            email = $tds.eq(3).text();
        dataList.append({'lastName': lastName , 'firstName':firstName , 'account':account , 'email':email});
    });
    return dataList;
}