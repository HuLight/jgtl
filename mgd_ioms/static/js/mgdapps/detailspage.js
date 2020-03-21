window.onload = function () {
    // 1 网络  2 操作系统
    type = getQueryString("type")
    informationBar(type)                //获取左侧信息栏数据
}
//获取url中的hostid
function getQueryString(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
    return unescape(r[2]);
    }
    return null;
}
// 获取左侧信息栏数据
function informationBar(type) {
    $.ajax({
        url:"/get_information_bar/",
        type:"GET",
        dataType:"json",
        data:{
            "type":type
        },
        success:function (data) {
            // 动态添加li标签
            // 主机设备
            ulmainlist = $("#mainlist")
            ulmainlist.html("")
            $(data).each(
                function (i,item) {
                    ulmainlist.append(
                    "<li class='has_submenu current open c-open'> <a href='javascript:void(0);'> <i class=''> <span style='font-size: 14px'>" +
                        item.groupName + "</span><span class='pull-right'><i class='fa fa-angle-down'></i></span></a>" +
                        "<ul class='sub-menu' id='list" + i + "'></ul></li>"
                    )
                    if (item.groupName.search("网络") != -1){
                        load = 'getNetworkInfo(this)'

                    }else {
                        load = 'getHostInfo(this)'
                    }
                    var ullist = $("#list"+i)
                    ullist.html("")
                    $(item.list.result).each(
                        function (j,value) {
                            ullist.append(
                                "<li onclick='"+load+ "'value="+value.hostid+">"+value.name+"<i class='fa fa-chevron-right pull-right'></i></li>"

                            )

                        }
                    )
                }
            )
            var li = $('.navi li');
            li.each(function(){
                 $(this).click(function(){
                     if( $(this).hasClass('c-open')){
                        $(this).find('ul').slideUp(350);
                        $(this).removeClass('c-open');
                     }else{
                       $(this).find('ul').slideDown(350);
                       $(this).addClass('c-open');
                       }
                  })
            });
        }
    })
}


var hostLoad = 0            //如果为0说明第一次加载,需要ajax清空页面并重新加载 如果为1则不需要加载页面

// 获取主机页面
function getHostInfo(item) {
    showLoading(1)
    $.ajax({
        type:"GET",
        url:"/host_page/",
        success:function (data) {
            hostid = $(item).val();

            networkLoad = 0                             // 将网络主机设置为0
            if (hostLoad == 0){
                $('#mainContents').empty();//清空页面
                $('#mainContents').append(data)         //加载页面
                hostLoad = 1                            //设置为1
                commonLocalRefresh(hostid,0.5);
            }else {
                //$('#mainContents').append(data)
                commonLocalRefresh(hostid,0.5);
            }
            closeLoading(1)

        }
    });

    hostid = $(item).val();
   window.clearInterval(t2)  // 去除定时器
   var t2 = window.setInterval(function() {

       //commonLocalRefresh(hostid);

   },10000)
    commonLocalRefresh(hostid,0.5);
}
 function loadtime(time){
    commonLocalRefresh(hostid,time)
}

// 获取网络页面
var networkLoad = 0
function getNetworkInfo(item) {
    showLoading(1)
    $.ajax({
        type:"GET",
        url:"/network_detailspage/",
        success:function (data) {
            hostid = $(item).val();
            hostLoad = 0                            //将主机页面设为0  下次点击重新加载
            if(networkLoad == 0){
                $('#mainContents').empty();
                $('#mainContents').append(data)         //装入页面
                commonLoaclNetworkRefresh(hostid)       //加载页面数据
                networkLoad = 1                         //将网络主机页面设为1

            }else {
                commonLoaclNetworkRefresh(hostid)
            }
            closeLoading(1)
        }
    });
    return false;
}

//  获取数据局部刷新网络设备页面
function commonLoaclNetworkRefresh(hostid) {
    $.ajax({
        url:"/get_network_equipment_info/",
        type:"GET",
        dataType:"json",
        data:{"hostid":hostid},
        success:function (data) {
            // 网络设备信息
            equipmentInfo = data.network_host_info
            $("#equipmentName").html(equipmentInfo.system_name)                  // 主机名/设备名
            $("#businessName").html(equipmentInfo.name)                                            //业务名称
            $("#networkipAddress").html(equipmentInfo.ip)               //ip地址
            $("#networkosType").html()                  //OS类型
            $("#networkRunTime").html(equipmentInfo.uptime)                 //运行时间
            $("#networkHostStatus").html(equipmentInfo.state)              //运行状态
            $("#networkSystemVersion").html()           //系统版本
            //硬件信息

            myChart1.setOption({
                 series:[{
                     data:data.physical_status.usage
                 }],

             })
            //端口流量TOP5
            myChart2.setOption({
                 series:[{
                     data:data.net_traffic_top5.ranking_top5_value,
                 }],
                 yAxis:[{
                     data:data.net_traffic_top5.ranking_top5_name
                 }],
             })
            //端口状态
            myChart3.setOption({
                 series:[{
                     data:[{value:data.port_state.normal_value,name:'up'},{value:data.port_state.abnormal_value,name:'down'}],
                 }]
             })
            // 错包数
            if (data.err_packet.name[0] != undefined){
                var dom4 = document.getElementById("porterrorTraffic");
                var myChart4 = echarts.init(dom4);
                option4 = {
                    tooltip : {
                        trigger: 'axis',
                        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        },
                        extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影

                    },
                    legend: {
                        data: ['错包数(Kbps)']
                    },
                    grid: {
                        top:"1px",
                        left:"60px",
                        right:"1px",
                        bottom:"5px",
                        width:"80%", //图例宽度

                        height:"180px", //图例高度
                    },
                    xAxis:  {
                        type: 'value',
                        min: "0",
                        splitLine:{show:false},
                        data:[""],
                        axisLabel:{
                            interval:0,
                            formatter:'{value}',
                        }
                    },
                    yAxis: {
                        type: 'category',
                        data: data.err_packet.name,
                        smooth:true,
                        symbol: 'none',
                        axisLabel:{
                            rotate:45,
                            fontSize:'10'
                        },
                        min:490

                    },
                    series: [
                        {
                            name: '',
                            type: 'bar',
                            stack: '总量',
                           // barWidth:30,
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: data.err_packet.value,
                            symbol: 'none',
                        },
                    ]
                }
                if (option4 && typeof option4 === "object") {
                    myChart4.setOption(option4, true);
                }

            }else {
                $("#porterrorTraffic").html("<P>暂无错包数据<p>")

            }

            if (data.err_packet.name[0] != undefined){
                var dom5 = document.getElementById("portlostTraffic");
                var myChart5 = echarts.init(dom5);
                option5 = {
                    tooltip : {
                        trigger: 'axis',
                        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        },
                        extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影

                    },
                    legend: {
                        data: ['丢包数(Kbps)']
                    },
                    grid: {
                        top:"1px",
                        left:"60px",
                        right:"1px",
                        bottom:"5px",
                        width:"80%", //图例宽度

                        height:"180px", //图例高度
                    },
                    xAxis:  {
                        type: 'value',
                        min: "0",
                        splitLine:{show:false},
                        data:[""],
                        axisLabel:{
                            interval:0,
                            formatter:'{value}',
                        }
                    },
                    yAxis: {
                        type: 'category',
                        data: data.err_packet.name,
                        smooth:true,
                        symbol: 'none',
                        axisLabel:{
                            rotate:45,
                            fontSize:'10'
                        },
                        min:490

                    },
                    series: [
                        {
                            name: '',
                            type: 'bar',
                            stack: '总量',
                           // barWidth:30,
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: data.err_packet.value,
                            symbol: 'none',
                        },
                    ]
                }
                if (option5 && typeof option5 === "object") {
                    myChart5.setOption(option5, true);
                }
            }else {
                $("#portlostTraffic").html("<P>暂无丢包数据<p>")

            }
            // 端口流量% top10
             myChart6.setOption({
                series:[{
                     data:data.port_percent.value
                 }],
                 yAxis:[{
                     data:data.port_percent.name
                 }],
             })
             // 端口流量值 top10
             myChart7.setOption({
                series:[{
                     data:data.port_value_top10.value
                 }],
                 yAxis:[{
                     data:data.port_value_top10.name
                 }],
             })
            var language = {
              search: '搜索：',
              lengthMenu: "每页显示 _MENU_ 记录",
              zeroRecords: "没找到相应的数据！",
              info: "分页 _PAGE_ / _PAGES_",
              infoEmpty: "暂无数据！",
              infoFiltered: "(从 _MAX_ 条数据中搜索)",
              paginate: {
                first: '首页',
                last: '尾页',
                previous: '上一页',
                next: '下一页',
              }
            }
            console.log("data.port_state.port_state_list",data.port_state.port_state_list)
            $('#table2_demo1').dataTable({
                  paging: true, //隐藏分页
                  ordering: false, //关闭排序
                  info: false, //隐藏左下角分页信息
                  searching: false, //关闭搜索
                  pageLength : 5, //每页显示几条数据
                  lengthChange: false, //不允许用户改变表格每页显示的记录数
                  language: language, //汉化,
                  destroy: true,
                  data:data.port_state.port_state_list,
                  "columns": [

                      {
                        data:"",
                        orderable:false,
                        render : function(data, type, row, meta){
                           return "<a "+"onclick="+ "xadmin.open('端口详情','/information/?name="+row.name+"&hostid="+hostid+"',400,300)>"+row.name+"</a>";
                        }


                      },
                      {"data":"state"},

                  ]

            });

            // 告警信息
            var warningMessage = $("#warningMessage");
            warningMessage.html("");
            $(data.warned_message).each(
                function (i,value) {
                    index = i + 1
                    warningMessage.append(
                        "<tr><td>" + index + "</td>"
                        +"<td>" + value.trigger_time + "</td>"
                        +"<td>" + value.priority + "</td>"
                        +"<td>" + "</td>"
                        +"<td>" + value.status + "</td>"
                        +"<td>" + "</td>"
                        +"<td>" + value.name + "</td>"
                        +"<td>" + value.description + "</td>"
                        +"<td>" + "</td>"
                        +"<td>" + "</td>"
                        +"<td>" + "</td>"
                    )
                }
            )


        }


    })

}
//  获取数据局部刷新主机页面
function commonLocalRefresh(hostid,time) {
    $.ajax({
        url:"/get_detailspage_info/",
        type:"GET",
        dataType:"json",
        data:{"hostid":hostid,"time":time},
        success:function (data) {
            // 主机信息
            var hostInfo = data.host_info
            $("#hostName").html(hostInfo.name)          //主机
            $("#host").html(hostInfo.host)              //主机名
            $("#ipAddress").html(hostInfo.ip)           //ip
            $("#osType").html(hostInfo.os_name)         //os
            $("#runTime").html(hostInfo.uptime)         //运行时间
            $("#hostStatus").html(hostInfo.state)       //主机状态
            // 清空所有数据
            // cpu使用率
            if (data.cpu_info != null){
                var dom1 = document.getElementById("cpuUsage");
                var myChart1 = echarts.init(dom1);
                option1 = null;
                option1 = {
                    title: {
                        text: 'CPU趋势图',
                        textStyle: {
                            fontWeight: 'normal',
                            color: "#00FFFF",
                        },
                    },
                    legend: {
                        data:['CPU趋势图'],
                     },
                    tooltip: {
                        trigger: 'axis'
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data : data.cpu_info.period_of_time,
                        splitLine:{show:false},
                        axisLabel:{
                            rotate:45,
                        },


                    },
                    yAxis: {
                        type: 'value',
                        axisLabel:{
                            formatter:'{value}%'
                        }

                    },
                    series: [
                        {
                            name:'CPU趋势图',
                            type:'line',
                            stack: '百分比1',
                            data:data.cpu_info.historical_value,
                            smooth:true,
                            symbol: 'none',
                            itemStyle:{
                                normal:{
                                    color:'#228B22'
                                },
                            }
                        },
                    ]
                };
                if (option1 && typeof option1 === "object") {
                    myChart1.setOption(option1, true);
                }
            }else {
                $("#cpuUsage").html("<P>暂无数据<p>")
            }
            // 内存使用率
            if (data.memory_utilization != null){
                myChart2.setOption({
                 series:[{
                     data:data.memory_utilization.memory_unilization_value
                 }],
                 xAxis:[{
                     data:data.memory_utilization.memory_unilization_time
                 }],
             })
            }else {
                myChart2.setOption({
                 series:[{
                     data:[]
                 }],
                 xAxis:[{
                     data:[]
                 }],
             })
            }

            //网卡流量
            if (data.net_traffic != null){
                myChart3.setOption({
                 series:[{
                     data:data.net_traffic.sent_traffic_value
                 },{
                     data:data.net_traffic.received_traffic_value
                 }],
                 xAxis:[{
                     data:data.net_traffic.received_traffic_time
                 }],
             })
            }else {
                myChart3.setOption({
                 series:[{
                     data:[]
                 },{
                     data:[]
                 }],
                 xAxis:[{
                     data:[]
                 }],
             })
            }

            // 磁盘读写速度
            if (data.rw_rate != null){
                myChart4.setOption({
                 series:[{
                     data:data.rw_rate.read_rate_value
                 },{
                     data:data.rw_rate.write_rate_value
                 }],
                 xAxis:[{
                     data:data.rw_rate.write_rate_time
                 }],
             })
            }else {
                myChart4.setOption({
                 series:[{
                     data:[]
                 },{
                     data:[]
                 }],
                 xAxis:[{
                     data:[]
                 }],
             })
            }
            // 告警信息
            var warningMessage = $("#warningMessage");
            warningMessage.html("");
            $(data.warned_message).each(
                function (i,value) {
                    index = i + 1
                    warningMessage.append(
                        "<tr><td>" + index + "</td>"
                        +"<td>" + value.trigger_time + "</td>"
                        +"<td>" + value.priority + "</td>"
                        +"<td>" + "</td>"
                        +"<td>" + value.status + "</td>"
                        +"<td>" + "</td>"
                        +"<td>" + value.name + "</td>"
                        +"<td>" + value.description + "</td>"
                        +"<td>" + "</td>"
                        +"<td>" + "</td>"
                        +"<td>" + "</td>"
                    )
                }
            )
            // 磁盘使用率
            if (data.disk_utilization != null){
                myChart6.setOption({
                 series:[{
                     data:data.disk_utilization.disk_usage,
                 }],
                 yAxis:[{
                     data:data.disk_utilization.hard_disk_mount_point
                 }],
             })
            }else {
                myChart6.setOption({
                 series:[{
                     data:[]
                 }],
                 yAxis:[{
                     data:[]
                 }],
             })
            }
            console.log("name==",name)
            myChart7.setOption({
                series:[{
                     data:[{name:data.swap_in_out_info.name,value:data.swap_in_out_info.value}]
                 }],

            })

        }
    })
}

function showLoading(num){
    $('#loding-img-' + num).show();
}
function closeLoading(num) {
    $('#loding-img-' + num).hide();
}