var dark_mode = false

function checkDarkMode() {
  if (dark_mode) {
    $(".hero").addClass('is-dark-mode')
    $(".button").addClass('is-dark-mode')
    $(".footer").addClass('is-dark-mode')
    $(".navbar").addClass('is-dark-mode')
    $("p").addClass('is-dark-mode')
    $("a").addClass('is-dark-mode')
    $("hr").addClass('is-dark-mode')
  } else {
    $(".hero").removeClass('is-dark-mode')
    $(".button").removeClass('is-dark-mode')
    $(".footer").removeClass('is-dark-mode')
    $(".navbar").removeClass('is-dark-mode')
    $("p").removeClass('is-dark-mode')
    $("a").removeClass('is-dark-mode')
    $("hr").removeClass('is-dark-mode')

  }
}

function switchDarkMode() {
  dark_mode = !dark_mode
  checkDarkMode()
}

$(document).ready(function() {
  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function() {
      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");
      if ($(".navbar-burger").hasClass('is-active')) {
        $(".hero").css('margin-top', 'calc(' + $('.navbar').height() + 'px - 3.25rem)');
      } else {
        $(".hero").css('margin-top', '0');
      }
  });
});