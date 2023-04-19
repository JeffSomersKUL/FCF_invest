/**
 *
 *  sticky navigation
 *
 */

let navbar = $(".navbar");

let stats = $(".section-2 .container-fluid")

let sec3Left = $(".section-3 .how-to-work-col")

let sec3Right = $(".section-3 .items-col")

$(window).scroll(function () {
  // get the complete hight of window
  //let oTop = window.innerHeight - $(".section-2").offset().top;
  if ($(window).scrollTop() >= $("header").offset().top + $("header").height()) {
    navbar.addClass("sticky");
  } else {
    navbar.removeClass("sticky");
  }

  if ($(window).scrollTop() + window.innerHeight >= $(".section-2").offset().top + $(".section-2").height() * (4/5)) {
    stats.removeClass("hidden");
    stats.addClass("up-in")
  }

  if ($(window).scrollTop() + window.innerHeight >= $(".section-3").offset().top + 70) {
    sec3Left.removeClass("hidden");
    sec3Left.addClass("left-in")

    sec3Right.removeClass("hidden");
    sec3Right.addClass("right-in")
  }
});

function expand(item) {
  const content = item.querySelector('.information-content');
  // Get the height of the content in the expanded state
  const contentHeight = content.scrollHeight;
  
  // Set the height of the div to the height of the content
  content.style.height = `${contentHeight}px`;
}

function collapse(item) {
  const content = item.querySelector('.information-content');
  // Reset the height of the div to 0
  content.style.height = '0';
}

const items = document.querySelectorAll('.information-item');

items.forEach(item => {
  item.addEventListener('click', () => {
    if (item.classList.contains('active')) {
      item.classList.remove('active');
      collapse(item)
    } else {
      items.forEach(item => {
        item.classList.remove('active');
        collapse(item)
      });
      item.classList.add('active');
      expand(item)
    }
  });
});