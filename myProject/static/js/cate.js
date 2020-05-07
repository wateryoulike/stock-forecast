$(document).ready(function () {


    function message_success() {
        $modal({
            type: 'message', //弹框类型  'alert' or  'confirm' or 'message'  message提示(开启之前如果之前含有弹框则清除)
            icon: 'success', // 提示图标显示 'info' or 'success' or 'warning' or 'error'  or 'question'
            timeout: 2500, // 单位 ms  显示多少毫秒后关闭弹框 （ confirm 下无效 | 不传默认为 2000ms | 最短显示时间为500ms）
            content: '退出成功', // 提示文字
            center: false,// 是否绝对居中 默认为false  设置true后   top无效
            top:100, //距离顶部距离 单位px
            transition: 500, //过渡动画 默认 200   单位ms
            closable: true, // 是否显示可关闭按钮  默认为 false
        })
    }
    function message_fail() {
        $modal({
            type: 'message', //弹框类型  'alert' or  'confirm' or 'message'  message提示(开启之前如果之前含有弹框则清除)
            icon: 'error', // 提示图标显示 'info' or 'success' or 'warning' or 'error'  or 'question'
            timeout: 2500, // 单位 ms  显示多少毫秒后关闭弹框 （ confirm 下无效 | 不传默认为 2000ms | 最短显示时间为500ms）
            content: '退出失败', // 提示文字
            center: false,// 是否绝对居中 默认为false  设置true后   top无效
            top:100, //距离顶部距离 单位px
            transition: 500, //过渡动画 默认 200   单位ms
            closable: true, // 是否显示可关闭按钮  默认为 false
        })
    }
    var cateId = $('input#cateId').val() - 1;
    // console.log(cateId);
    var cateLists = $('#cateLists > li > a');
    $(cateLists[cateId]).css('color', '#4272d7');

    $('#content > tr').each(function () {
        console.log(this);
        var more = $(this).children('td:last-child').children('span');
        console.log(more);
        $(more).click(function () {
            var val = $(this).parent().parent().children('input').val();
            console.log(val);
            window.location.href = '/detail?id=' + val;
        })
    });
    console.log($('#loginOut'));
    $('#loginOut').click(function () {
        console.log('hello');
        list = {'loginOut': 1};
        $.ajax({
            //请求方式
            type : "POST",
            //请求的媒体类型
            contentType: "application/json;charset=UTF-8",
            //请求地址
            url : "/handleLoginOut",
            //数据，json字符串
            data : JSON.stringify(list),
            //请求成功
            success : function(result) {
                console.log(result['loginOutStatus']);
                var status = result['loginOutStatus'];
                if(status === 1){
                    message_success();
                    setTimeout(function () {
                        window.location.href = '/login';
                    }, 2700)

                }else{
                    message_fail();
                }
            },
            //请求失败，包含具体的错误信息
            error : function(e){
                console.log(e.status);
                console.log(e.responseText);
                message_fail();
            }
        });
    })
});