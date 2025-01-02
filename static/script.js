document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const categoryDropdown = document.getElementById('category');
    const fetchNewsButton = document.getElementById('fetch-news');
    const newsContainer = document.getElementById('news-container');


    // Theme toggle
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark');
        themeToggle.textContent = document.body.classList.contains('dark') ? 'Light Mode' : 'Dark Mode';
    });

    // Fetch news
    fetchNewsButton.addEventListener('click', () => {
        const category = categoryDropdown.value;
        fetch(`/get_news?category=${category}`)
            .then(response => response.json())
            .then(data => {
                newsContainer.innerHTML = ''; // Clear old articles
                data.articles.forEach(article => {
                    const card = document.createElement('div');
                    card.className = 'card p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition';
                    card.innerHTML = `
                        <img src="${article.urlToImage || 'static/images/default.jpg'}" alt="${article.title}" class="w-full h-40 object-cover rounded-md mb-4">
                        <h3 class="text-lg font-semibold mb-2">${article.title}</h3>
                        <p class="text-sm text-gray-600 mb-4">${article.description || 'No description available.'}</p>
                        <a href="${article.url}" target="_blank" class="text-blue-500 hover:underline">Read more</a>
                        <p class="text-sm text-gray-600 mb-4">Published: ${new Date(article.publishedAt).toLocaleDateString()}</p>
                        <button
                            class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                            onclick="bookmarkArticle('${article.url}', '${article.title}', '${article.description || 'Unknown'}', '${article.source.name || 'Unknown'}')">
                            Bookmark
                        </button>
                    `;
                    newsContainer.appendChild(card);
                });
            })
            .catch(error => console.error("Error fetching news:", error));
    });
});

// Function to handle bookmarking
function bookmarkArticle(url, title, description, sourceName) {
    fetch('/bookmark', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url: url,
            title: title,
            description: description,
            source_name: sourceName,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("Article bookmarked successfully!");
        } else {
            alert("Failed to bookmark the article.");
        }
    })
    .catch(error => {
        console.error("Error bookmarking article:", error);
        alert("An error occurred while bookmarking.");
    });
}

