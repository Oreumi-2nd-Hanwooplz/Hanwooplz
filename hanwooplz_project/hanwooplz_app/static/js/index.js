// Prallax script
$(window).scroll(function () {
    var scrollTop = $(this).scrollTop();
    $('.parallax-bg').css('top', -(scrollTop / 3) + 'px');
});
// Prallax script END
var scroll = new SmoothScroll('a[href*="#"]');