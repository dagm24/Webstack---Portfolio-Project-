const sidebarLinks = document.querySelectorAll('.sidebar a');
    const sections = document.querySelectorAll('.section');

    sidebarLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetSection = link.getAttribute('data-section');

        sections.forEach(section => section.classList.remove('active'));

        document.getElementById(targetSection).classList.add('active');
      });
    });