document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contactForm");
    const formStatus = document.getElementById("formStatus");

    if (!contactForm || !formStatus) {
        return;
    }

    const submitButton = contactForm.querySelector('button[type="submit"]');

    contactForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        if (!contactForm.reportValidity()) {
            return;
        }

        const formData = new FormData(contactForm);

        const payload = {
            fullName: (formData.get("fullName") || "").trim(),
            email: (formData.get("email") || "").trim(),
            phone: (formData.get("phone") || "").trim(),
            service: formData.get("service") || "",
            subject: (formData.get("subject") || "").trim(),
            budget: formData.get("budget") || "",
            message: (formData.get("message") || "").trim(),
            consent: contactForm.elements.consent ? contactForm.elements.consent.checked : false
        };

        if (submitButton) {
            submitButton.disabled = true;
        }
        formStatus.textContent = "Sending your enquiry...";

        try {
            const endpoint = window.location.port === "5500"
                ? "http://127.0.0.1:5000/api/contact"
                : "/api/contact";

            const response = await fetch(
                endpoint,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                }
            );

            const result = await response.json();

            if (!response.ok || !result.success) {
                throw new Error(
                    result.message || "Unable to submit your enquiry."
                );
            }

            formStatus.textContent = result.message;
            contactForm.reset();

        } catch (error) {
            console.error("Contact form error:", error);

            formStatus.textContent =
                error.message === "Failed to fetch"
                    ? "Unable to connect to the server. Please check your backend."
                    : error.message || "Something went wrong. Please try again.";

        } finally {
            if (submitButton) {
                submitButton.disabled = false;
            }
        }
    });
});
