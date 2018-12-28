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

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/house/search/?";
    if($(th).attr("area-id") && $(th).attr("area-name") && $(th).attr("start-date") && $(th).attr("end-date")){
        url += ("aid=" + $(th).attr("area-id"));
        url += "&";
        var areaName = $(th).attr("area-name");
        if (undefined == areaName) areaName="";
        url += ("aname=" + areaName);
        url += "&";
        url += ("sd=" + $(th).attr("start-date"));
        url += "&";
        url += ("ed=" + $(th).attr("end-date"));
        location.href = url;
    }else{
        alert('请选择城区、入住时间、离开时间')
    }
}

$(document).ready(function(){
    $.ajax({
        url: '/house/area/',
        dataType: 'json',
        type: 'get',
        success: function(data){
             for(var i=0; i<data.area.length; i++){
                 $('.area-list').append('<a href="#" area-id="'+ data.area[i].id + '">' + data.area[i].name + '</a>');
             }
             $(".area-list a").click(function(e){
                $("#area-btn").html($(this).html());
                $(".search-btn").attr("area-id", $(this).attr("area-id"));
                $(".search-btn").attr("area-name", $(this).html());
                $("#area-modal").modal("hide");
            });
        }
    })
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });
    $.post('/house/my_house/', function(data){
        $('.btn.top-btn.btn-theme').show()
        $('.user-info.fr').hide()
        if(data.user_id){
           $('.btn.top-btn.btn-theme').hide()
           $('.user-info.fr').show()
           $('.user-name').text(data.name)
        }
        for(var i=0; i<data.house.length; i++){
            var house = '<div class="swiper-slide">'
            house += '<a href="/house/detail/?house_id=' + data.house[i].id + '"><img src="/static/images/' + data.house[i].image + '"></a>'
            house += '<div class="slide-title">' + data.house[i].title + '</div>'
            house += '</div>'
            $('.swiper-wrapper').append(house)
        }
        $(".top-bar>.register-login").show();
            var mySwiper = new Swiper ('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationClickable: true
        });
    })
})