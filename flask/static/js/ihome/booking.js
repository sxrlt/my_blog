function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function order(){
    var house_id = location.search.split('=')[1];
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    if(startDate && endDate){
        var sd = new Date(startDate);
        var ed = new Date(endDate);
        days = (ed - sd)/(1000*3600*24) + 1;
        var price = $(".house-text>p>span").html();
        var amount = days * parseFloat(price);
        $.ajax({
            url: '/orders/booking/',
            dataType: 'json',
            type: 'post',
            data: {
            'days': days,
            'amount': amount,
            'house_id': house_id,
            'begin_date': startDate,
            'end_date': endDate
            },
            success: function(data){
                if(data.code == 200){
                    alert('提交订单成功')
                    location.href = '/orders/my_order/'
                }
                if(data.code == 10000){
                    alert('入住时间错误')
                }
            }
        })
    }else{
        alert('请选择入住时间！')
    }
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var house_id = location.search.split('=')[1];
    $.get('/orders/booking/' + house_id + '/', function(data){
          $('.house-info img').attr('src', '/static/media/' + data.house.image)
          $('.house-text h3').text(data.house.title)
          $('.house-text p span').text(data.house.price)
    })
})
