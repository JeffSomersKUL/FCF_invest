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