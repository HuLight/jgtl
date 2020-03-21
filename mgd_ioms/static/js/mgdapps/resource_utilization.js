$(function(){
    $("#plugin3_demo1 .select2_box").select2({
            placeholder: '请选择选项'
        });


        $("#plugin3_demo3 .select2_box").select2({
            ajax: {
                url: "/get_group_host/",
                cache: false,
                //对返回的数据进行处理
                results: function (data) {

                    return data;

                }
            }

        });
    var li = $('.navbar-nav li');
    li.each(function(){
        $(this).click(function(){
            if( $(this).hasClass('opens') && $(this).find('ul li').length !=0){
                $(this).find('ul').slideUp(250);
                $(this).removeClass('opens');
            }else if($(this).find('ul li').length !=0){
                $(this).find('ul').slideDown(250);
                $(this).addClass('opens');
                $(this).siblings('li').removeClass('opens').find('ul').slideUp();
            }
        });
    });
    function renderTpl(str, cfg) {
            var re = /(#(.+?)#)/g;

            return str.replace(re, function() {
                var val = cfg[arguments[2]]+'';
                if(typeof val == 'undefined') {
                    val = '';
                }
                return val;
            });
        }
    // 加载群组列表
         $.ajax({
               url: "/get_group_host/",
               type: "GET",
               dataType: "json",
             success: function (result) {
                   $("#plugin3_demo2 .select2_box").select2({ data: result });
                   $("#plugin3_demo2 .select2_box").select2("val","");
                    $("#plugin3_demo3 .select2_box").select2("val","");
                    $("#plugin3_demo4 .select2_box").select2("val","");
             }
         })


        gethostinfos()
        $("#cpuValue").on("change",function () {
            var selectGroup =  $("#plugin3_demo2 .select2_box").select2("val")
           var selecthost =  $("#plugin3_demo3 .select2_box").select2("val")
           var selectip =  $("#plugin3_demo4 .select2_box").select2("val")
            if (selectGroup == ""){
                gethostinfos("none","none","none")
            }else {
                gethostinfos(selectGroup,selecthost,selectip)

            }
        })
         $("#memoryValue").on("change",function () {

             var selectGroup =  $("#plugin3_demo2 .select2_box").select2("val")
           var selecthost =  $("#plugin3_demo3 .select2_box").select2("val")
           var selectip =  $("#plugin3_demo4 .select2_box").select2("val")
             if (selectGroup == ""){
                gethostinfos("none","none","none")
            }else {
                gethostinfos(selectGroup,selecthost,selectip)

            }
        })
         $("#diskValue").on("change",function () {

            var selectGroup =  $("#plugin3_demo2 .select2_box").select2("val")
           var selecthost =  $("#plugin3_demo3 .select2_box").select2("val")
           var selectip =  $("#plugin3_demo4 .select2_box").select2("val")
            if (selectGroup == ""){
                            gethostinfos("none","none","none")
                        }else {
                            gethostinfos(selectGroup,selecthost,selectip)

                        }        })
        $("#plugin3_demo2 .select2_box").on("change",function () {
            // 加载主机列表
             $.ajax({
                   url: "/get_list_host/",
                   type: "GET",
                   dataType: "json",
                   data:{
                      selectGroup: $("#plugin3_demo2 .select2_box").select2("val")
                   },
                 success: function (result) {
                       $("#plugin3_demo3 .select2_box").select2({ data: result });
                       $("#plugin3_demo3 .select2_box").select2("val",result[0].text);
                       $.ajax({
                           url: "/get_host_ip/",
                           type: "GET",
                           dataType: "json",
                           data:{
                              hostName: result[0].text
                           },
                         success: function (result) {
                               $("#plugin3_demo4 .select2_box").select2({ data: result });
                               $("#plugin3_demo4 .select2_box").select2("val",result[0].text);
                               var selectGroup =  $("#plugin3_demo2 .select2_box").select2("val")
                               var selecthost =  $("#plugin3_demo3 .select2_box").select2("val")
                               var selectip =  $("#plugin3_demo4 .select2_box").select2("val")
                               gethostinfos(selectGroup,selecthost,selectip)
                         }
                     })
                 }
             })

        })

        $("#plugin3_demo3 .select2_box").on("change",function () {

            // 加载主机列表
             $.ajax({
                   url: "/get_host_ip/",
                   type: "GET",
                   dataType: "json",
                   data:{
                      hostName: $("#plugin3_demo3 .select2_box").select2("val")
                   },
                 success: function (result) {
                       $("#plugin3_demo4 .select2_box").select2({ data: result });
                       $("#plugin3_demo4 .select2_box").select2("val",result[0].text);
                       var selectGroup =  $("#plugin3_demo2 .select2_box").select2("val")
                       var selecthost =  $("#plugin3_demo3 .select2_box").select2("val")
                       var selectip =  $("#plugin3_demo4 .select2_box").select2("val")
                       gethostinfos(selectGroup,selecthost,selectip)

                 }
             })

        })
})

function getcurrentdata(){
        var position = $(this).attr('data-position');
        toastr.remove();
        toastr.success('获取中，请稍后',{
            positionClass: position
        });
        $.ajax({
               url: "/get_history/",
               type: "GET",
               dataType: "json",
            success: function (result) {
                if(result.msg=='获取成功'){
                        toastr['success']('获取成功');
                }else {
                        toastr['error']('获取失败');

                }

               }
        })


    }


    function gethostinfos(selectGroup="",selecthost="",selectip="",all="false") {
        if (all == "true"){
            var cpuValue = 0;
        var memoryValue = 0
        $("#cpuValue").val("")
        $("#memoryValue").val("")
            $("#plugin3_demo2 .select2_box").select2("val","");
            $("#plugin3_demo3 .select2_box").select2("val","");
            $("#plugin3_demo4 .select2_box").select2("val","");


        }else{
            var cpuValue = $("#cpuValue").val();
            var memoryValue = $("#memoryValue").val();
        }

        //首次进入页面进行加载
           // $.ajaxSetup({ cache: false });
        var hostinfo = $("#table2_demo4 tbody");

           $.ajax({
               url: "/get_utilization_info/",
               type: "GET",
               dataType: "json",
                contentType: false,   // jQuery不要去设置Content-Type请求头
               data: {
                   "cpuValue":cpuValue,
                   "memoryValue":memoryValue,
                   "time":new Date().getTime(),
                   "selectGroup":selectGroup,
                   "selecthost":selecthost,
                   "selectip":selectip,

               },
               success: function (result) {

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

                    var table = $("#table2_demo4").dataTable({
                        autoWidth: false,
                        lengthChange: true, //不允许用户改变表格每页显示的记录数
                        pageLength : 20, //每页显示几条数据
                        //lengthMenu: [20,30,40], //每页显示选项
                        pagingType: 'full_numbers',
                        ordering: false,
                        lengthChange:false,
                        destroy: true,
                        searching: false,
                        scrollX: true,
                        language:language,
                        data:result,
                        "columns": [
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap' title='" + row.group_name + "'>" + row.group_name + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap' title='" + row.host + "'>" + row.host + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap' title='" + row.name + "'>" + row.name + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value1' title='" + row.status + "'>" + row.status + "</div>"
                             }
                            },
                            {
                                data:"",
                                orderable:false,
                                render : function(data, type, row, meta){
                                   return "<a "+"onclick="+ "xadmin.open('详情页','/host_detailspage/?hostid="+ row.hostid + "','','',true)>"+row.ip+"</a>";
                                }


                              },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value1' title='" + row.cpu_num + "'>" + row.cpu_num + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value2' title='" + row.cpu_value_max + "'>" + row.cpu_value_max + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value2' title='" + row.cpu_value_avg + "'>" + row.cpu_value_avg + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value2' title='" + row.cpu_value_min + "'>" + row.cpu_value_min + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value1' title='" + row.memory_size + "'>" + row.memory_size + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value2' title='" + row.mem_value_max + "'>" + row.mem_value_max + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value2' title='" + row.mem_value_avg + "'>" + row.mem_value_avg + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value2' title='" + row.mem_value_min + "'>" + row.mem_value_min + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value3' title='" + row.disk_size + "'>" + row.disk_size + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value4' title='" + row.disk_used + "'>" + row.disk_used + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_value4' title='" + row.disk_used_percent + "'>" + row.disk_used_percent + "</div>"
                             }
                            },
                            {
                             data:"",
                             render:function(data, type, row, meta){
                                 return "<div class='wrap_date' title='" + row.date + "'>" + row.date + "</div>"
                             }
                            },

                        ]

                    });

               }
           })
    }