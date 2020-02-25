    // $(document).ready(function() {
    //     namespace = '/test';
    //     var pcsocket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    //
    //     pcsocket.on('server_response', function(res) {
    //         update_mychart(res);
    //     });
    //
    // });

    $(document).ready(function() {
        // 设置命名空间
        namespace = '/capture';
        // 这种方法也可以
        // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
        // 创建套接字连接
        var socket = io(namespace);


            socket.on('connect', function() {
// alert(1);
                socket.emit('startpc', {data: 'no'});
                socket.emit('startsniff', {data: 'no'});
            });
         $("#startproject").click(function () {
             // 向服务器发送请求，要求立刻抓取
                socket.emit('startpc', {data: 'start'});
                socket.emit('startsniff', {data: 'start'});
        })

            socket.on("testresponse",function (data) {
                alert(data)
            })
        // PC数据传输与接受
        socket.on('pcinfo_response', function (data) {
            var cpuinfo = String(data['cpu']);var diskinfo = String(data['disk']);
            var meminfo = String(data['mem']);
            $('#div_cpu').text(cpuinfo+'%').attr({
                    "aria-valuenow":cpuinfo,
                    "style": "min-width: 2em;width:"+ cpuinfo +"%;",
                    "class": data['cpu']<40? "progress-bar progress-bar-success" :(data['cpu']<70 ? "progress-bar progress-bar-warning" : "progress-bar progress-bar-danger")
                }),

                $('#div_disk').text(diskinfo+'%').attr({
                    "aria-valuenow":diskinfo,
                    "style": "min-width: 2em;width:"+ diskinfo +"%;",
                    "class": data['disk']<40? "progress-bar progress-bar-success" :(data['disk']<70 ? "progress-bar progress-bar-warning" : "progress-bar progress-bar-danger")
                }),

                $('#div_mem').text(meminfo+'%').attr({
                    "aria-valuenow":meminfo,
                    "style": "min-width: 2em;width:"+ meminfo +"%;",
                    "class": data['mem']<40? "progress-bar progress-bar-success" :(data['mem']<70 ? "progress-bar progress-bar-warning" : "progress-bar progress-bar-danger")
                }),

                $('#div_net_up').text(data['send']),
                $('#div_net_down').text(data['recv'])
        })

        socket.on('packet_response', function (data) {
            // alert(JSON.stringify(data))
            $("#capture_table").bootstrapTable('insertRow', {
        index: 0,
        row: {
          id: data['id'],
             sourceip: data['sourceip'],
             destinip: data['destinip'],
             protocol: data['protocol'],
            ttl:data['ttl'],
            time:data['time'],
            level:"<span class='label label-"+data['level']+"'>"+data['level']+"</span>",
            dump:data['dump']
        }
       });
            if(data['isdanger'] == 1) {
                var stabledata = $('#statistic_table').bootstrapTable('getData', {
                    useCurrentPage: false,
                    includeHiddenRows: true
                });
                var havesame = 0;
                // alert(JSON.stringify(stabledata))
                for (inner in stabledata) {
                    // alert(JSON.stringify(stabledata[inner]['evilip']==data['sourceip']));
                    if (stabledata[inner]['evilip']==data['sourceip']) {
                        // alert(stabledata[inner]['evilip']);
                        // $('#statistic_table').bootstrapTable('updateCellByUniqueId', {
                        //     id: stabledata[inner]['evilip'],
                        //     field: 'times',
                        //     value: stabledata[inner]['times']+1
                        // });
                        havesame = 1;
                        // alert(30);
                        break;
                    }
                }
                if(havesame == 0){
                    $('#statistic_table').bootstrapTable('insertRow', {
                        index: 0,
                        row: {
                            evilip: data['sourceip'],
                            times: 1
                        }
                    })
                }

            }})

        socket.on('notify_response', function (data) {
            // alert(data['data'])
            $('#table_notify_text').bootstrapTable('insertRow',{
                index:0,
                row:{
                    msg : data['msg'],
                    data: data['data']
                }
            })

        })
    });

