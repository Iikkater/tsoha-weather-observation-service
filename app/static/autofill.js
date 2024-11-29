// static/autofill.js
function fetchUsers(query) {
    fetch(`/search_users?q=${query}`)
        .then(response => response.json())
        .then(data => {
            const suggestions = document.getElementById("suggestions");
            suggestions.innerHTML = "";
            data.forEach(user => {
                const div = document.createElement("div");
                div.classList.add("suggestion-item");
                div.textContent = user.username;
                div.onclick = () => {
                    document.getElementById("username").value = user.username;
                    suggestions.innerHTML = "";
                };
                suggestions.appendChild(div);
            });
        });
}

function fetchObservations(query) {
    fetch(`/search_observations?q=${query}`)
        .then(response => response.json())
        .then(data => {
            const suggestions = document.getElementById("observation-suggestions");
            suggestions.innerHTML = "";
            data.forEach(observation => {
                const div = document.createElement("div");
                div.classList.add("suggestion-item");
                div.textContent = observation.id;
                div.onclick = () => {
                    document.getElementById("observation_id").value = observation.id;
                    suggestions.innerHTML = "";
                };
                suggestions.appendChild(div);
            });
        });
}

document.addEventListener("click", function(event) {
    const suggestions = document.getElementById("suggestions");
    if (!suggestions.contains(event.target) && event.target.id !== "username") {
        suggestions.innerHTML = "";
    }
    const observationSuggestions = document.getElementById("observation-suggestions");
    if (!observationSuggestions.contains(event.target) && event.target.id !== "observation_id") {
        observationSuggestions.innerHTML = "";
    }
});