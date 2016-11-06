$(document).ready(function(){
  $(".question").hide();
  $("#q0").show();
  var last = 0;
  for (var i = 0; i < 6; i++){
    if ($("#q"+i).length) {
      (function(){
        var i2 = i;
        $("#"+i2+"yes").click(function(){
          $("#"+i2+"button").val("1");
          $("#q"+i2).slideUp();
          $("#q"+(i2+1)).slideDown();
        });
        $("#"+i2+"no").click(function(){
          $("#"+i2+"button").val("0");
          $("#q"+i2).slideUp();
          $("#q"+(i2+1)).slideDown();
        });
        $("#"+i2+"button").click(function(){
          $("#q"+i2).slideUp();
          $("#q"+(i2+1)).slideDown();
        });
      })();
      last = i;
    } else {
      last = i - 2;
      $("#"+last+"yes").click(function(){
        $("#"+last+"button").val("1");
        setTimeout(function(){ $("#form").submit(); }, 2000);
      });
      $("#"+last+"no").click(function(){
        $("#"+last+"button").val("0");
        setTimeout(function(){ $("#form").submit(); }, 2000);
      });
      $("#"+last+"button").click(function(){
        setTimeout(function(){ $("#form").submit(); }, 2000);
      });
    }

  }

})
