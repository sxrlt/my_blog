//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var order_id = 0;

function comment(id){
    order_id = id
}

function order_comment(){
    id = order_id
    var content = $('#comment').val()
    console.log(content)
    console.log(id)
    $.ajax({
        url: '/orders/comment/',
        dataType: 'json',
        type: 'post',
        data: {'comments': content, 'order_id': id},
        success: function(data){
            if(data.code == 200){
                location.reload()
            }
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url: '/orders/my_order/',
        dataType: 'json',
        type: 'POST',
        success: function(data){
            if(data.code == 200){
               for(var i=0; i<data.order.length; i++){
                    var order = ''
                    order += '<li id="">'
                    order += '<div class="order-title">'
                    order += '<h3>订单编号：<span>' + data.ord_id[i] + '</span></h3>'
                    order += '<div class="fr order-operate">'
                    order += '<button type="button" onclick="comment('+ data.order[i].order_id +');" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">发表评价</button>'
                    order += '</div></div>'
                    order += '<div class="order-content">'
                    order += '<img src="/static/media/'+ data.order[i].image +'">'
                    order += '<div class="order-text">'
                    order += '<h3>订单</h3>'
                    order += '<ul>'
                    order += '<li>创建时间：' + data.order[i].create_date + '</li>'
                    order += '<li>入住日期：' + data.order[i].begin_date + '</li>'
                    order += '<li>离开日期：' + data.order[i].end_date + '</li>'
                    order += '<li>合计金额：' + data.order[i].amount + '元(共' + data.order[i].days + '晚)</li>'
                    order += '<li>订单状态：'
                    if(data.order[i].status == "WAIT_ACCEPT"){
                         order += '<span>待接单</span>'
                    }
                    if(data.order[i].status == "REJECTED"){
                         order += '<span>已拒单</span>'
                    }
                    if(data.order[i].status == "WAIT_PAYMENT"){
                         order += '<span>待支付</span>'
                    }
                    if(data.order[i].status == "CANCELED"){
                         order += '<span>待支付</span>'
                    }
                    order += '</li>'
                    if(data.order[i].comment){
                        order += '<li class="order_'+ data.order[i].order_id +'">我的评价：' + data.order[i].comment + '</li>'
                    }else{
                        order += '<li class="order_'+ data.order[i].order_id +'">我的评价：</li>'
                    }
                    order += '<li>拒单原因：</li>'
                    order += '</ul>'
                    order += '</div></div>'
                    order += '</li>'
                    $('.orders-list').append(order)
               }
            }
        }
    })
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-comment").on("click", function(){
        alert('123')
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });
});