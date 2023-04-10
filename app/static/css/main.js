/**
 *
 *  sticky navigation
 *
 */

let navbar = $(".navbar");

let stats = $(".section-2 .container-fluid")

$(window).scroll(function () {
  // get the complete hight of window
  //let oTop = window.innerHeight - $(".section-2").offset().top;
  if ($(window).scrollTop() >= $("header").offset().top + $("header").height()) {
    navbar.addClass("sticky");
  } else {
    navbar.removeClass("sticky");
  }

  if ($(window).scrollTop() + window.innerHeight >= $(".section-2").offset().top) {
    console.log("yes")
    stats.removeClass("hidden");
    stats.addClass("up-in")
  }
});