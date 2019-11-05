$(function(){
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

 function jsonpcallback(data){
 var re = JSON.serialize(data);
 console.log(re);
 }
})
