/**
 *
 *  sticky navigation
 *
 */

let navbar = $(".navbar");

$(window).scroll(function () {
  // get the complete hight of window
  //let oTop = window.innerHeight - $(".section-2").offset().top;
  if ($(window).scrollTop() >= $(".section-1").offset().top) {
    navbar.addClass("sticky");
  } else {
    navbar.removeClass("sticky");
  }
});