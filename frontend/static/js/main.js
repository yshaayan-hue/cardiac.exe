/**
 * CARDIAC.EXE — CORE FRONTEND INTERACTION ENGINE
 * 3D Holographic Card Tilt, Live Filtering, AJAX Cart & WhatsApp Formatter
 */

document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initMobileMenu();
    init3DCardTilt();
    initCatalogFilter();
    initAjaxCart();
    initQuantitySteppers();
    initAuthForms();
    initWhatsAppLinks();
});

/* ==========================================================================
   THEME TOGGLE SYSTEM (DARK / LIGHT)
   ========================================================================== */
function initTheme() {
    const savedTheme = localStorage.getItem("cardiac_theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);

    const toggleBtns = document.querySelectorAll(".theme-toggle-btn");
    toggleBtns.forEach(btn => {
        btn.textContent = savedTheme === "dark" ? "LIGHT MODE" : "DARK MODE";
        btn.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme");
            const next = current === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", next);
            localStorage.setItem("cardiac_theme", next);
            toggleBtns.forEach(b => b.textContent = next === "dark" ? "LIGHT MODE" : "DARK MODE");
        });
    });
}

/* ==========================================================================
   MOBILE NAVIGATION DRAWER
   ========================================================================== */
function initMobileMenu() {
    const menuBtn = document.querySelector(".mobile-menu-btn");
    const drawer = document.querySelector(".mobile-nav-drawer");

    if (menuBtn && drawer) {
        menuBtn.addEventListener("click", () => {
            drawer.classList.toggle("open");
            menuBtn.textContent = drawer.classList.contains("open") ? "✕" : "☰";
        });
    }
}

/* ==========================================================================
   3D HOLOGRAPHIC CARD TILT & GLARE EFFECT
   ========================================================================== */
function init3DCardTilt() {
    const cards = document.querySelectorAll(".card-3d, .detail-card-3d");

    cards.forEach(card => {
        const glare = card.querySelector(".card-holo-glare");

        card.addEventListener("mousemove", (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;

            const rotateX = (0.5 - y) * 26;
            const rotateY = (x - 0.5) * 26;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;

            if (glare) {
                glare.style.opacity = "0.75";
                glare.style.background = `radial-gradient(
                    circle at ${x * 100}% ${y * 100}%,
                    rgba(255, 255, 255, 0.85) 0%,
                    rgba(0, 240, 255, 0.45) 25%,
                    rgba(255, 42, 95, 0.45) 50%,
                    transparent 75%
                )`;
            }
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)";
            if (glare) {
                glare.style.opacity = "0";
            }
        });
    });
}

/* ==========================================================================
   LIVE SEARCH & FILTERING FOR CARDS
   ========================================================================== */
function initCatalogFilter() {
    const searchInput = document.getElementById("cardSearchInput");
    const filterPills = document.querySelectorAll(".filter-pill");
    const sortSelect = document.getElementById("cardSortSelect");
    const cardGrid = document.getElementById("cardsGrid");

    if (!cardGrid) return;

    let activeFilter = "all";
    let searchTerm = "";

    function filterCards() {
        const cards = Array.from(cardGrid.querySelectorAll(".product-card-item"));
        let visibleCount = 0;

        cards.forEach(card => {
            const title = card.getAttribute("data-title")?.toLowerCase() || "";
            const price = parseFloat(card.getAttribute("data-price") || 0);
            const stock = parseInt(card.getAttribute("data-stock") || 0);

            const matchesSearch = title.includes(searchTerm);
            let matchesFilter = true;

            if (activeFilter === "instock") {
                matchesFilter = stock > 0;
            } else if (activeFilter === "under700") {
                matchesFilter = price < 700;
            } else if (activeFilter === "premium") {
                matchesFilter = price >= 700;
            }

            if (matchesSearch && matchesFilter) {
                card.style.display = "";
                visibleCount++;
            } else {
                card.style.display = "none";
            }
        });

        // Show/hide empty state message
        let emptyEl = document.getElementById("noCardsFound");
        if (emptyEl) {
            emptyEl.style.display = visibleCount === 0 ? "block" : "none";
        }
    }

    function sortCards() {
        if (!sortSelect) return;
        const sortVal = sortSelect.value;
        const cards = Array.from(cardGrid.querySelectorAll(".product-card-item"));

        cards.sort((a, b) => {
            const priceA = parseFloat(a.getAttribute("data-price") || 0);
            const priceB = parseFloat(b.getAttribute("data-price") || 0);
            const titleA = a.getAttribute("data-title") || "";
            const titleB = b.getAttribute("data-title") || "";

            if (sortVal === "price-low") return priceA - priceB;
            if (sortVal === "price-high") return priceB - priceA;
            if (sortVal === "name") return titleA.localeCompare(titleB);
            return 0; // default
        });

        cards.forEach(card => cardGrid.appendChild(card));
    }

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            searchTerm = e.target.value.toLowerCase().trim();
            filterCards();
        });
    }

    filterPills.forEach(pill => {
        pill.addEventListener("click", () => {
            filterPills.forEach(p => p.classList.remove("active"));
            pill.classList.add("active");
            activeFilter = pill.getAttribute("data-filter") || "all";
            filterCards();
        });
    });

    if (sortSelect) {
        sortSelect.addEventListener("change", () => {
            sortCards();
        });
    }
}

/* ==========================================================================
   AJAX CART SUBMISSIONS & TOAST NOTIFICATIONS
   ========================================================================== */
function initAjaxCart() {
    document.addEventListener("submit", async (e) => {
        const form = e.target;
        if (!form.classList.contains("ajax-cart-form")) return;

        e.preventDefault();

        const submitBtn = form.querySelector("button[type='submit']");
        const originalText = submitBtn ? submitBtn.innerHTML : "";
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = "ADDING...";
        }

        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            if (response.ok) {
                const data = await response.json();
                updateCartBadge(data.cart_count);
                showToast(data.message || "Card added to cart!", "success");
            } else {
                showToast("Could not add card to cart.", "error");
            }
        } catch (err) {
            console.error(err);
            form.submit(); // fallback to standard submission
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }
    });
}

function updateCartBadge(count) {
    const badges = document.querySelectorAll(".cart-badge");
    badges.forEach(badge => {
        badge.textContent = count;
        badge.style.transform = "scale(1.3)";
        setTimeout(() => {
            badge.style.transform = "scale(1)";
        }, 200);
    });
}

/* ==========================================================================
   QUANTITY STEPPERS (PRODUCT DETAIL & CART)
   ========================================================================== */
function initQuantitySteppers() {
    // Product detail page quantity picker
    const detailSteppers = document.querySelectorAll(".quantity-stepper");

    detailSteppers.forEach(stepper => {
        const minusBtn = stepper.querySelector(".btn-minus");
        const plusBtn = stepper.querySelector(".btn-plus");
        const input = stepper.querySelector(".stepper-input");

        if (!input) return;

        const max = parseInt(input.getAttribute("max") || 99);
        const min = parseInt(input.getAttribute("min") || 1);

        if (minusBtn) {
            minusBtn.addEventListener("click", () => {
                let current = parseInt(input.value) || 1;
                if (current > min) {
                    input.value = current - 1;
                }
            });
        }

        if (plusBtn) {
            plusBtn.addEventListener("click", () => {
                let current = parseInt(input.value) || 1;
                if (current < max) {
                    input.value = current + 1;
                }
            });
        }
    });
}

/* ==========================================================================
   TOAST NOTIFICATION ENGINE
   ========================================================================== */
function showToast(message, type = "success") {
    let container = document.querySelector(".toast-container");
    if (!container) {
        container = document.createElement("div");
        container.className = "toast-container";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    const icon = type === "success" ? "✓" : "!";
    toast.innerHTML = `<span style="color:var(--accent-pulse);font-weight:bold;">[${icon}]</span> <span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(10px)";
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}
window.showToast = showToast;

/* ==========================================================================
   AUTH FORM HANDLER (LOGIN & REGISTER VIA JWT)
   ========================================================================== */
function initAuthForms() {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const feedbackBox = document.getElementById("authFeedback");

    function displayFeedback(msg, isSuccess = false) {
        if (!feedbackBox) return;
        feedbackBox.textContent = msg;
        feedbackBox.className = `auth-feedback ${isSuccess ? "success" : "error"}`;
    }

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const submitBtn = loginForm.querySelector("button[type='submit']");
            submitBtn.disabled = true;
            submitBtn.textContent = "AUTHENTICATING...";

            const email = loginForm.email.value.trim();
            const password = loginForm.password.value;

            try {
                const res = await fetch("/api/auth/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });

                const data = await res.json();

                if (res.ok) {
                    localStorage.setItem("cardiac_token", data.access_token);
                    localStorage.setItem("cardiac_user", JSON.stringify(data.user));
                    displayFeedback("Login successful! Redirecting...", true);
                    setTimeout(() => {
                        window.location.href = "/";
                    }, 1000);
                } else {
                    displayFeedback(data.error || "Login failed. Check your credentials.");
                    submitBtn.disabled = false;
                    submitBtn.textContent = "LOGIN";
                }
            } catch (err) {
                displayFeedback("Network error. Please try again.");
                submitBtn.disabled = false;
                submitBtn.textContent = "LOGIN";
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const submitBtn = registerForm.querySelector("button[type='submit']");
            submitBtn.disabled = true;
            submitBtn.textContent = "CREATING ACCOUNT...";

            const name = registerForm.name.value.trim();
            const email = registerForm.email.value.trim();
            const password = registerForm.password.value;

            try {
                const res = await fetch("/api/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name, email, password })
                });

                const data = await res.json();

                if (res.ok) {
                    displayFeedback(data.message || "Account created! Check your email to verify.", true);
                    registerForm.reset();
                    submitBtn.disabled = false;
                    submitBtn.textContent = "REGISTER";
                } else {
                    displayFeedback(data.error || "Registration failed.");
                    submitBtn.disabled = false;
                    submitBtn.textContent = "REGISTER";
                }
            } catch (err) {
                displayFeedback("Network error. Please try again.");
                submitBtn.disabled = false;
                submitBtn.textContent = "REGISTER";
            }
        });
    }

    // Check if user is logged in
    const userJson = localStorage.getItem("cardiac_user");
    if (userJson) {
        try {
            const user = JSON.parse(userJson);
            const userBtn = document.querySelector(".auth-nav-btn");
            if (userBtn) {
                userBtn.textContent = user.name ? user.name.split(" ")[0] : "ACCOUNT";
            }
        } catch (e) {}
    }
}

/* ==========================================================================
   WHATSAPP ORDER LINK GENERATOR
   ========================================================================== */
function initWhatsAppLinks() {
    const copyBtns = document.querySelectorAll(".btn-copy-order");
    copyBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const textToCopy = btn.getAttribute("data-copy");
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    showToast("Order details copied to clipboard!", "success");
                });
            }
        });
    });
}