var dark_mode = false

function checkDarkMode() {
  const css_classes = '.hero, .button, .footer, .navbar, .box, p, a, hr, h1, h2, h3, h4, h5, h6'
  if (dark_mode) {
    $(css_classes).addClass('is-dark-mode')
  } else {
    $(css_classes).removeClass('is-dark-mode')

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

  $('#logout_link').click(function(e) {
    e.preventDefault()
    const url = $("#logout_link").attr('url')
    console.log(url)
    $.confirm({
      title: 'Logout?',
      content: 'Are you sure want to logout',
      autoClose: 'logoutUser|10000',
      theme: 'supervan',
      buttons: {
          logoutUser: {
              text: 'Yes',
              action: function() {
                window.location.href = url
              }
          },
          cancel: function () {
              
          }
      }
    });
  })
});
