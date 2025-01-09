document.addEventListener("DOMContentLoaded", () => {
    const newsContainer = document.getElementById("news-container");

    fetch("/google_news_data")  // Fetches news from the API proxy route
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "ok") {
                data.articles.forEach((article) => {
                    const card = document.createElement("div");
                    card.className = "card p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition";
                    card.innerHTML = `
                        <img src="${article.urlToImage || 'static/images/default.jpg'}" alt="${article.title}" class="w-full h-40 object-cover rounded-md mb-4">
                        <h3 class="text-lg font-semibold mb-2">${article.title}</h3>
                        <p class="text-sm text-gray-600 mb-4">${article.description || "No description available."}</p>
                        <a href="${article.url}" target="_blank" class="text-blue-500 hover:underline">Read more</a>
                    `;
                    newsContainer.appendChild(card);
                });
                showToast("Fetched Google News!", "success");
            } else {
                newsContainer.innerHTML = "<p class='text-red-500'>Failed to load news. Please try again later.</p>";
            }
        })
        .catch((error) => {
            console.error("Error fetching Google News:", error);
            showToast("Error fetching Google News!", "error");
            //newsContainer.innerHTML = "<p class='text-red-500'>An error occurred while loading news.</p>";
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