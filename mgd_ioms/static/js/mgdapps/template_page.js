var count = 0
var currpage = 1
$(function () {
    $.ajax({
        type:"GET",
        url:"/get_template_data/",
        data:{
            "page":1
        },
        success:function (data) {
            layui.use('laypage', function(){
                var laypage = layui.laypage;
                //执行一个laypage实例
                laypage.render({
                elem: 'paging' //注意，这里的 test1 是 ID，不用加 # 号
                ,count: data.total //数据总数，从服务端得到
                ,limit: 4
                ,jump: function(obj, first){
                    currpage = obj.curr
                    get_dta(obj.curr)

                    }
                });
            });
            count = data.total
        }
    })
})

function get_dta(page) {
    var page = page
    $.ajax({
        type:"GET",
        url:"/get_template_data/",
        data:{
            "page":page
        },
        success:function (data) {
            var chart_info = $("#chart_info")
            chart_info.html("")
            $.each(data.results,function (index,element) {
                console.log("element==",element)
                chart_info.append("<div class='chart' id='chart"+index+"'></div>")
                var ids = "chart"+index
                ids = document.getElementById("chart"+index);
                var myChart = "myChart" + index
                myChart = echarts.init(ids);
                var option = "option" + index
                var displaymode = element.type
                var xAxis = {}
                var yAxis = {}
                if (displaymode == "line"){
                    xAxis['type'] = "category"
                    xAxis['data'] = element.time
                    xAxis['splitLine'] = "{show:false}"
                    yAxis['type'] = "value"

                }else {
                    yAxis['type'] = "category"
                    yAxis['data'] = element.time
                    yAxis['splitLine'] = "{show:false}"
                    xAxis['splitLine'] = "{show:false}"
                    xAxis['type'] = "value"
                }
                option = {
                    backgroundColor:"#FFFFFF",
                    title: {
                        text: '',
                        textStyle: {
                            fontWeight: 'normal',
                            color: "#00FFFF",
                        },
                    },
                    legend: {
                        data:[''],
                     },
                    tooltip: {
                        trigger: 'axis'
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true,
                        width:"80%",
                    },
                    xAxis,
                    yAxis,
                    series: [
                        {
                            name:'',
                            type:displaymode,
                            data:element.data,
                            smooth:true,
                            symbol: 'none',
                            itemStyle:{
                                normal:{
                                    color:'#228B22'
                                },
                            },
                        },
                    ]
                }
                if (option && typeof option === "object") {
                    myChart.setOption(option, true);
                }
                myChart.resize();
            })
        }
    })
}
$(function () {
    //检测窗口变化 重新加载echarts
    $(window).resize(function() {
        console.log("curr",currpage)
        get_dta(currpage)

    });
})
