function myPagination(_ref) {
    var pageSize = _ref.pageSize,
        pageTotal = _ref.pageTotal,
        curPage = _ref.curPage,
        id = _ref.id,
        getPage = _ref.getPage,
        showPageTotalFlag = _ref.showPageTotalFlag,
        showSkipInputFlag = _ref.showSkipInputFlag,
        pageAmount = _ref.pageAmount,
        dataTotal = _ref.dataTotal;

    this.pageSize = pageSize || 5; //分页个数
    this.pageTotal = pageTotal; //总共多少页
    this.pageAmount = pageAmount; //每页多少条
    this.dataTotal = dataTotal; //总共多少数据
    this.curPage = curPage || 1; //初始页码
    this.ul = document.createElement('ul');
    this.id = id;
    this.getPage = getPage;
    this.showPageTotalFlag = showPageTotalFlag || false; //是否显示数据统计
    this.showSkipInputFlag = showSkipInputFlag || false; //是否支持跳转
    this.init();
};
// 给实例对象添加公共属性和方法
myPagination.prototype = {
    init: function init() {
        var pagination = document.getElementById(this.id);
        pagination.innerHTML = '';
        this.ul.innerHTML = '';
        pagination.appendChild(this.ul);
        var that = this;
        //首页
        that.firstPage();
        //上一页
        that.lastPage();
        //分页
        that.getPages().forEach(function (item) {
            var li = document.createElement('li');
            if (item == that.curPage) {
                li.className = 'active';
            } else {
                li.onclick = function () {
                    that.curPage = parseInt(this.innerHTML);
                    that.init();
                    that.getPage(that.curPage);
                    console.log(this.innerHTML);
                    page = this.innerHTML;

                    var now_date = $('#now_date').val();
                    var now_p_change = $('#now_p_change').val();
                    var now_price_change = $('#now_price_change').val();
                    var now_volume = $('#now_volume').val();
                    console.log(now_date, now_p_change, now_price_change, now_volume);

                    list = {
                        'page': page,
                        'now_date': now_date,
                        'now_p_change': now_p_change,
                        'now_price_change': now_price_change,
                        'now_volume': now_volume
                    };
                    $.ajax({
                        //请求方式
                        type : "POST",
                        //请求的媒体类型
                        contentType: "application/json;charset=UTF-8",
                        //请求地址
                        url : "/page_ajax",
                        //数据，json字符串
                        data : JSON.stringify(list),
                        //请求成功
                        success : function(result) {
                            console.log(result['datas']);
                            var datas = result['datas'];
                            console.log(datas.length);
                            var len = datas.length;
                            if(len < 10){
                                var i = len;
                                var test = {
                                    'close': "",
                                    'code': "",
                                    'date': "",
                                    'high': "",
                                    'id': 0,
                                    'low': "",
                                    'ma10': "",
                                    'ma20': "",
                                    'ma5': "",
                                    'name': "",
                                    'open': "",
                                    'p_change': "",
                                    'p_mark': 0,
                                    'price_change': "",
                                    'price_mark': 0,
                                    'sort_id': 0,
                                    'volume': ""
                                };
                                for(;i < 10; i++){
                                    datas.push(test)
                                }
                            }
                            // console.log('&&&&&&&&&&', datas.length);
                            var num = 0;
                            $('#content > tr').each(function () {
                                // console.log(this);
                                var data = datas[num];
                                var children = $(this).children('td').children('div').children('h6');
                                $(children[1]).text(data['name']);
                                $(children[2]).text(data['code']);
                                $(children[3]).text(data['date']);
                                if(data['p_mark'] === 1){
                                    $(children[4]).css('color', '#dc3545');
                                }
                                else{
                                    $(children[4]).css('color', '#28a745');
                                }
                                $(children[4]).text(data['p_change']);
                                if(data['price_mark'] === 1){
                                    $(children[4]).css('color', '#dc3545');
                                }
                                else{
                                    $(children[4]).css('color', '#28a745');
                                }
                                $(children[5]).text(data['price_change']);
                                $(children[6]).text(data['volume']);
                                // console.log('........', data['volume'], data);
                                // console.log(children);
                                num++;
                            })
                        },
                        //请求失败，包含具体的错误信息
                        error : function(e){
                            console.log(e.status);
                            console.log(e.responseText);
                        }
                    });
                };
            }
            li.innerHTML = item;
            that.ul.appendChild(li);
        });
        //下一页
        that.nextPage();
        //尾页
        that.finalPage();

        //是否支持跳转
        if (that.showSkipInputFlag) {
            that.showSkipInput();
        }
        //是否显示总页数,每页个数,数据
        if (that.showPageTotalFlag) {
            that.showPageTotal();
        }
    },
    //首页
    firstPage: function firstPage() {
        var that = this;
        var li = document.createElement('li');
        li.innerHTML = '首页';
        li.id = 'fist';
        this.ul.appendChild(li);
        li.onclick = function () {
            var val = parseInt(1);
            that.curPage = val;
            that.getPage(that.curPage);
            that.init();

            var now_date = $('#now_date').val();
            var now_p_change = $('#now_p_change').val();
            var now_price_change = $('#now_price_change').val();
            var now_volume = $('#now_volume').val();
            console.log(now_date, now_p_change, now_price_change, now_volume);

            list = {
                'page': 1,
                'now_date': now_date,
                'now_p_change': now_p_change,
                'now_price_change': now_price_change,
                'now_volume': now_volume
            };
            $.ajax({
                //请求方式
                type : "POST",
                //请求的媒体类型
                contentType: "application/json;charset=UTF-8",
                //请求地址
                url : "/page_ajax",
                //数据，json字符串
                data : JSON.stringify(list),
                //请求成功
                success : function(result) {
                    console.log(result['datas']);
                    var datas = result['datas'];
                    console.log(datas.length);
                    var len = datas.length;
                    if(len < 10){
                        var i = len;
                        var test = {
                            'close': "",
                            'code': "",
                            'date': "",
                            'high': "",
                            'id': 0,
                            'low': "",
                            'ma10': "",
                            'ma20': "",
                            'ma5': "",
                            'name': "",
                            'open': "",
                            'p_change': "",
                            'p_mark': 0,
                            'price_change': "",
                            'price_mark': 0,
                            'sort_id': 0,
                            'volume': ""
                        };
                        for(;i < 10; i++){
                            datas.push(test)
                        }
                    }
                    // console.log('&&&&&&&&&&', datas.length);
                    var num = 0;
                    $('#content > tr').each(function () {
                        // console.log(this);
                        var data = datas[num];
                        var children = $(this).children('td').children('div').children('h6');
                        $(children[1]).text(data['name']);
                        $(children[2]).text(data['code']);
                        $(children[3]).text(data['date']);
                        if(data['p_mark'] === 1){
                            $(children[4]).css('color', '#dc3545');
                        }
                        else{
                            $(children[4]).css('color', '#28a745');
                        }
                        $(children[4]).text(data['p_change']);
                        if(data['price_mark'] === 1){
                            $(children[4]).css('color', '#dc3545');
                        }
                        else{
                            $(children[4]).css('color', '#28a745');
                        }
                        $(children[5]).text(data['price_change']);
                        $(children[6]).text(data['volume']);
                        // console.log('........', data['volume'], data);
                        // console.log(children);
                        num++;
                    })
                },
                //请求失败，包含具体的错误信息
                error : function(e){
                    console.log(e.status);
                    console.log(e.responseText);
                }
            });
        };
    },
    //上一页
    lastPage: function lastPage() {
        var that = this;
        var li = document.createElement('li');
        li.innerHTML = '<';
        li.id = 'previous';
        if (parseInt(that.curPage) > 1) {
            li.onclick = function () {
                that.curPage = parseInt(that.curPage) - 1;
                that.init();
                that.getPage(that.curPage);
                var now_date = $('#now_date').val();
                var now_p_change = $('#now_p_change').val();
                var now_price_change = $('#now_price_change').val();
                var now_volume = $('#now_volume').val();
                console.log(now_date, now_p_change, now_price_change, now_volume);

                list = {
                    'page': that.curPage,
                    'now_date': now_date,
                    'now_p_change': now_p_change,
                    'now_price_change': now_price_change,
                    'now_volume': now_volume
                };
                $.ajax({
                    //请求方式
                    type : "POST",
                    //请求的媒体类型
                    contentType: "application/json;charset=UTF-8",
                    //请求地址
                    url : "/page_ajax",
                    //数据，json字符串
                    data : JSON.stringify(list),
                    //请求成功
                    success : function(result) {
                        console.log(result['datas']);
                        var datas = result['datas'];
                        console.log(datas.length);
                        var len = datas.length;
                        if(len < 10){
                            var i = len;
                            var test = {
                                'close': "",
                                'code': "",
                                'date': "",
                                'high': "",
                                'id': 0,
                                'low': "",
                                'ma10': "",
                                'ma20': "",
                                'ma5': "",
                                'name': "",
                                'open': "",
                                'p_change': "",
                                'p_mark': 0,
                                'price_change': "",
                                'price_mark': 0,
                                'sort_id': 0,
                                'volume': ""
                            };
                            for(;i < 10; i++){
                                datas.push(test)
                            }
                        }
                        // console.log('&&&&&&&&&&', datas.length);
                        var num = 0;
                        $('#content > tr').each(function () {
                            // console.log(this);
                            var data = datas[num];
                            var children = $(this).children('td').children('div').children('h6');
                            $(children[1]).text(data['name']);
                            $(children[2]).text(data['code']);
                            $(children[3]).text(data['date']);
                            if(data['p_mark'] === 1){
                                $(children[4]).css('color', '#dc3545');
                            }
                            else{
                                $(children[4]).css('color', '#28a745');
                            }
                            $(children[4]).text(data['p_change']);
                            if(data['price_mark'] === 1){
                                $(children[4]).css('color', '#dc3545');
                            }
                            else{
                                $(children[4]).css('color', '#28a745');
                            }
                            $(children[5]).text(data['price_change']);
                            $(children[6]).text(data['volume']);
                            // console.log(children);
                            num++;
                        })
                    },
                    //请求失败，包含具体的错误信息
                    error : function(e){
                        console.log(e.status);
                        console.log(e.responseText);
                    }
                });
            };
        } else {
            li.className = 'disabled';
        }
        this.ul.appendChild(li);
    },
    //分页
    getPages: function getPages() {
        var pag = [];
        if (this.curPage <= this.pageTotal) {
            if (this.curPage < this.pageSize) {
                //当前页数小于显示条数
                var i = Math.min(this.pageSize, this.pageTotal);
                while (i) {
                    pag.unshift(i--);
                }
            } else {
                //当前页数大于显示条数
                var middle = this.curPage - Math.floor(this.pageSize / 2),
                    //从哪里开始
                    i = this.pageSize;
                if (middle > this.pageTotal - this.pageSize) {
                    middle = this.pageTotal - this.pageSize + 1;
                }
                while (i--) {
                    pag.push(middle++);
                }
            }
        } else {
            console.error('当前页数不能大于总页数');
        }
        if (!this.pageSize) {
            console.error('显示页数不能为空或者0');
        }
        return pag;
    },
    //下一页
    nextPage: function nextPage() {
        var that = this;
        var li = document.createElement('li');
        li.innerHTML = '>';
        li.id = 'next';
        if (parseInt(that.curPage) < parseInt(that.pageTotal)) {
            li.onclick = function () {
                that.curPage = parseInt(that.curPage) + 1;
                that.init();
                that.getPage(that.curPage);

                console.log(that.curPage);
                var now_date = $('#now_date').val();
                var now_p_change = $('#now_p_change').val();
                var now_price_change = $('#now_price_change').val();
                var now_volume = $('#now_volume').val();
                console.log(now_date, now_p_change, now_price_change, now_volume);

                list = {
                    'page': that.curPage,
                    'now_date': now_date,
                    'now_p_change': now_p_change,
                    'now_price_change': now_price_change,
                    'now_volume': now_volume
                };
                $.ajax({
                    //请求方式
                    type : "POST",
                    //请求的媒体类型
                    contentType: "application/json;charset=UTF-8",
                    //请求地址
                    url : "/page_ajax",
                    //数据，json字符串
                    data : JSON.stringify(list),
                    //请求成功
                    success : function(result) {
                        console.log(result['datas']);
                        var datas = result['datas'];
                        console.log(datas.length);
                        var len = datas.length;
                        if(len < 10){
                            var i = len;
                            var test = {
                                'close': "",
                                'code': "",
                                'date': "",
                                'high': "",
                                'id': 0,
                                'low': "",
                                'ma10': "",
                                'ma20': "",
                                'ma5': "",
                                'name': "",
                                'open': "",
                                'p_change': "",
                                'p_mark': 0,
                                'price_change': "",
                                'price_mark': 0,
                                'sort_id': 0,
                                'volume': ""
                            };
                            for(;i < 10; i++){
                                datas.push(test)
                            }
                        }
                        // console.log('&&&&&&&&&&', datas.length);
                        var num = 0;
                        $('#content > tr').each(function () {
                            // console.log(this);
                            var data = datas[num];
                            var children = $(this).children('td').children('div').children('h6');
                            $(children[1]).text(data['name']);
                            $(children[2]).text(data['code']);
                            $(children[3]).text(data['date']);
                            if(data['p_mark'] === 1){
                                $(children[4]).css('color', '#dc3545');
                            }
                            else{
                                $(children[4]).css('color', '#28a745');
                            }
                            $(children[4]).text(data['p_change']);
                            if(data['price_mark'] === 1){
                                $(children[4]).css('color', '#dc3545');
                            }
                            else{
                                $(children[4]).css('color', '#28a745');
                            }
                            $(children[5]).text(data['price_change']);
                            $(children[6]).text(data['volume']);
                            // console.log(children);
                            num++;
                        })
                    },
                    //请求失败，包含具体的错误信息
                    error : function(e){
                        console.log(e.status);
                        console.log(e.responseText);
                    }
                });
            };
        } else {
            li.className = 'disabled';
        }
        this.ul.appendChild(li);
    },
    //尾页
    finalPage: function finalPage() {
        var that = this;
        var li = document.createElement('li');
        li.innerHTML = '尾页';
        li.id = 'last';
        this.ul.appendChild(li);
        li.onclick = function () {
            var yyfinalPage = that.pageTotal;
            var val = parseInt(yyfinalPage);
            that.curPage = val;
            that.getPage(that.curPage);
            that.init();

            console.log(val);
            var now_date = $('#now_date').val();
            var now_p_change = $('#now_p_change').val();
            var now_price_change = $('#now_price_change').val();
            var now_volume = $('#now_volume').val();
            console.log(now_date, now_p_change, now_price_change, now_volume);

            list = {
                'page': val,
                'now_date': now_date,
                'now_p_change': now_p_change,
                'now_price_change': now_price_change,
                'now_volume': now_volume
            };
            $.ajax({
                //请求方式
                type : "POST",
                //请求的媒体类型
                contentType: "application/json;charset=UTF-8",
                //请求地址
                url : "/page_ajax",
                //数据，json字符串
                data : JSON.stringify(list),
                //请求成功
                success : function(result) {
                    console.log(result['datas']);
                    var datas = result['datas'];
                    console.log(datas.length);
                    var len = datas.length;
                    if(len < 10){
                        var i = len;
                        var test = {
                            'close': "",
                            'code': "",
                            'date': "",
                            'high': "",
                            'id': 0,
                            'low': "",
                            'ma10': "",
                            'ma20': "",
                            'ma5': "",
                            'name': "",
                            'open': "",
                            'p_change': "",
                            'p_mark': 0,
                            'price_change': "",
                            'price_mark': 0,
                            'sort_id': 0,
                            'volume': ""
                        };
                        for(;i < 10; i++){
                            datas.push(test)
                        }
                    }
                    // console.log('&&&&&&&&&&', datas.length);
                    var num = 0;
                    $('#content > tr').each(function () {
                        // console.log(this);
                        var data = datas[num];
                        var children = $(this).children('td').children('div').children('h6');
                        $(children[1]).text(data['name']);
                        $(children[2]).text(data['code']);
                        $(children[3]).text(data['date']);
                        if(data['p_mark'] === 1){
                            $(children[4]).css('color', '#dc3545');
                        }
                        else{
                            $(children[4]).css('color', '#28a745');
                        }
                        $(children[4]).text(data['p_change']);
                        if(data['price_mark'] === 1){
                            $(children[4]).css('color', '#dc3545');
                        }
                        else{
                            $(children[4]).css('color', '#28a745');
                        }
                        $(children[5]).text(data['price_change']);
                        $(children[6]).text(data['volume']);
                        // console.log(children);
                        num++;
                    })
                },
                //请求失败，包含具体的错误信息
                error : function(e){
                    console.log(e.status);
                    console.log(e.responseText);
                }
            });
        };
    },
    //是否支持跳转
    showSkipInput: function showSkipInput() {
        var that = this;
        var li = document.createElement('li');
        li.className = 'totalPage';
        var span1 = document.createElement('span');
        span1.innerHTML = '跳转到';
        li.appendChild(span1);
        var input = document.createElement('input');
        input.onkeydown = function (e) {
            var oEvent = e || event;
            if (oEvent.keyCode == '13') {
                var val = parseInt(oEvent.target.value);
                if (typeof val === 'number' && val <= that.pageTotal) {
                    that.curPage = val;
                    that.getPage(that.curPage);
                }else{
                    alert("跳转页数不能大于总页数 !")
                }
                that.init();
            }
        };
        li.appendChild(input);
        var span2 = document.createElement('span');
        span2.innerHTML = '页';
        li.appendChild(span2);
        this.ul.appendChild(li);
    },
    //是否显示总页数,每页个数,数据
    showPageTotal: function showPageTotal() {
        var that = this;
        var li = document.createElement('li');
        li.innerHTML = '共&nbsp' + that.pageTotal + '&nbsp页';
        li.className = 'totalPage';
        this.ul.appendChild(li);
        var li3 = document.createElement('li');
        li3.innerHTML = '合计&nbsp' + that.dataTotal + '&nbsp条数据';
        li3.className = 'totalPage';
        this.ul.appendChild(li3);
    }
};