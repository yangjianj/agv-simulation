$(function(){
$("#submit").click(function(){

  //var targetUrl = $("#addForm").attr("action");
  var data = $("#ff").serialize();
  console.log(1111);
  console.log(data);

   $.ajax({
        type:'POST',
        url:'http://127.0.0.1:8080/submit',
        data:data,  //重点必须为一个变量如：data
        dataType:'json',
        success:function(data){
        console.log('success');
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
