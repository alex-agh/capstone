$(document).ready(function() {
    var windowHeight = $(window).height();
    $('.container').height(windowHeight);
    $('.container').css('overflow', 'auto');

    $('#auth_form label').remove();
    $('#auth_form input[type=checkbox]').remove();
    $('#auth_form button').addClass('btn btn-primary w-25 submit');
    $('#auth_form input').addClass('form-control');
    
    $('h1').addClass('text-center fw-bold');
    $('p').addClass('text-center fw-light');

    $('#auth_form input[name=email]').attr('placeholder', 'Email');
    $('#auth_form input[name=Password1]').attr('placeholder', 'Password');
    $('#auth_form input[name=Password2]').attr('placeholder', 'Password (again)');

    var divHeight = $('.hero').outerHeight();
    var windowHeight = $(window).height();
    var topMargin = (windowHeight - divHeight) / 3.5;
    $('.hero').css('margin-top', topMargin);

    $('.main_menu_items li').addClass('nav-item');
    $('.main_menu_items a').addClass('nav-link');
});

