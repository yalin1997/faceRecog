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
    newCell6.innerHTML = "<button class='btn btn-primary' id = 'btn_"+studentCounter+"' onclick = 'editMemberData(id)'>編輯</button>"
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
    $(table).find('tr').each(function (i) {
        var $tds = $(this).find('td'),
            lastName = $tds.eq(1).text(),
            firstName = $tds.eq(2).text(),
            account = $tds.eq(3).text(),
            email = $tds.eq(4).text();
        if(!(lastName == "" && firstName == "" && account == "" && email == "")){
            dataList.push({'classId': location.search.split('=')[1],'lastName': lastName , 'firstName':firstName , 'account':account , 'email':email});
        }
    });
    return dataList;
}

function editMemberData(id){
    var currentRow = $("#"+id).closest('tr');
    var $tds = currentRow.find('td');
    $('input[name="lastName"]').val($tds.eq(1).text());
    $('input[name="firstName"]').val($tds.eq(2).text());
    $('input[name="account"]').val($tds.eq(3).text());
    $('input[name="email"]').val($tds.eq(4).text());
    currentRow.remove();
    studentCounter--;
}