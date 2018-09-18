function ttc(){
            method = $('.nav-item.active.method').text();
            area = $(".area.option-list a.on").text();
            subway = $(".subway.option-list a.on").text();
            suboption = $('#line-sub-list a.on').text()
            zffs = $(".zffs.option-list a.on").text();
            jushi = $(".jushi.option-list a.on").text();
            filter = $(".filter.option-list a.on").text();
            tag = $(".tag.option-list a.on").text();
            search = $("#searchipt").val()

            result = {
                'method': method,
                'area': area,
                'subway': subway,
                'suboption': suboption,
                'zffs': zffs,
                'jushi': jushi,
                'filter': filter,
                'tag': tag,
                'search': search
            }
            
            return result;
        }

        function add_sublist_click_function(){
            $("#line-sub-list a").click(function(e) {
                $("#searchipt").val('')
                $("#line-sub-list a").removeClass('on');
                $(e.target).addClass('on');

                $("#table").bootstrapTable('destroy');
                update_table(ttc())
            });
        }


        function update_table(parameters) {
            console.log(parameters)
            $('#table').bootstrapTable({
                url: '/jsondata',
                method: 'get',
                queryParams: function (p) {
                    return {
                        id: 'aa', 
                        limit: p.limit,
                        offset: p.offset,
                        method: parameters['method'],
                        area: parameters['area'],
                        subway: parameters['subway'],
                        suboption: parameters['suboption'] ,
                        zffs: parameters['zffs'],
                        jushi: parameters['jushi'],
                        filter: parameters['filter'],
                        tag: parameters['tag'],
                        search: parameters['search']
                    };
                },
                dataType: "json",
                pagination: true, //前端处理分页
                singleSelect: false,//是否只能单选
                search: false, //显示搜索框，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
                striped: false, //是否显示行间隔色
                cache: false, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                pageNumber: 1, //初始化加载第10页，默认第一页
                pageSize: 15, //每页的记录行数（*）
                pageList: [15, 30, 60, 100], //可供选择的每页的行数（*）
                strictSearch: true,//设置为 true启用 全匹配搜索，false为模糊搜索
                showColumns: false, //显示内容列下拉框
                showRefresh: false, //显示刷新按钮
                minimumCountColumns: 2, //当列数小于此值时，将隐藏内容列下拉框
                clickToSelect: true, //设置true， 将在点击某行时，自动勾选rediobox 和 checkbox
                uniqueId: "id", //每一行的唯一标识，一般为主键列
                showToggle: false, //是否显示详细视图和列表视图的切换按钮
                cardView: false, //是否显示详细视图
                detailView: false, //是否显示父子表，设置为 true 可以显示详细页面模式,在每行最前边显示+号#}
                sidePagination: "server", //分页方式：client客户端分页，server服务端分页（*）
                buttonsClass: 'light',
                columns: [
                {
                    field: 'title',
                    title: '租房信息',
                    align: 'left',
                    formatter: function (value, row, index) {
                        var color = value.flag == '0'? 'text-dark' : '"text-danger"'
                        var e = '<a class=' + color + ' ' + 'target="_blank"  href="' + value.href + '">' + value.title + '</a>'
                        e = '<div>' + e + '</div>'
                        return e;
                    }
                }, {
                    field: 'post_time',
                    title: '发布时间',
                    align: 'center',
                    width: '14.8%',
                }, {
                    field: 'user',
                    title: '是否中介',
                    align: 'center',
                    width: '12%',
                    formatter: function (value, row, index) {
                        var color = value.flag == '0'? '' : 'bg-dark text-white'
                        var e = '<div class="' + color + ' ">' + value.u + '</div> '
                        return e;
                    }
                },{
                    field: 'source',
                    title: '来源',
                    align: 'center',
                    width: '10%'
                }],
            });
        }



        function get_sub_options(type_p, value) {
            $.ajax({
                url: '/get_sub_options',
                type: 'get',
                data: {
                        'type': type_p,
                        'value': value
                      },
                dataType: 'json',
                success: function(data) {
                    var bodyFa = document.getElementById("line-sub-list");
                    bodyFa.innerHTML = ""
                    var a = document.createElement("a");
                    a.innerText = '不限'
                    a.classList.add('on')
                    a.classList.add('suball')
                    a.href = '#'
                    bodyFa.appendChild(a);

                    //<a class="allsub on" href="#" id="0">不限</a>

                    for (var i = 0; i < data['data'].length; i++) {
                        var a=document.createElement("a");
                        a.innerText = data['data'][i];
                        a.href = '#';
                        bodyFa.appendChild(a);
                    }
                    add_sublist_click_function()
                }
            })
        }


        $(function(){

            $("#comment-btn").click(function(e) {
                $.ajax({
                    url: '/comment',
                    type: 'get',
                    data: {
                            'comment': $('#comment-area').val()
                          },
                    dataType: 'json',
                    success: function(data) {
                        $("#myModal").modal();
                        $('#comment-area').val("")
                    }
                })

            });


            $("#searchbtn").click(function(e) {
                parameters = ttc()
                parameters['search'] = $("#searchipt").val()
                $("#table").bootstrapTable('destroy');
                update_table(parameters)

            });


            $(".mynav-item").click(function(e) {
                $(".option-list a").removeClass('on'); 
                $('.all').addClass('on');
                $("#line-sub-list a").removeClass('on');
                $('.allsub').addClass('on');
                $('#line-sub-list').hide()
                $('#addinfo').show()

                parameters = ttc()
                parameters['method'] = e.target.innerHTML;
                $("#table").bootstrapTable('destroy');
                update_table(parameters)
            });

            $("#nav-map-tab").click(function() {
                $('#addinfo').hide();
                setTimeout(function(){
                    var point={
                        lng:116.405706,
                        lat:39.91582
                    };

                    p = new BMap.Point(point.lng,point.lat);
                    mymap.centerAndZoom(p, 12);  //设置地图显示中间点、地图显示级别
                 },100);

            });

            $(".area.option-list a").click(function(e) {
                $("#searchipt").val('')
                $(".area.option-list a").removeClass('on');
                $(e.target).addClass('on'); 
                $("#line-sub-list a").removeClass('on');
                $('#line-sub-list').show();
                $('.allsub').addClass('on');

                get_sub_options('area', e.target.innerHTML)
                $("#table").bootstrapTable('destroy');
                update_table(ttc())
            });

            $(".subway.option-list a").click(function(e) {
                $("#searchipt").val('')
                $(".subway.option-list a").removeClass('on');
                $(e.target).addClass('on'); 
                $("#line-sub-list a").removeClass('on');
                $('#line-sub-list').show();
                $('.allsub').addClass('on');

                get_sub_options('subway', e.target.text)
                
                $("#table").bootstrapTable('destroy');
                update_table(ttc())
            });

            $(".hide.all").click(function(e) {
                $("#searchipt").val('')
                $('#line-sub-list').hide()
            });


            $(".zffs.option-list a").click(function(e) {
                $(".zffs.option-list a").removeClass('on');
                $(e.target).addClass('on');

                $("#table").bootstrapTable('destroy');
                update_table(ttc())
            });

            $(".jushi.option-list a").click(function(e) {
                $(".jushi.option-list a").removeClass('on');
                $(e.target).addClass('on');

                $("#table").bootstrapTable('destroy');
                update_table(ttc())
            });

            $(".filter.option-list a").click(function(e) {
                $(".filter.option-list a").removeClass('on');
                $(e.target).addClass('on');

                $("#table").bootstrapTable('destroy');
                update_table(ttc())
            });

            $(".tag.option-list a").click(function(e) {
                $(".tag.option-list a").removeClass('on');
                $(e.target).addClass('on');

                $("#table").bootstrapTable('destroy');
                update_table(ttc())
            });

        })



function AddMap(){
        //设置地图容器高度
        var screenH = window.innerHeight / 2;
        var headerH = this.elById("map_show").offsetHeight;
        this.elById("map_show").style.height = screenH-headerH+"px";
    }

    /**
     * @param el 地图初始化容器
     * @param p  初始化坐标点
     */
    AddMap.prototype.init=function(el,p){
        var point={
            lng:116.405706,
            lat:39.91582
        };
        if(p && p.lng && p.lat){
            point.lng=p.lng;
            point.lat=p.lat;
        }
        this.m = new BMap.Map(el);      //实例化地图
        this.p = new BMap.Point(point.lng,point.lat);

        this.m.enableContinuousZoom();    //启用地图惯性拖拽
        this.m.enableScrollWheelZoom();   //启用滚轮放大缩小
        this.m.centerAndZoom(this.p, 12);  //设置地图显示中间点、地图显示级别

        this.search();               //搜索
        return this.m
    };


    AddMap.prototype.elById=function(id) {
        return document.getElementById(id);
    };




    //添加坐标显示
    AddMap.prototype.addMaker=function(location){
        var mk = new BMap.Marker(location);
        //mk.enableDragging();        //marker可拖拽
        mk.enableMassClear();
        this.m.addOverlay(mk); //在地图中添加marker
        mk.addEventListener('click', function() {
            alert(mk.getPosition());
        })
        var _this=this;

    };

    //搜索
    AddMap.prototype.search=function(){
        var _this=this;
        var ac = new BMap.Autocomplete(    //建立一个自动完成的对象
                {
                    "input" : "suggestId",
                    "location" : _this.m
                }
        );
        ac.addEventListener("onconfirm", function(e) {  
            var _value = e.item.value;
            myValue = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;
            _this.setPlace(_this.m);
        });
    };

    //定位到具体位置
    AddMap.prototype.setPlace=function(m){
        var _this=this;
        //m.clearOverlays();    //清除地图上所有覆盖物
        function myFun(){
            var pp = local.getResults().getPoi(0).point;    //获取第一个智能搜索的结果
            m.centerAndZoom(pp, 15);  //设置地图显示中间点、地图显示级别
            //_this.addMaker(pp);
        }
        var local = new BMap.LocalSearch(m, { //智能搜索
            onSearchComplete: myFun
        });
        local.search(myValue);
    };