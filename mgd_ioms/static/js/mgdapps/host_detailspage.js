$(function(){
        hostid = getQueryString('hostid')
        commonLocalRefresh(hostid,0.5)
    })
function loadtime(time){
    commonLocalRefresh(hostid,time)
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
//  获取数据局部刷新主机页面
function commonLocalRefresh(hostid,time) {
    $.ajax({
        url:"/get_detailspage_info/",
        type:"GET",
        dataType:"json",
        async:false,
        data:{"hostid":hostid,"time":time},
        success:function (data) {
            // 主机信息
            var hostInfo = data.host_info
            //$("#hostName").html(hostInfo.name)          //主机
            $("#hostName").html("<span class='wrap' title='" + hostInfo.name + "'>" + hostInfo.name +"</span>" )
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

        }
    })
}

$('#bk-dropdown-menu4').bkDropdown({
    onInit: function(dropdown) {
        $('#bk-dropdown-menu4').data('bkDropdown').hide();
        // 自定义操作
        dropdown.find('a').on('click', function() {
            dropdown.data('bkDropdown').hide();
            console.log("dropdown.data",dropdown.data('bkDropdown'))
        });
    },
    onShow: function(dropdown) {
        dropdown.find('.bk-icon').addClass('icon-flip');
    },
    onHide: function(dropdown) {
        dropdown.find('.bk-icon').removeClass('icon-flip');
    }
});

var dom2 = document.getElementById("memoryUsage");
var myChart2 = echarts.init(dom2);
var app = {};
option2 = null;
option2 = {
    title: {
        text: '内存使用率',
        textStyle: {
            fontWeight: 'normal',
            color: "#00FFFF",
        },
    },
    legend: {
        data:['内存使用率'],
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
        data : [''],
        splitLine:{show:false},
        axisLabel:{
            rotate:45,
        }


    },
    yAxis: {
        type: 'value',
        axisLabel:{
            formatter:'{value}%'
        }

    },
    series: [
        {
            name:'内存使用率',
            type:'line',
            stack: '百分比1',
            data:[''],
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
if (option2 && typeof option2 === "object") {
    myChart2.setOption(option2, true);
}

var dom3 = document.getElementById("networkTraffic");
var myChart3 = echarts.init(dom3);
var app = {};
option3 = null;
option3 = {
    title: {
        text: '网卡流量',
        textStyle: {
            fontWeight: 'normal',
            color: "#00FFFF",
        },
    },
    legend: {
        data:['出口流量','进口流量'],
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
        data : [''],
        splitLine:{show:false},
        axisLabel:{
            rotate:45,
        }

    },
    yAxis: {
        type: 'value',
        axisLabel:{
            formatter:'{value}Kbps'
        }

    },
    series: [
        {
            name:'出口流量',
            type:'line',
            stack: '百分比1',
            data:[''],
            smooth:true,
            symbol: 'none',
        },{
            name:'进口流量',
            type:'line',
            stack: '百分比1',
            data:[''],
            smooth:true,
            symbol: 'none',
        },


    ]
};
if (option3 && typeof option3 === "object") {
    myChart3.setOption(option3, true);
}


var dom4 = document.getElementById("diskIO");
var myChart4 = echarts.init(dom4);
var app = {};
option4 = null;
option4 = {
    title: {
        text: '磁盘读写速率',
        textStyle: {
            fontWeight: 'normal',
            color: "#00FFFF",
        },
    },
    legend: {
        data:['磁盘读速率','磁盘写速率'],
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
        data : [''],
        splitLine:{show:false},
        axisLabel:{
            rotate:45,

        }

    },
    yAxis: {
        type: 'value',
        axisLabel:{
            interval:0,
            formatter:'{value}M'

        }

    },
    series: [
        {
            name:'磁盘读速率',
            type:'line',
            stack: '百分比1',
            data:[''],
            smooth:true,
            symbol: 'none',
        },{
            name:'磁盘写速率',
            type:'line',
            stack: '百分比1',
            data:[''],
            smooth:true,
            symbol: 'none',
        },


    ]
};
if (option4 && typeof option4 === "object") {
    myChart4.setOption(option4, true);
}



var dom6 = document.getElementById("diskUtilization");
var myChart6 = echarts.init(dom6);
option6 = null;
option6 = {
    title: {
        text: '磁盘使用率',
        textStyle: {
            fontWeight: 'normal',
            color: "#00FFFF",
        },
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影

    },
    legend: {
        data: ['磁盘使用率']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis:  {
        type: 'value',
        min: "0",
        max: "100",
        splitLine:{show:false},
        data:[""],
        axisLabel:{
            interval:0,
            rotate:45,
            formatter:'{value}%'
        }
    },
    yAxis: {
        type: 'category',
        data: [""],
        smooth:true,
        symbol: 'none',

    },
    series: [
        {
            name: '',
            type: 'bar',
            stack: '总量',
            barWidth:30,
            label: {
                normal: {
                    position: 'right',
                    show: true
                }
            },

            data: [''],
            symbol: 'none',

            itemStyle:{
                normal:{
                    color:function(params){
                        if (params.data >50){
                            return '#FF4500'
                        }else{
                            return '#228B22'
                        }

                    }
                },

            }
        },


    ]
}
if (option6 && typeof option6 === "object") {
    myChart6.setOption(option6, true);
}

//检测窗口变化 重新加载echarts
$(window).resize(function() {
    var window_width = $(window).width();//获取浏览器窗口宽度
    //myChart1.resize();
    //myChart2.resize();
    //myChart3.resize();
    //myChart4.resize();
    //myChart5.resize();
    //myChart6.resize();
});
