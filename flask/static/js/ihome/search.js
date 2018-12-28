var cur_page = 1; // 当前页
var next_page = 1; // 下一页
var total_page = 1;  // 总页数
var house_data_querying = true;   // 是否正在向后台获取数据

// 解析url中的查询字符串
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

// 更新用户点选的筛选条件
var area_id = 0;
var content = '最新上线';
function updateFilterDateDisplay() {
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").eq(0).children("span").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }

    if(area_id != 0){
        $('.house-list li').remove()
        var area = '?aid='+ area_id +'&sd=' + startDate + '&ed='+ endDate + '&content=' + encodeURI(content);
        get(area);
        return;
    }
    if(area_id != 0 || content != '最新上线'){
        $('.house-list li').remove()
        var area = location.search +'&content=' + encodeURI(content);
        get(area);
    }
}


// 更新房源列表信息
// action表示从后端请求的数据在前端的展示方式
// 默认采用追加方式
// action=renew 代表页面数据清空从新展示
function updateHouseData(action) {
    var areaId = $(".filter-area>li.active").attr("area-id");
    if (undefined == areaId) areaId = "";
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var sortKey = $(".filter-sort>li.active").attr("sort-key");
    var params = {
        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
    };
    //发起ajax请求，获取数据，并显示在模板中
}

function get(area){
     $.get('/house/my_search/' + area, function(data){
        if(data.code == 200){
             for(var i=0; i<data.house.length; i++){
                 var house = '';
                 house += '<li class="house-item">'
                 house += '<a href="/house/detail/?house_id='+ data.house[i].id +'"><img src="/static/media/'+ data.house[i].image +'"></a>'
                 house += '<div class="house-desc">'
                 house += '<div class="landlord-pic"><img src="/static/media/'+ data.avatar[i] +'""></div>'
                 house += '<div class="house-price">￥<span>'+ data.house[i].price +'</span>/晚</div>'
                 house += '<div class="house-intro">'
                 house += '<span class="house-title">'+ data.house[i].title +'</span>'
                 house += '<em>出租'+ data.house[i].room +'间 - 1次入住 - '+ data.house[i].address +'</em>'
                 house += '</div>'
                 house += '</div>'
                 house += '</li>'
                 $('.house-list').append(house)
             }
        }
    })
}

$(document).ready(function(){
    $.get('/house/area/', function(data){
         for(var i=0; i<data.area.length; i++){
             $('.filter-item.filter-area').append('<li area-id="'+ data.area[i].id + '">'+ data.area[i].name +'</li>');
         }
    })
    var area = location.search + '&content=' + encodeURI(content);
    get(area);
    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start-date").val(startDate);
    $("#end-date").val(endDate);
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    if (!areaName) areaName = "位置区域";
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    var $filterItem = $(".filter-item-bar>.filter-item");
    $(".filter-title-bar").on("click", ".filter-title", function(e){
        var index = $(this).index();
        if (!$filterItem.eq(index).hasClass("active")) {
            $(this).children("span").children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
            $(this).siblings(".filter-title").children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).addClass("active").siblings(".filter-item").removeClass("active");
            $(".display-mask").show();
        } else {
            $(this).children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).removeClass('active');
            $(".display-mask").hide();
            updateFilterDateDisplay();
        }
    });
    $(".display-mask").on("click", function(e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();
        cur_page = 1;
        next_page = 1;
        total_page = 1;
        updateHouseData("renew");
    });
    $(".filter-item-bar>.filter-area").on("click", "li", function(e) {
        area_id = $(this).attr('area-id')
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html($(this).html());
        } else {
            $(this).removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html("位置区域");
        }
    });
    $(".filter-item-bar>.filter-sort").on("click", "li", function(e) {
        content = $(this).html()
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(2).children("span").eq(0).html($(this).html());
        }
    })
})