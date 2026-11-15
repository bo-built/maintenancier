  document.addEventListener("DOMContentLoaded", function () {
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(link => {
      // Remove any hardcoded active classes first
      link.classList.remove('active');
      link.parentElement.classList.remove('active');

      // Check if the link's href matches the current URL path
      if (link.getAttribute('href') === currentLocation ||
          (currentLocation === '/' && link.getAttribute('href') === 'index.html')) {

        // Adds 'active' to both <a> (Bootstrap 5) and <li> (Bootstrap 4)
        link.classList.add('active');
        link.parentElement.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });
  });