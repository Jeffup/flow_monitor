$('#capture_table').bootstrapTable({
    height: '600',

//     search: true,
//     showSearchButton: true,
//     searchOnEnterKey: true,
//     queryParams: function queryParams(params) { //设置查询参数
//     var param = {
//         csrfmiddlewaretoken :$("input[name='csrfmiddlewaretoken']").val(),
//         pageNumber: params.pageNumber,
//         pageSize: params.pageSize,
//         search:$("input[ name='search_text' ] ").val(), //定义传输的搜索参数
//         order:params.sortOrder,
//         sort:params.sortName
//     };
//     return param;
// },
    search: true, //开启刷选
    detailView: true,
    detailFormatter:"detailFormatter",
    //表格汉化
    data_local: "zh-US",
    //设置为 true 会有隔行变色效果
    striped: true,
    //表头
  columns: [{
    field: 'id',
    title: '#',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  }, {
    field: 'sourceip',
    title: '源地址',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  }, {
    field: 'destinip',
    title: '目的地址',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  }, {
    field: 'protocol',
    title: '协议',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  }, {
    field: 'ttl',
    title: 'TTL',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  }, {
    field: 'time',
    title: '时间',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  }, {
    field: 'level',
    title: '威胁等级',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  }, ]
})

$("#statistic_table").bootstrapTable({
    height: '300',
    detailView: false,
    uniqueId:"evilip",
    //表格汉化
    data_local: "zh-US",
    //设置为 true 会有隔行变色效果
    striped: true,
    //表头
    onSort:function(name,order)
            {
              $('#statistic_table').bootstrapTable('refreshOptions', {
               sortName:name,
               sortOrder:order
              })},
  columns: [{
    field: 'evilip',
    title: '恶意地址',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  }, {
    field: 'times',
    title: '统计数量',
    align: 'center',//对其方式
    valign: 'middle',//对其方式
       sortable:true
  }, ]
})

// $("#div_net_up").text(20)

$('#table_notify_text').bootstrapTable({
    height: '200',
    //表格汉化
    data_local: "zh-US",
    //设置为 true 会有隔行变色效果
    striped: true,
    //表头
  columns: [{
    field: 'msg',
    align: 'center',//对其方式
    valign: 'middle'//对其方式
  },],
   onClickCell: function (field, value, row, $element) {
                alert(row['data']);
            }
})



 function detailFormatter(index, row) {
    var html = []
    // $.each(row, function (key, value) {
    //   html.push('<p><b>' + key + ':</b> ' + value + '</p>')
    // });
     html.push('<p>' + row['dump'] + '</p>')
    return html.join('');
  }