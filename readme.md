# Kushagra Sharoya | Personal Portfolio

A premium, single-page personal portfolio website designed to showcase technical capabilities, competitive programming milestones, and a clear roadmap toward backend and Artificial Intelligence engineering.

This site uses a custom, bold **editorial design** and **asymmetric layout blocks** (forest green, warm gold, off-white cream) inspired by a high-end personal branding aesthetic.

---

## 📁 Repository Structure

As requested, the core project is built using strictly **two files** to maintain high speed and zero dependencies:

```
portfolio/
├── index.html   # Main structure, styling (inline CSS), and actions (vanilla JS)
└── README.md    # Project documentation and customization guide
```

---

## 🛠️ Tech Stack & Design Attributes

* **HTML5:** Semantic architecture to maximize accessibility (WCAG AA).
* **CSS3:** Custom variables, responsive clamp utility typography, and fluid columns.
* **Vanilla JavaScript (ES6+):** Scroll spying, typing carousel, and IntersectionObserver-based scroll reveals.
* **Fonts:** Expressive display serif (`Fraunces`) and clean geometric sans-serif (`Plus Jakarta Sans`) imported from Google Fonts.
* **Animations:** Eased hover lifts, rotating carousels, outline text elements, and prefers-reduced-motion compatibility.

---

## ⚙️ How to Run Locally

Since the project is built on pure client-side web technologies, you don't need any complex build systems (Webpack, Vite, npm scripts) to preview or edit it:

1. **Direct Preview:** Double-click `index.html` to open it in Chrome, Safari, Firefox, or Edge.
2. **VS Code Live Server (Recommended):** Right-click `index.html` and click **"Open with Live Server"** to run it on a local hot-reloading development port (`http://5500`).
3. **Python Server:** Run the following command in your terminal within the repository root:
   ```bash
   python -m http.server 8000
   ```
   Open `http://localhost:8000` in your browser.

---

## ✍️ Customization Instructions

### 1. Replacing Image Placeholders
No external project or profile images are pre-bundled in the codebase. To personalize:
* **Profile Frame:** Find the `<div class="avatar-placeholder">` in `index.html`. Replace it with an image tag pointing to your photo:
  ```html
  <img src="assets/images/profile.jpg" alt="Kushagra Sharoya" style="width:100%; height:100%; object-fit:cover;">
  ```
* **Project Showcase:** Find the `<div class="project-image-placeholder">` under the **EcoInsight** project card. Replace it with your project screenshot:
  ```html
  <img src="assets/images/ecoinsight-screenshot.jpg" alt="EcoInsight Dashboard" style="width:100%; height:100%; object-fit:cover;">
  ```

### 2. Setting Up the Contact Form
The contact form is pre-configured with a placeholder URL. To receive email messages:
1. Register a free account at [Formspree](https://formspree.io/).
2. Create a new form and copy the endpoint URL (e.g., `https://formspree.io/f/xz3j2k`).
3. Open `index.html` and locate the form tag under the Contact section:
   ```html
   <form class="contact-form" action="https://formspree.io/f/YOUR_FORMSPREE_ID_HERE" method="POST" id="contact-form">
   ```
4. Replace `YOUR_FORMSPREE_ID_HERE` with your actual Formspree ID.

### 3. Integrating Live GitHub Widgets
The GitHub Stats section contains placeholders:
* You can integrate live-updating GitHub stats by embedding iframe endpoints from popular open-source stats generators (like [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats)).
* Example iframe snippet:
  ```html
  <iframe src="https://github-readme-stats.vercel.app/api?username=KushagraSharoya&show_icons=true&theme=default" width="100%" height="180px" frameborder="0"></iframe>
  ```

---

## 📑 Spec Documentation

For reference, the initial plans, components specifications, responsive design, and branding strategy chapters can be found inside the `MD/` directory. Use these files as a guide if you plan to extend the portfolio into v2.0 (adding a blog, certifications, or custom backend services).
