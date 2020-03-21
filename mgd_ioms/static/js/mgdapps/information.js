window.onload = function () {
     // 获取端口名称
     var portName = getQueryString("name")
     var hostid = getQueryString("hostid")
     $.ajax({
         url:"/get_port_info/",
         type:"GET",
         dataType:"json",
         data:{
             "portName":portName,
             "hostid":hostid
         },
         success:function (data) {
             console.log("data===",data)
             $("#portstatus").html(data.status);
             $("#type").html(data.type);
             $("#rate").html(data.speed);
             $("#traffic").html(data.traffic);
             $("#mac").html();

         }
     })
}
 function getQueryString(name) {
        var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        var r = window.location.search.substr(1).match(reg);
        if (r != null) {
        return unescape(r[2]);
        }
        return null;
    }