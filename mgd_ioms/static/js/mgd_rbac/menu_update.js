$("#btnSave").click(function () {
            var data = $("#addForm").serialize();
            $.ajax({
                type: $("#addForm").attr('method'),
                url: "{% url 'system:rbac-menu-update' %}",
                data: data,
                cache: false,
                success: function (msg) {
                    if (msg.result) {
                        layer.alert('数据保存成功！', {icon: 1}, function (index) {
                            parent.layer.closeAll(); //关闭所有弹窗
                        });
                    } else {
                        layer.alert('数据保存失败', {icon: 5});
                        //$('errorMessage').html(msg.message)
                    }
                    return;
                }
            });
        });


        /*点取消刷新新页面*/
        $("#btnCancel").click(function () {
            window.location.reload();

        });

        $(function () {
            //Initialize Select2 Elements
            $(".select2").select2();
        });
