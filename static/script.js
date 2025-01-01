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
                        <img src="${article.urlToImage}" alt="${article.title}" class="w-full h-40 object-cover rounded-md mb-4">
                        <h3 class="text-lg font-semibold mb-2">${article.title}</h3>
                        <p class="text-sm text-gray-600 mb-4">${article.description}</p>
                        <a href="${article.url}" target="_blank" class="text-blue-500 hover:underline">Read more</a>
                        <p class="text-sm text-gray-600 mb-4">${article.publishedAt}</p>
                    `;
                    newsContainer.appendChild(card);
                });
            });
    });
});
