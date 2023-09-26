// ############ for the Nav bar ########################

let navbar = $(".navbar");

let stats = $(".section-2 .container-fluid")

let sec3Left = $(".section-3 .how-to-work-col")

let sec3Right = $(".section-3 .items-col")

let sec4Left = $(".section-4 .form-col")

let sec4Right = $(".section-4 .contact-us-col")


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

  if ($(window).scrollTop() + window.innerHeight >= $(".section-3").offset().top + 200) {
    sec3Left.removeClass("hidden");
    sec3Left.addClass("left-in")

    sec3Right.removeClass("hidden");
    sec3Right.addClass("right-in")
  }

  if ($(window).scrollTop() + window.innerHeight >= $(".section-4").offset().top + 200) {
    sec4Left.removeClass("hidden");
    sec4Left.addClass("left-in")

    sec4Right.removeClass("hidden");
    sec4Right.addClass("right-in")
  }
});


// ############ for the how to work section ########################

const portfolioItem = document.querySelector('#portfolio');

const portfolioContent = document.querySelector("#content-portfolio")
const contentPortfolioSectionWidth = portfolioContent.offsetWidth; 

const portfolioContentContainer = document.querySelector('#content-portfolio .information-container')
const paddingportfolioContentContainer = parseInt(window.getComputedStyle(portfolioContentContainer).getPropertyValue('padding'));

const cardPortfolio = document.querySelector('.portfolio-block');
const paddingCardPortfolio = parseInt(window.getComputedStyle(cardPortfolio).getPropertyValue('padding'));


const percentageWidthFront = 0.5
const percentageWidthBack = 0.9

const cardFront = document.querySelector('.portfolio-block-front');
const cardBack = document.querySelector('.portfolio-block-back');



const items = document.querySelectorAll('.information-item');


// setup for the front of the card in the beginning

cardPortfolio.style.width = percentageWidthFront*contentPortfolioSectionWidth + 2*paddingCardPortfolio + 'px';
cardFront.style.width = percentageWidthFront*contentPortfolioSectionWidth + 'px';

const cardFrontHeight = cardFront.clientHeight;
cardPortfolio.style.height = cardFrontHeight + 2*paddingCardPortfolio + 'px';




function expand(item) {
  const content = item.querySelector('.information-content');

  if (content.id == "content-portfolio"){
    if (cardPortfolio.classList.contains('flipped')){
      // Get the height of the content in the expanded state
      const cardBackHeight = document.querySelector('.portfolio-block-back').clientHeight;
      contentHeightPortfolio = cardBackHeight + 2*paddingCardPortfolio + 2*paddingportfolioContentContainer + 'px';
      // Set the height of the div to the height of the content
      content.style.height = contentHeightPortfolio;
    }else{
      // Get the height of the content in the expanded state
      contentHeightPortfolio = cardFrontHeight + 2*paddingCardPortfolio + 2*paddingportfolioContentContainer + 'px';
      // Set the height of the div to the height of the content
      content.style.height = contentHeightPortfolio;
    }

  }else{
    // Get the height of the content in the expanded state
    contentHeight = content.scrollHeight + 'px';
    // Set the height of the div to the height of the content
    content.style.height = contentHeight;
  }

  
}

function collapse(item) {
  const content = item.querySelector('.information-content');
  // Reset the height of the div to 0
  content.style.height = '0';
}



items.forEach(item => {
  const buttonContainer = item.querySelector('.information-title')

  buttonContainer.addEventListener('click', () => {
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

const excelSwitchButton = document.querySelectorAll('.excel-button');

excelSwitchButton.forEach(excelSwitchButtons =>{
  excelSwitchButtons.addEventListener('click', () =>{
  cardPortfolio.classList.toggle('flipped')
  if (cardPortfolio.classList.contains('flipped')){
    cardPortfolio.style.width = percentageWidthBack*contentPortfolioSectionWidth + 2*paddingCardPortfolio + 'px';
    cardBack.style.width = percentageWidthBack*contentPortfolioSectionWidth + 'px';

    const cardBackHeight = cardBack.clientHeight;
    cardPortfolio.style.height = cardBackHeight + 2*paddingCardPortfolio + 'px';

    portfolioContent.style.height = cardBackHeight + 2*paddingCardPortfolio + 2*paddingportfolioContentContainer + 'px';

  }else{
    cardPortfolio.style.width = percentageWidthFront*contentPortfolioSectionWidth + 2*paddingCardPortfolio + 'px';
    cardFront.style.width = percentageWidthFront*contentPortfolioSectionWidth + 'px';

    const cardFrontHeight = cardFront.clientHeight;
    cardPortfolio.style.height = cardFrontHeight + 2*paddingCardPortfolio + 'px';

    portfolioContent.style.height = cardFrontHeight + 2*paddingCardPortfolio + 2*paddingportfolioContentContainer + 'px';
  }
})
})

document.addEventListener('DOMContentLoaded', function () {
  const navbarToggler = document.getElementById('navbar-toggler');
  const offcanvas = document.getElementById('offcanvas');
  const closeOffcanvas = document.getElementById('close-offcanvas');

  navbarToggler.addEventListener('click', function () {
      offcanvas.classList.add('show');
  });

  closeOffcanvas.addEventListener('click', function () {
      offcanvas.classList.remove('show');
  });
});