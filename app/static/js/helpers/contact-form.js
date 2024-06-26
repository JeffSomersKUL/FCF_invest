// JavaScript to handle form submission
$(document).ready(function () {
  document
    .getElementById("contact-form")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission
      // display waiting circle
      var feedbackDiv = document.getElementById("feedback-form-container");
      feedbackDiv.innerHTML =
        '<div id="waiting-feedback"><div class="spinner-border" role="status"></div></div>';
      feedbackDiv.style.height = feedbackDiv.scrollHeight + "px";
      // disbale button
      var myButton = document.getElementById("form-submit");
      myButton.disabled = true;

      $.ajax({
        type: "POST",
        url: "/submit_form", // Flask route for form submission
        data: $("#contact-form").serialize(), // Serialize form data
        success: function (response) {
          // Handle the response as needed
          console.log(response);
          if (response.response == "success") {
            const successDiv =
              '<div class="alert alert-success" id="success-feedback" role="alert">We successfully received your message!</div>';
            feedbackDiv.innerHTML = successDiv;
            feedbackDiv.style.height = feedbackDiv.scrollHeight + "px";
          } else if (response.response == "failed") {
            const backendFailedDiv =
              '<div class="alert alert-warning" role="alert">Something went wrong on our side when saving your form, please try again later.</div>';
            feedbackDiv.innerHTML = backendFailedDiv;
            feedbackDiv.style.height = feedbackDiv.scrollHeight + "px";
          } else {
            const notFilledDiv =
              '<div class="alert alert-danger" role="alert">Not all fields are filled in.</div>';
            feedbackDiv.innerHTML = notFilledDiv;
            feedbackDiv.style.height = feedbackDiv.scrollHeight + "px";
            myButton.disabled = false;
          }
        },
        error: function (error) {
          // response if something went wrong please retry or contact later
          const warningDiv =
            '<div class="alert alert-warning" role="alert">Something went wrong on our side, please try again later.</div>';
          feedbackDiv.innerHTML = warningDiv;
          feedbackDiv.style.height = feedbackDiv.scrollHeight + "px";
        },
      });
    });
});
