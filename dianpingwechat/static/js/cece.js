var roomnostr;
var leng;

function checkForVote() {
    // body...
    //check whehter the vote is all done
    var checkForVote = $('.checkclass');
    var arr = new Array();
    for (var i = checkForVote.length - 1; i >= 0; i--) {
        if (checkForVote[i].checked == true) {
            arr.push(checkForVote[i].id);
            // business_id array
        }
    };
    // console.log(arr);
    $.ajax({
        type: "post",
        url: "/polls/" + roomnostr + "/vote/",
        data: JSON.stringify({
            "id": arr
        }),
        contentType: "application/json",
        dataType: "json",
        success: function(data) {
            window.location.href = "#shopresult";
        }
    });
}

function showList(jsonObj) {
    // body...
    console.log(jsonObj);
    //jsonobj: the json object
    if (jsonObj.status == "OK") {
        var list = jsonObj.businesses;
        leng = list.length;
        //clear the elemnts
        $("#showlist").empty();
        var buf = '<input type="checkbox" class="checkclass" name="' + 2552704 + '" id="' + 2552704 + '">';
            buf += '<label for="' + 2552704 + '">'
            buf += '<div class="ui-grid-a"><div class="ui-block-a"><div>' + '<img align="middle" height="50px" width="50px" src="' + "http://i1.dpfile.com/2008-08-25/852885_m.jpg" + '" />' +
                '</div></div><div class="ui-block-b"><div>' + '<div>' + '一茶一坐(龙之梦店)'.substring(0, 10) + '</div>' + '<img src="' + "http://i2.dpfile.com/s/i/app/api/16_0star.png" + '" />' + '</div></div></div><!-- /grid-a -->';
            //buf += '<img height="30%" width="30%" src="' + list[i].s_photo_url + '" />';
            // buf += '<div>' + list[i].name + '</div>';
            // buf += '<img src="' + list[i].rating_s_img_url + '" />';
            buf += '</label>';
            $("#showlist").append(buf).trigger("create");
        for (var i = list.length - 1; i >= 0; i--) {
            var buf = '<input type="checkbox" class="checkclass" name="' + list[i].business_id + '" id="' + list[i].business_id + '">';
            buf += '<label for="' + list[i].business_id + '">'
            buf += '<div class="ui-grid-a"><div class="ui-block-a"><div>' + '<img align="middle" height="50px" width="50px" src="' + list[i].s_photo_url + '" />' +
                '</div></div><div class="ui-block-b"><div>' + '<div>' + list[i].name.substring(0, 10) + '</div>' + '<img src="' + list[i].rating_s_img_url + '" />' + '</div></div></div><!-- /grid-a -->';
            //buf += '<img height="30%" width="30%" src="' + list[i].s_photo_url + '" />';
            // buf += '<div>' + list[i].name + '</div>';
            // buf += '<img src="' + list[i].rating_s_img_url + '" />';
            buf += '</label>';
            $("#showlist").append(buf).trigger("create");
        };
    } else {
        alert("status: wrong0");
    }
}

$(document).on("pageshow", "#idresult", function() {
    console.log("idre");
    str = location.href;
    roomnostr = str.split("?")[1];
    $('#roomstr').html(roomnostr);
});

$(document).on("pageshow", "#votepage", function() {
    str = location.href;
    if (str.split("?")[1] != undefined)
    {
        roomnostr = str.split("?")[1];
    }
    $.get("/polls/" + roomnostr, function(data) {
        showList(data);
    });
});
//get the result of votions
$(document).on("pageshow", "#shopresult", function() {
    $.ajax({
        type: "post",
        url: "/polls/" + roomnostr + "/result/",
        dataType: "json",
        success: function(data) {
            var buf = data;
            var str = "<div>" + data[0].name + "</div>";
            bId = data[0].business_id;
            console.log(bId);
            $('#voteresult').empty();
            $('#voteresult').append(str);
        }
    });
});

function beginvote() {
    // body...
    window.location.href = "#votepage";
    // console.log($('#slider-1')[0].value);
    // var t;
    // if ($('#radio-choice-0a').checked == true)
    // {
    //     console.log('AA');
    //     t = 0;
    // }
    // else
    // {
    //     t = 1;
    // }
    // $.ajax({
    //     type: "post",
    //     url: "/polls/" + roomnostr,
    //     data:
    //     {
    //         "poll_type": t,
    //         "cost": $('#slider-1')[0].value,
    //         "count": $('#slider-2')[0].value
    //     },
    //     contentType: "application/json",
    //     dataType: "json",
    //     success: function(data) {
    //         window.location.href = "#votepage";
    //     }
    // });
}

function export1 () {
    // body...
    window.location.href = "#end";
    $.get("/polls/checkorder/" + roomnostr, function(data){
        var pricesum = 0;
        
        for(var i = data.length-1;i>=0;i--)
        {
            var buf = 
            '<div class="ui-grid-c">'
            +'<div class="ui-block-a"><div class="ui-bar ui-bar-a" style="height:60px">'+data[i].dish_name+'</div></div>'
            +'<div class="ui-block-b"><div class="ui-bar ui-bar-a" style="height:60px">'+data[i].category+'</div></div>'
            +'<div class="ui-block-c"><div class="ui-bar ui-bar-a" style="height:60px">￥'+data[i].price+'.00</div></div>'
            +'<div class="ui-block-d"><div class="ui-bar ui-bar-a" style="height:60px" id="'+data[i].id+'">' + data[i].amount + '份</div></div>'
            +'</div>';
            pricesum+=data[i].price*data[i].amount;
            $('#endlist').append(buf);
        }
        buf = 
            '<div class="ui-grid-c">'
            +'<div class="ui-block-a"><div class="ui-bar ui-bar-a" style="height:60px">菜种：</div></div>'
            +'<div class="ui-block-b"><div class="ui-bar ui-bar-a" style="height:60px">'+data.length+'</div></div>'
            +'<div class="ui-block-c"><div class="ui-bar ui-bar-a" style="height:60px">总价：</div></div>'
            +'<div class="ui-block-d"><div class="ui-bar ui-bar-a" style="height:60px">￥' + pricesum + '.00</div></div>'
            +'</div>';
            $('#endlist').append(buf);
    });
}