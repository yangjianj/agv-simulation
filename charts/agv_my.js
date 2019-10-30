$(function(){
    var dom = document.getElementById("container");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;
    var symbol = 'emptyCircle';
    var symbolSize = 10;
    var linedata = {
                'name':["a","b"],
                'data':[[[100,900],[300,900],[300,700],[100,700],[100,900]],
                [[800,500],[800,300],[800,200],[800,300],[500,300],[500,500],[800,500]]]
                };
    //var linelist = ["a","b"]
    var points = [];

    option = {
        title: {
            text: 'Click to Add Points',
            show: false
        },
        tooltip: {
            formatter: function (params) {
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
            max: 1000,
            interval: 100,
            type: 'value',
            axisLine: {onZero: false}
        },
        yAxis: {
            min: 0,
            max: 1000,
            interval: 100,
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
                              {symbol: 'pin',value:'站点1',symbolSize:50,xAxis:100,yAxis:900},
                              {symbol: 'pin',value:'站点2',symbolSize:50,xAxis:300,yAxis:700},
                              {symbol: 'circle',value:'1',symbolSize:20,xAxis:150,yAxis:700}, ]
                            },
                data: linedata.data[0]
            },
            {
                id: linedata.name[1],
                type: 'line',
                smooth: false,
                color: '#ff0000',
                symbolSize: symbolSize,
                markPoint:{
                            symbol: 'circle',
                            data:[
                              {symbol: 'pin',value:'充电',xAxis:800,yAxis:200},
                               {symbol: 'circle',value:'2',symbolSize:20,xAxis:700,yAxis:300},
                                ]
                            },
                data: linedata.data[1]
            }
        ]
    };

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
    }); */

    zr.on('mousemove', function (params) {
        var pointInPixel = [params.offsetX, params.offsetY];
        zr.setCursorStyle(myChart.containPixel('grid', pointInPixel) ? 'copy' : 'default');
    });

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }

    var sock = null;
    var serversocket = "ws://127.0.0.1:8080/wsocket";
    sock = new WebSocket(serversocket);
    sock.onopen = function(){
        console.log("connect to "+serversocket);
    }
    sock.onclose = function(e){
        console.log("connect closed("+e.code+")");
    }

    sock.onmessage = function(e){
        console.log("message recevice:"+e.data);
        //var redata = eval(e.data);
        var redata =jQuery.parseJSON(e.data);
        var pointlist = redata.message 

        addpoint(pointlist)
    }

    function send(){
        var smsg = "123456";
        sock.send(smsg);
    }
    
    function addpoint(params){
        for(var i=0;i<params.length;i++){

            var pointInPixel = [params[i].offsetX, params[i].offsetY];
            var pointInGrid = myChart.convertFromPixel('grid', pointInPixel);

            if (myChart.containPixel('grid', pointInPixel)) {
                data[i].push(pointInGrid);
                myChart.setOption({
                    series: [{
                        id: linelist[i],
                        data: data[i]
                    }]
                });
            }
        }
        
    }

})
