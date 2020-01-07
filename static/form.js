$(function(){
    /*
    var dd = [{'id':1,'text':'yyy'},{'id':2,'text':'ii'}]
    $('#cc').combobox({
        //url:'127.0.0.1:8080/get_json',
        valueField:'id',
        textField:'text',
        data:dd
    });
    */
    var carsdata = null;
    getData();

$("#submit").click(function(){
  //var targetUrl = $("#addForm").attr("action");
  //var data = $("#ff").serialize();
  var fileds = $("#ff").serializeArray();  //form表单生成数组
  var data={};
  $.each(fileds,function(index,filed) {  //数组转为json对象
          data[filed.name] = filed.value;
      }
  )
  console.log(data);

   $.ajax({
        type:'POST',
        url:'http://127.0.0.1:8080/submit',
        contentType:"application/json; charset=utf-8",
        data:JSON.stringify(data),  //json数组
        dataType:'json',
        success:function(data){
            //var response = jQuery.parseJSON(data);
            if(data.status != 'ok'){
                alert('input params error !')
            }
        },
        error:function(error){
            console.log(error)
        }
   })
return false   //不重新加载页面
})

    function getData(){
        $.ajax({
             type: "GET",
             url: 'http://127.0.0.1:8080/get_json',
             data: {},
             dataType: "json",
             success: function(response){
                 console.log('in get_json');
             console.log(response);
             carsdata = response.data;
                var html_name = '';
               for(var i=0;i<carsdata.length;i++){
                html_name +='<option value="'+carsdata[i].name+'">'+carsdata[i].name+'</option>';
               }
               $('#cc').append(html_name);

               var htmlx = '';
               for(var k in carsdata[0].sites) {
                    htmlx += '<option value="[' + carsdata[0].sites[k] + ']">[' + carsdata[0].sites[k] + ']</option>';
                }
                $('#cc1').children().remove();
                $('#cc1').append(htmlx);
                $('#src').children().remove();
                $('#src').append(htmlx);

                var html_mode = '';
               for(var i=0;i<response.workmode.length;i++){
                html_mode +='<option value="'+response.workmode[i]+'">'+response.workmode[i]+'</option>';
               }
               $('#mode').append(html_mode);
                /*
                //src
               var htmlx = '';
               for(var k in carsdata[0].sites) {
                    htmlx += '<option value="[' + carsdata[0].sites[k] + ']">[' + carsdata[0].sites[k] + ']</option>';
                }
                $('#src').children().remove();
                $('#src').append(htmlx);
                */
             },
             error:function(e){
             console.log('error:',e);
             }
         });}


$("#cc").change(function(){

    var selected = $("#cc").val();
    for(var i=0;i<carsdata.length;i++){
        if(selected == carsdata[i].name){
            //console.log(carsdata[i].sites);
            var html = '';
            for(var k in carsdata[i].sites) {
                html += '<option value="[' + carsdata[i].sites[k] + ']">[' + carsdata[i].sites[k] + ']</option>';
            }
            $('#cc1').children().remove();
            $('#cc1').append(html);
            $('#src').children().remove();
            $('#src').append(html);
        }
    }
});
})
