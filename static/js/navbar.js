$(document).ready(function() {
    var windowHeight = $(window).height();
    $('.container').height(windowHeight);
    $('.container').css('overflow', 'auto');

    $('.main_menu_items li').addClass('nav-item');
    $('.main_menu_items a').addClass('nav-link');
});