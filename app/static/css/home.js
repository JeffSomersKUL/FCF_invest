// ############ for the Nav bar ########################
let offsetHeightStart = window.innerHeight*0.15

let featureCards = $(".section-1 .container-fluid");

let stats = $(".section-2 .container-fluid");

let sec3Left = $(".section-3 .how-to-work-col");

let sec3Right = $(".section-3 .items-col");

let sec4Left = $(".section-4 .form-col");

let sec4Right = $(".section-4 .contact-us-col");

if ($(window).scrollTop() + window.innerHeight >= $(".section-1").offset().top ) {
  featureCards.removeClass("hidden");
  featureCards.addClass("left-in");
}

if ($(window).scrollTop() + window.innerHeight >= $(".section-3").offset().top + offsetHeightStart) {
  sec3Left.removeClass("hidden");
  sec3Left.addClass("left-in");

  sec3Right.removeClass("hidden");
  sec3Right.addClass("right-in");
}

if ($(window).scrollTop() + window.innerHeight >= $(".section-4").offset().top + offsetHeightStart) {
  sec4Left.removeClass("hidden");
  sec4Left.addClass("left-in");

  sec4Right.removeClass("hidden");
  sec4Right.addClass("right-in");
}

$(window).scroll(function () {
  if ($(window).scrollTop() + window.innerHeight >= $(".section-1").offset().top + offsetHeightStart) {
    featureCards.removeClass("hidden");
    featureCards.addClass("left-in");
  }

  if ($(window).scrollTop() + window.innerHeight >= $(".section-2").offset().top + offsetHeightStart) {
    stats.removeClass("hidden");
    stats.addClass("up-in");
  }

  if ($(window).scrollTop() + window.innerHeight >= $(".section-3").offset().top + offsetHeightStart) {
    sec3Left.removeClass("hidden");
    sec3Left.addClass("left-in");

    sec3Right.removeClass("hidden");
    sec3Right.addClass("right-in");
  }

  if ($(window).scrollTop() + window.innerHeight >= $(".section-4").offset().top + offsetHeightStart) {
    sec4Left.removeClass("hidden");
    sec4Left.addClass("left-in");

    sec4Right.removeClass("hidden");
    sec4Right.addClass("right-in");
  }
});

const items = document.querySelectorAll(".information-item");

function expand(item) {
  const content = item.querySelector(".information-content");
  // Get the height of the content in the expanded state
  contentHeight = content.scrollHeight + "px";
  // Set the height of the div to the height of the content
  content.style.height = contentHeight;
}

function collapse(item) {
  const content = item.querySelector(".information-content");
  // Reset the height of the div to 0
  content.style.height = "0";
}

items.forEach((item) => {
  const buttonContainer = item.querySelector(".information-title");

  buttonContainer.addEventListener("click", () => {
    if (item.classList.contains("active")) {
      item.classList.remove("active");
      collapse(item);
    } else {
      items.forEach((item) => {
        item.classList.remove("active");
        collapse(item);
      });
      item.classList.add("active");
      expand(item);
    }
  });
});

function showOffCanvas() {
  $("#offcanvas").modal("show");
}

function closeOffCanvas() {
  var offcanvas = document.getElementById("offcanvas");
  offcanvas.classList.add("show-div");
  $("#offcanvas").modal("hide");
  setTimeout(function () {
    offcanvas.classList.remove("show-div");
  }, 500);
}