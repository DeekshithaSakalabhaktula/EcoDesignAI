const cards = document.querySelectorAll(".material-card");
const display = document.getElementById("impact-display");

cards.forEach(card => {
    card.addEventListener("click", () => {
        const material = card.dataset.material;

        fetch(`/api/material/${material}`)
            .then(res => res.json())
            .then(data => {
                display.innerHTML = `
                    <h3>${material.toUpperCase()}</h3>
                    <p>Carbon Impact: ${"█".repeat(data.carbon)}</p>
                    <p>Recyclable: ${data.recyclable}</p>
                    <p>Cost: ${data.cost}</p>
                    <p>Durability: ${data.durability}</p>
                    <button onclick="sendToChatbot('${material}')">
                        Design with this material →
                    </button>
                `;
            });
    });
});

function sendToChatbot(material) {
    fetch("/api/send_to_chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: `Design a sustainable product using ${material}`
        })
    });
}