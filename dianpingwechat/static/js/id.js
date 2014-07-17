function showMenu(busiid){
	//roomnostr=10000;
	$.get("/polls/menu2/" + busiid + "/" +roomnostr, function(data){
	//$.get("/polls/menu/" + busiid + "/" +roomnostr, function(data){
		list = data;
		for (var i = list.length - 1; i >= 0; i--) {
            var buf =
            '<div data-role="collapsible" data-collapsed-icon="carat-d" data-expanded-icon="carat-u">'
        	+'<h4>'+list[i].category+'</h4>'
        	+'<ul data-role="listview" data-inset="false">';
			for(var j=list[i].dishes.length-1;j>=0;j--){
        		buf+='<li><div class="ui-grid-b" onclick="mountup('+i+','+j+')" >'
				+'<div class="ui-block-a ui-a-ccz"><div class="ui-bar ui-bar-a" style="height:50px">'+list[i].dishes[j].dish_name+'</div></div>'
				+'<div class="ui-block-b ui-b-ccz"><div class="ui-bar ui-bar-a" style="height:50px">￥'+list[i].dishes[j].price+'.00</div></div>'
				+'<div class="ui-block-c ui-c-ccz"><div class="ui-bar ui-bar-a" style="height:50px" id="dish'+list[i].dishes[j].id+'">'+list[i].dishes[j].amount+'份</div></div>'
				+'</div></li>';
			}
        	buf+='</ul>'
			+'</div>';

		 //    '<div class="ui-grid-c" onclick="mountup('+i+')" >'
		 //    +'<div class="ui-block-a"><div class="ui-bar ui-bar-a" style="height:60px">'+list[i].dish_name+'</div></div>'
		 //    +'<div class="ui-block-b"><div class="ui-bar ui-bar-a" style="height:60px">'+list[i].category+'</div></div>'
		 //    +'<div class="ui-block-c"><div class="ui-bar ui-bar-a" style="height:60px">'+list[i].price+'</div></div>'
		 //    +'<div class="ui-block-d"><div class="ui-bar ui-bar-a" style="height:60px" id="dish'+list[i].id+'">'+list[i].amount+'</div></div>'
			// +'</div>';
            $("#menulist").append(buf).trigger("create");
            
        }

   //      for (var i = list.length - 1; i >= 0; i--) {
   //          var buf = 
		 //    '<div class="ui-grid-c" onclick="mountup('+i+')" >'
		 //    +'<div class="ui-block-a"><div class="ui-bar ui-bar-a" style="height:60px">'+list[i].dish_name+'</div></div>'
		 //    +'<div class="ui-block-b"><div class="ui-bar ui-bar-a" style="height:60px">'+list[i].category+'</div></div>'
		 //    +'<div class="ui-block-c"><div class="ui-bar ui-bar-a" style="height:60px">'+list[i].price+'</div></div>'
		 //    +'<div class="ui-block-d"><div class="ui-bar ui-bar-a" style="height:60px" id="dish'+list[i].id+'">'+list[i].amount+'</div></div>'
			// +'</div>';
   //          $("#menulist").append(buf).trigger("create");
            
   //      }
        setInterval("flushMenu()", 5000);
	});
}
$(document).on("pageshow","#page2",function(){
		//showMenu(bId);
		showMenu("2552704");
});
function mountup(i,j){
    $.get("/polls/adddish/" + roomnostr + "/" +list[i].dishes[j].dish_name, function(data){
        $('#dish'+list[i].dishes[j].id).html(data+'份');
    });
}
// function mountup(i){
//     $.get("/polls/adddish/" + roomnostr + "/" +list[i].dish_name, function(data){
//         $('#dish'+list[i].id).html(data);
//     });
// }
function flushMenu(){
	$.get("/polls/checkorder/" + roomnostr, function(data){
        
        for(var i = data.length-1;i>=0;i--)
        $('#dish'+data[i].id).html(data[i].amount+'份');
    });
}