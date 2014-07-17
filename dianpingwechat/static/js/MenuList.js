$(function(){
  setInterval("flushMenu()", 1000);
});
var count =0;
function flushMenu(){
  $('#reslist').append('测试'+ count++ +'下');
}