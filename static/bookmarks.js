document.addEventListener('DOMContentLoaded', () => {
    const bookmarksContainer = document.getElementById('bookmarks-container');

    // Fetch bookmarks from the server
    fetch('/get_bookmarks')
        .then(response => response.json())
        .then(data => {
            bookmarksContainer.innerHTML = ''; // Clear existing content

            if (data.length === 0) {
                bookmarksContainer.innerHTML = '<p class="text-gray-600">No bookmarks available.</p>';
                return;
            }

            data.forEach(bookmark => {
                const card = document.createElement('div');
                card.className = 'card p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition';
                card.innerHTML = `
                    <h3 class="text-lg font-semibold mb-2">${bookmark.title}</h3>
                    <p class="text-sm text-gray-600 mb-4">${bookmark.description || 'No description available.'}</p>
                    <a href="${bookmark.url}" target="_blank" class="text-blue-500 hover:underline">Read more</a>
                    <p class="text-sm text-gray-600 mb-4">Source: ${bookmark.source_name || 'Unknown'}</p>
                    <button
                        class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 delete-bookmark"
                        data-id="${bookmark.id}">
                        Delete
                    </button>
                `;
                bookmarksContainer.appendChild(card);
            });
            // Add event listeners for delete buttons
            const deleteButtons = document.querySelectorAll('.delete-bookmark');
            deleteButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const bookmarkId = e.target.getAttribute('data-id');
                    deleteBookmark(bookmarkId);
                });
            });
        })
        .catch(error => {
            console.error("Error fetching bookmarks:", error);
            showToast("Error fetching bookmarks!", "error");
            bookmarksContainer.innerHTML = '<p class="text-red-600">Failed to load bookmarks.</p>';
        });
});

// Function to delete a bookmark
function deleteBookmark(bookmarkId) {
    fetch(`/delete_bookmark/${bookmarkId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showToast("Bookmark deleted successfully!", "success");
            document.querySelector(`[data-id="${bookmarkId}"]`).parentElement.remove(); // Remove the card
        } else {
            showToast("Failed to delete bookmark.", "error");
        }
    })
    .catch(error => {
        console.error("Error deleting bookmark:", error);
        showToast("An error occurred while deleting the bookmark.", "error");
    });
}

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