# Project Context: Taskwarrior Web UI with HTMX, Flask, and Tailwind CSS

This project is a web-based user interface for Taskwarrior. It leverages:
* **Backend:** Flask (Python)
* **Taskwarrior Interaction:** `tasklib` (Python library)
* **Frontend Dynamics:** HTMX (minimal JavaScript, server-side rendering)
* **Styling:** Tailwind CSS (utility-first CSS framework)
* **Development Workflow:** Unified `npm run dev` command for live reloading (Python, HTML, CSS) and Tailwind JIT compilation.

## General Instructions for Gemini CLI:

* **Technology Stack Priority:** Solutions *must* leverage Flask, `tasklib`, Jinja2 templates, HTMX, and Tailwind CSS. Avoid suggesting alternative complex JavaScript frameworks or custom CSS unless absolutely necessary and justified.
* **HTMX First for Interactivity:** When suggesting frontend interactivity, always prioritize HTMX attributes (`hx-get`, `hx-post`, `hx-put`, `hx-delete`, `hx-swap`, `hx-target`, `hx-trigger`) to achieve dynamic updates without writing custom JavaScript.
* **Tailwind CSS for Styling:** All styling should be done using Tailwind CSS utility classes. Avoid suggesting custom CSS files or inline styles unless for very specific, isolated cases where Tailwind cannot provide the desired effect (which is rare). When adding or modifying HTML, always consider appropriate Tailwind classes for layout, typography, colors, spacing, etc.
* **CSS View Transitions:** Actively look for opportunities to implement smooth UI transitions using the CSS View Transitions API in conjunction with HTMX's `transition:true` and `view-transition-name` CSS properties. This enhances the user experience significantly.
* **Taskwarrior Best Practices:** Ensure any task manipulation adheres to Taskwarrior's conventions and uses the `tasklib` library correctly and efficiently.
* **Code Quality & Readability:**
    * **Python:** Adhere strictly to PEP 8 for formatting and style. Write clean, well-commented, and modular Flask application code.
    * **HTML/Jinja2:** Keep templates clean, semantic, readable, and well-structured. Break down large templates into smaller, reusable components (e.g., `_task_item.html`, `_task_form.html`).
    * **CSS (Tailwind):** Maintain a clear and consistent application of Tailwind classes.
* **Modularity:** Aim for high modularity across all layers of the application (e.g., separate Flask blueprints if the project grows, reusable Jinja2 macros/includes).
* **Error Handling:** Suggest robust error handling for all operations, including API calls, `tasklib` interactions, and user input validation, providing clear feedback to the user via HTMX swaps.
* **User Experience (UX):** Prioritize an intuitive, responsive, and visually appealing user experience, leveraging the strengths of HTMX and Tailwind CSS. Consider loading states, success/error messages, and clear interaction points.
* **Security:** Advise on basic web security practices, especially regarding form submissions, environment variables, and data handling (e.g., using Flask's `SECRET_KEY`).
* **Dev Workflow Integration:** When suggesting changes that affect the development environment, remember the `npm run dev` command and ensure compatibility or suggest updates to `package.json` scripts if necessary.

## Component-Specific Guidance:

### Backend (Flask & `tasklib`)

* **API Endpoints:** Design RESTful or REST-like endpoints for CRUD operations on tasks. Responses should typically be HTML fragments suitable for HTMX swapping.
* **Data Validation:** Implement server-side validation for all incoming data to ensure data integrity before interacting with `tasklib`.
* **`tasklib` Usage:** All Taskwarrior data access and manipulation must go through the `tasklib` library. Handle `tasklib` exceptions gracefully.

### Frontend (HTMX & Jinja2)

* **HTMX Driven:** All dynamic UI updates (adding, editing, deleting tasks, form submissions) should be driven by HTMX. Avoid `window.location` changes for these operations.
* **Partial Updates:** Focus on swapping only the necessary parts of the DOM. For example, when adding a task, append only the new task item HTML. When editing, swap the task display with an edit form and then back again.
* **Loading States & Feedback:** Utilize HTMX's `htmx-indicator` or events (`htmx:beforeRequest`, `htmx:afterRequest`) to provide visual feedback during asynchronous operations (e.g., spin icon, disabling buttons).

### Styling (Tailwind CSS)

* **Utility-First:** Use Tailwind utility classes directly in the HTML.
* **Responsive Design:** Leverage Tailwind's responsive prefixes (e.g., `md:`, `lg:`) to ensure the UI looks good on various screen sizes.
* **Theming:** If any basic theming is desired (e.g., dark mode toggle), suggest how to integrate it with Tailwind's capabilities.

### View Transitions (CSS)

* **`view-transition-name`:** For elements that should visually transition across page swaps (e.g., a task item when its content changes, or when it moves position), ensure they have a unique `view-transition-name` in the HTML.
* **CSS Animation:** Provide `@keyframes` and `::view-transition-old()`, `::view-transition-new()` pseudo-elements in `static/css/style.css` (or wherever custom CSS might be needed for transitions specifically) to define the animation.
* **`transition:true`:** Remember to add `transition:true` to HTMX `hx-swap` attributes to enable the View Transitions API.

## Example Use Cases for Gemini CLI:

* "Design the HTML structure for a single task item, including Tailwind CSS classes for basic styling (padding, background, border, shadow) and an edit/delete button, suitable for HTMX swapping."
* "Implement the Flask route and corresponding HTMX attributes to allow toggling a task's completion status with a single click, using view transitions to smoothly update the task's appearance."
* "How can I display a simple loading spinner using Tailwind CSS and HTMX's `htmx-indicator` when a task is being added or updated?"
* "Generate the `tailwind.config.js` and `postcss.config.js` files with basic configurations to start using Tailwind in this project."
* "Suggest improvements to the task form using Tailwind for better layout and a more modern look."
* "Walk me through adding a 'filter by status' feature to the task list using HTMX and Flask, ensuring the filter selection persists."
* "Help me debug why my Tailwind CSS changes aren't reflecting in the browser during `npm run dev`."

---
