var dom1 = document.getElementById("hardwareFittings");
var myChart1 = echarts.init(dom1);
option1 = null;
option1 = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影

    },
    legend: {
        data: ['硬件信息']
    },
    grid: {
        top:"5px",
        left:"35px",
        right:"1px",
        bottom:"5px",
        width:"70%", //图例宽度

        height:"180px", //图例高度
    },
    xAxis:  {
        type: 'value',
        min: "0",
        max: "100",
        splitLine:{show:false},
        data:[""],

        axisLabel:{
            interval:0,
            formatter:'{value}%'

        }


    },
    yAxis: {
        type: 'category',
        data: ["磁盘","内存","cpu"],
        smooth:true,
        symbol: 'none',

    },
    series: [
        {
            name: '',
            type: 'bar',
            stack: '磁盘',
            //barWidth:30,
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
                        if (params.data <50){
                            return '#228B22'
                        }else if (params.data >50 || params.data<70){
                            return '#FFFF00'
                        }else {
                            return'#FF4500'
                        }

                    }
                },

            }
        }
    ]
}
if (option1 && typeof option1 === "object") {
    myChart1.setOption(option1, true);
}

var dom2 = document.getElementById("portTraffic");
var myChart2 = echarts.init(dom2);
option2 = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影

    },
    legend: {
        data: ['端口流量top10(kbps)']
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
        data: [""],
        smooth:true,
        symbol: 'none',
        axisLabel:{
            rotate:45,
            fontSize:'10'
        }

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

            data: [''],
            symbol: 'none',
        },


    ]
}
if (option2 && typeof option2 === "object") {
    myChart2.setOption(option2, true);
}

var dom3 = document.getElementById("portState");
var myChart3 = echarts.init(dom3);
option3 = {
    title : {
        text: '端口状态',
        subtext: '',
        x:'left',
        textStyle: {
            fontWeight: 'normal',
            color: "#00FFFF",
        },
    },
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c}({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'bottom',
        data:['up','down']
    },
    series: [
        {
            name:'',
            type:'pie',
            radius: ['40%', '50%'],
            label: {
                normal: {
                    formatter: '{a|{a}}{abg|} {b|{b}：}{c}',
                    padding: [2, 7],
                    fontSize:12,
                    rich: {
                        a: {
                            color: '#999',
                            lineHeight: 12,
                            align: 'center',
                        },
                        b: {
                            fontSize: 12,
                            lineHeight: 33
                        },
                        per: {
                            color: '#eee',
                            backgroundColor: '#334455',
                            padding: [2, 4],
                            borderRadius: 2,
                            fontSize:12,
                        }
                    }
                }
            },
            data:[
                {}
            ],
            itemStyle:{
                emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                     },
                normal:{
                    color:function(params) {
                            //自定义颜色
                            var colorList = [
                                '#7CCD7C', '#FF4500',

                                ];
                                return colorList[params.dataIndex]
                             }
                }
            }

        }
    ]
};

if (option3 && typeof option3 === "object") {
    myChart3.setOption(option3, true);
}
var dom6 = document.getElementById("portTrafficPer");
var myChart6 = echarts.init(dom6);
option6 = null;
option6 = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影

    },
    legend: {
        data: ['端口流量%top10(Kbps)']
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
        data: [""],
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

            data: [''],
            symbol: 'none',
        },


    ]
}
if (option6 && typeof option6 === "object") {
    myChart6.setOption(option6, true);
}

var dom7 = document.getElementById("portTrafficValue");
var myChart7 = echarts.init(dom7);
option7 = null;
option7 = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影

    },
    legend: {
        data: ['端口流量数值top10(Kbps)']
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
        data: [""],
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
            //barWidth:0,
            label: {
                normal: {
                    position: 'right',
                    show: true
                }
            },

            data: [''],
            symbol: 'none',
        },


    ]
}
if (option7 && typeof option7 === "object") {
    myChart7.setOption(option7, true);
}


//检测窗口变化 重新加载echarts
$(window).resize(function() {
    var window_width = $(window).width();//获取浏览器窗口宽度
    myChart1.resize();
    myChart2.resize();
    myChart3.resize();
    myChart4.resize();
    myChart5.resize();
    myChart6.resize();
    myChart7.resize();
});

 $(function () {
    //table2_demo1_js_start
    //表格(DataTables)-1，html数据源
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
    $('#table2_demo1').dataTable({
      paging: true, //隐藏分页
      ordering: false, //关闭排序
      info: false, //隐藏左下角分页信息
      searching: false, //关闭搜索
      pageLength : 5, //每页显示几条数据
      lengthChange: false, //不允许用户改变表格每页显示的记录数
      language: language //汉化
    });
});
