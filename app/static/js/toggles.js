    // toggles
    for (let element of document.getElementsByClassName("toggle")) {
        element.addEventListener("click", (event) => {
            let clickedElement = event.currentTarget;
            let targetContainer = document.getElementById(clickedElement.dataset.target);

            // Hide all containers
            for (let container of document.getElementsByClassName("toggle-container")) {
                container.classList.remove("shown");
                container.classList.add("hidden");
            }

            // Mark all 'buttons' as inactive
            for (let element of document.getElementsByClassName("toggle")) {
                element.classList.remove("is-active");
            }

            // Reveal correct container
            targetContainer.classList.remove("hidden");
            targetContainer.classList.add("shown");

            // Update button
            clickedElement.classList.add("is-active");
        });
    }