$(function(){
    var dom = document.getElementById("container");
    var myChart = echarts.init(dom);
    option = null;
    var symbol = 'emptyCircle';
    var symbolSize = 10;
    var linedata = {
        'name':["car1","car2"],
       // 'data':[[[100,900],[300,900],[300,700],[100,700],[100,900]],
        //    [[800,500],[800,300],[800,200],[800,300],[500,300],[500,500],[800,500]]]
        'data':[[],[]]
    };
    var newseries = [];
    var series_template = {
                id: 'id1',
                type: 'line',
                smooth: false,
                color: '#00ef00',
                symbol: symbol,
                symbolSize: symbolSize,
                //animation:false,
                markPoint:{
                           //symbol: 'pin',

                            data:[
                                {symbol: 'circle',value:'1',symbolSize:20,xAxis:150,yAxis:700},
                                //{symbol: 'pin',value:'站点1',symbolSize:50,xAxis:100,yAxis:900},
                                //{symbol: 'pin',value:'站点2',symbolSize:50,xAxis:300,yAxis:700},
                               ]
                            },
                data: 'linedata'
            }

    option = {
        title: {
            text: 'Click to Add Points',
            show: false
        },
        tooltip: {
            formatter: function (params) {
                console.log(params);
                if (params.componentType == "markPoint"){
                    var name = params.data.name;
                    var speed = params.data.speed;
                    var x = params.data.xAxis;
                    var y = params.data.yAxis;
                    return ('name:'+name+'</br>'
                    +'speed:'+speed+'</br>'
                    +'xy:'+x.toFixed(2)+','+y.toFixed(2)+'</br>'
                    )
                }
                var data = params.data || [0, 0];
                return data[0].toFixed(2) + ', ' + data[1].toFixed(2);
            }
        },
        grid: {
            left: '0.2%',
            right: '1%',
            top:'1%',
            bottom: '1%',
            containLabel: true
        },
        xAxis: {
            min: 0,
            max: 10000,
            interval: 1000,
            type: 'value',
            axisLine: {onZero: false}
        },
        yAxis: {
            min: 0,
            max: 10000,
            interval: 1000,
            type: 'value',
            axisLine: {onZero: false}
        },
        series: [
            {
                id: linedata.name[0],
                type: 'line',
                smooth: false,
                color: '#00ef00',
                symbol: symbol,
                symbolSize: symbolSize,
                //animation:false,
                markPoint:{
                           //symbol: 'pin',
                            data:[
                                //{symbol: 'circle',value:'1',symbolSize:20,xAxis:150,yAxis:700},
                               ]
                            },
                data: linedata.data[0]
            }
        ]
    };

    var sock = null;
    var serversocket = "ws://127.0.0.1:8080/markpoint";
    sock = new WebSocket(serversocket);

    var zr = myChart.getZr();

/*
    zr.on('click', function (params) {
        var pointInPixel = [params.offsetX, params.offsetY];
        var pointInGrid = myChart.convertFromPixel('grid', pointInPixel);

        if (myChart.containPixel('grid', pointInPixel)) {
            data.push(pointInGrid);

            myChart.setOption({
                series: [{
                    id: 'a',
                    data: data,
                }]
            });
        }
    });
        */

    zr.on('mousemove', function (params) {
        var pointInPixel = [params.offsetX, params.offsetY];
        zr.setCursorStyle(myChart.containPixel('grid', pointInPixel) ? 'copy' : 'default');
    });

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }

    sock.onopen = function(){
        console.log("connect to "+serversocket);
    }
    sock.onclose = function(e){
        console.log("connect closed("+e.code+")");
    }

    sock.onmessage = function(e){
        //console.log("message recevice:"+e.data);
        //var redata = eval(e.data);
        var redata =jQuery.parseJSON(e.data);
        if(redata.line != null){
            var line = redata.line ;
            addpoint(line)   //根据获取数据初始化图像
        }else{
            var pointlist = redata.markpoint ;
            var point = redata.markpoint ;
            change_position(point);
        }
    }

    function send(){
        var smsg = "123456";
        sock.send(smsg);
    }
    
    function addpoint(params){   //line 增加端点

        for(var i=0;i<params.length;i++){
                var obj1=Object.assign({},series_template);
                obj1.id = params[i]['name'];
                obj1.data = params[i]['data'];
                obj1.markPoint = params[i]['markPoint'];
                obj1.color = params[i]['color'];
                newseries.push(obj1);
        }
         myChart.setOption({
                    series: newseries
                });
    }

    function change_position(params){  //改变markpoint 位置

        var carname = params.data.name;
        var markpoint_data = null;
        for (var i=0;i<newseries.length;i++){
            if(newseries[i].id == params.data.name){
                newseries[i].markPoint.data[0].xAxis = params.data.position[0];
                newseries[i].markPoint.data[0].yAxis = params.data.position[1];
                newseries[i].markPoint.data[0].speed = params.data.speed;
                markpoint_data = newseries[i].markPoint.data;
            }
        }

        myChart.setOption({
                    series: [{
                            id: carname,  //改变对应object的值
                            markPoint:{
                                   data:markpoint_data
                                    },
                    }]
                });
    }
})
