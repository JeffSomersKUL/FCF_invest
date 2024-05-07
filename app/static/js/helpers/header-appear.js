let navbar = $(".navbar");

if ($(window).scrollTop() >= $("header").offset().top + $("header").height()) {
    navbar.addClass("sticky");
} else {
    navbar.removeClass("sticky");
}

$(window).scroll(function () {
    if ($(window).scrollTop() >= $("header").offset().top + $("header").height()) {
        navbar.addClass("sticky");
    } else {
        navbar.removeClass("sticky");
    }
});