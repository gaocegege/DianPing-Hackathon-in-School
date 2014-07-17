$(function(){

	var str,roomnostr; 
	str = location.href; 
	roomnostr = str.split("?")[1];
	
	$.get("/polls/"+roomnostr, function(data){
		//testjson = JSON.parse(data);
	  	ctjsonobj= data;//eval('('+data+')');
  		//console.log(ctjsonobj);
  		if(ctjsonobj.status == 'OK'){
  			var bslist = ctjsonobj.businesses;
  			var buf= '<table class="table"><tbody>';
  			for(var i=0;i<bslist.length;++i){

  				buf+='<tr><td><label><input type="checkbox"></label></td><td><img style="width:70%;" src="'
  				+bslist[i].s_photo_url+'"></td><td>'+bslist[i].name+'</td></tr>';
  			}
  			buf+='</tbody></table>';
  			$('#reslist').append(buf);
  		}else{
  			alert("error");
  		}
  	});
});