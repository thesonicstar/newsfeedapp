document.getElementById('add-article-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    fetch('/add_article', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showToast("Article added successfully!", "success");
        } else {
            showToast("Error adding article.", "error");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showToast("An unexpected error occurred.", "error");
    });
});

function showToast(message, type = "info") {
    const toastContainer = document.getElementById("toast-container");

    // Create toast element
    const toast = document.createElement("div");
    toast.classList.add("toast", type, "show");
    toast.innerText = message;

    // Append toast to the container
    toastContainer.appendChild(toast);

    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove("show");
        // Remove toast from DOM after fade-out
        setTimeout(() => toastContainer.removeChild(toast), 500);
    }, 3000);
}