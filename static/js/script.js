
document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".site-header");
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  // Mobile navigation
  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("open");

      menuToggle.setAttribute("aria-expanded", String(isOpen));
      menuToggle.setAttribute(
        "aria-label",
        isOpen ? "Close navigation" : "Open navigation"
      );
      menuToggle.textContent = isOpen ? "×" : "☰";
      document.body.classList.toggle("menu-open", isOpen);
    });

    navLinks.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
        menuToggle.textContent = "☰";
        menuToggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("menu-open");
      });
    });

    document.addEventListener("keydown", event => {
      if (event.key === "Escape") {
        navLinks.classList.remove("open");
        menuToggle.textContent = "☰";
        menuToggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("menu-open");
      }
    });
  }

  // Header shadow on scroll
  function updateHeader() {
    if (header) {
      header.classList.toggle("scrolled", window.scrollY > 20);
    }
  }

  window.addEventListener("scroll", updateHeader, { passive: true });
  updateHeader();

  // Scroll reveal animation
  const revealItems = document.querySelectorAll(".reveal");

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    revealItems.forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add("visible"));
  }

  // Highlight current navigation page
  const currentPage = location.pathname.split("/").pop() || "index.html";

  document.querySelectorAll(".nav-links a").forEach(link => {
    const targetPage = new URL(link.href, location.href).pathname
      .split("/")
      .pop();

    if (targetPage === currentPage) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
  });

  // Project category filter
  const filterButtons = document.querySelectorAll(".filter-btn");
  const projectCards = document.querySelectorAll(".project-card");

  filterButtons.forEach(button => {
    button.addEventListener("click", () => {
      const category = button.dataset.filter;

      filterButtons.forEach(item => {
        item.classList.remove("active");
        item.setAttribute("aria-pressed", "false");
      });

      button.classList.add("active");
      button.setAttribute("aria-pressed", "true");

      projectCards.forEach(card => {
        const matches =
          category === "all" ||
          card.dataset.category === category;

        card.classList.toggle("hidden", !matches);
      });
    });
  });

  // Contact form front-end validation
  const contactForm = document.querySelector("#contactForm");
  const formStatus = document.querySelector("#formStatus");

  if (contactForm && formStatus) {
    contactForm.addEventListener("submit", event => {
      event.preventDefault();

      if (!contactForm.checkValidity()) {
        contactForm.reportValidity();
        return;
      }

      formStatus.textContent =
        "Your form is valid. Connect a backend or form service to receive messages.";
      formStatus.setAttribute("role", "status");
      formStatus.style.color = "#333";

      // No message is sent to a server by this demo.
    });
  }


  // Update footer year
  document.querySelectorAll("[data-year]").forEach(element => {
    element.textContent = new Date().getFullYear();
  });
});


document.addEventListener("DOMContentLoaded", function () {
    const revealItems = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            function (entries, instance) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        instance.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.1,
                rootMargin: "0px 0px -30px 0px"
            }
        );

        revealItems.forEach(function (item) {
            observer.observe(item);
        });
    } else {
        revealItems.forEach(function (item) {
            item.classList.add("visible");
        });
    }
});






document.addEventListener("DOMContentLoaded", function () {
    // Reveal elements as they enter the viewport.
    const revealItems = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -25px 0px"
            }
        );

        revealItems.forEach(function (item) {
            revealObserver.observe(item);
        });
    } else {
        revealItems.forEach(function (item) {
            item.classList.add("visible");
        });
    }

    // Automatic footer year.
    document.querySelectorAll("[data-year]").forEach(function (element) {
        element.textContent = new Date().getFullYear();
    });
});










document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".project-filter");
    const projectCards = document.querySelectorAll(".project-card");
    const emptyMessage = document.getElementById("projectsEmpty");

    if (!filterButtons.length || !projectCards.length) {
        return;
    }

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const selectedFilter = button.dataset.filter;
            let visibleCount = 0;

            filterButtons.forEach(function (filterButton) {
                const isActive = filterButton === button;

                filterButton.classList.toggle("active", isActive);
                filterButton.setAttribute(
                    "aria-pressed",
                    String(isActive)
                );
            });

            projectCards.forEach(function (card) {
                const category = card.dataset.category;

                const shouldShow =
                    selectedFilter === "all" ||
                    category === selectedFilter;

                card.hidden = !shouldShow;

                if (shouldShow) {
                    visibleCount++;
                }
            });

            if (emptyMessage) {
                emptyMessage.hidden = visibleCount !== 0;
            }
        });
    });
});






document.addEventListener("DOMContentLoaded", function () {
    // Automatically update the footer year
    const yearElement = document.querySelector("[data-year]");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // Front-end form handling
    const contactForm = document.getElementById("contactForm");
    const formStatus = document.getElementById("formStatus");

    if (contactForm && formStatus) {
        contactForm.addEventListener("submit", function (event) {
            event.preventDefault();

            if (!contactForm.checkValidity()) {
                contactForm.reportValidity();
                return;
            }

            formStatus.textContent =
                "Your form is valid. Connect the form to your backend or email API to send this enquiry.";
        });
    }
});


