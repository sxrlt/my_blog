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

$(document).ready(function(){
    $.ajax({
         url: '/orders/lorders/',
         dataType: 'json',
         type: 'post',
         success: function(data){
            if(data.lorder){
                for(var i=0; i<data.lorder.length; i++){
                    var order = ''
                    order += '<li id="' + data.lorder[i].id + '">'
                    order += '<div class="order-title">'
                    order += '<h3>订单编号：<span>' + data.lorder[i].order_id + '</span></h3>'
                    order += '<div class="fr order-operate">'
                    order += '<button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal">接单</button>'
                    order += '<button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal">拒单</button>'
                    order += '</div></div>'
                    order += '<div class="order-content">'
                    order += '<img src="/static/media/'+ data.lorder[i].image +'">'
                    order += '<div class="order-text">'
                    order += '<h3>订单</h3>'
                    order += '<ul>'
                    order += '<li>创建时间：' + data.lorder[i].create_date + '</li>'
                    order += '<li>入住日期：' + data.lorder[i].begin_date + '</li>'
                    order += '<li>离开日期：' + data.lorder[i].end_date + '</li>'
                    order += '<li>合计金额：' + data.lorder[i].amount + '元(共' + data.lorder[i].days + '晚)</li>'
                    order += '<li>订单状态：'
                    order += '<span>'+ data.lorder[i].status +'</span>'
                    order += '<input type="hidden" id="order_id" value="' + data.lorder[i].order_id + '">'
                    order += '</li>'
                    if(data.lorder[i].comment){
                        order += '<li>客户评价：' + data.lorder[i].comment + '</li>'
                    }else{
                        order += '<li>客户评价：</li>'
                    }
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
    $(".order-accept").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
    });
    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-reject").attr("order-id", orderId);
    });
});