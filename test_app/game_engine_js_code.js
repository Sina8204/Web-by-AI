document.addEventListener('DOMContentLoaded', () => {
    console.log('My Game Engine Documentation - JavaScript Loaded!');

    // Smooth scroll for navigation links
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                // Remove 'active' class from all nav links
                document.querySelectorAll('nav a').forEach(link => {
                    link.classList.remove('active');
                });
                // Add 'active' class to the clicked link
                this.classList.add('active');

                // Scroll smoothly to the target section
                window.scrollTo({
                    top: targetElement.offsetTop - document.querySelector('nav').offsetHeight - 10, // Adjust for fixed nav height
                    behavior: 'smooth'
                });
            }
        });
    });

    // Highlight active nav link on scroll
    const sections = document.querySelectorAll('main section');
    const navLinks = document.querySelectorAll('nav a');
    const navHeight = document.querySelector('nav').offsetHeight;

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - navHeight - 20; // Adjust for nav and some padding
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop && pageYOffset < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) {
                link.classList.add('active');
            }
        });
    });

    // Set initial active link if page is loaded at a specific hash
    if (window.location.hash) {
        const initialActiveLink = document.querySelector(`nav a[href="${window.location.hash}"]`);
        if (initialActiveLink) {
            initialActiveLink.classList.add('active');
        }
    } else {
        // Default to 'home' if no hash is present
        const homeLink = document.querySelector('nav a[href="#home"]');
        if (homeLink) {
            homeLink.classList.add('active');
        }
    }
});