const map = L.map('map').setView([53.3811, -1.4701], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let geojsonLayer;
let currentCostLimit = 1000;
let currentScoreThreshold = 0.5;
let activeFilter = 'cost';

fetch('./sheffield.json')
    .then(res => res.json())
    .then(data => {
        function style(feature) {
            const cost = parseFloat(feature.properties.Cost);
            const rawScore = parseFloat(feature.properties.LivabilityScore);
            const score = Math.round(rawScore * 1000) / 1000;
            const hasGreen = (feature.properties.GreenSpace || "").toLowerCase() === "yes";

            if (activeFilter === 'cost') {
                return {
                    color: "#3388ff",
                    fillColor: cost <= currentCostLimit ? "#3388ff" : "transparent",
                    weight: 1,
                    fillOpacity: cost <= currentCostLimit ? 0.5 : 0
                };
            } else if (activeFilter === 'score') {
                return {
                    color: "#3388ff",
                    fillColor: score >= currentScoreThreshold ? "#3388ff" : "transparent",
                    weight: 1,
                    fillOpacity: score >= currentScoreThreshold ? 0.5 : 0
                };
            } else if (activeFilter === 'greenspace') {
                return {
                    color: hasGreen ? "#2ecc71" : "transparent",
                    fillColor: hasGreen ? "#2ecc71" : "transparent",
                    weight: 1,
                    fillOpacity: hasGreen ? 0.5 : 0
                };
            }
        }

        function highlightStyle() {
            return {
                fillOpacity: 0.6,
                weight: 2,
                color: "#1e90ff"
            };
        }

        function onEachFeature(feature, layer) {
            const areaName = feature.properties.WD13NM || "Unnamed Area";
            layer.bindTooltip(areaName, {
                permanent: false,
                direction: "top",
                opacity: 0.9
            });

            layer.on("mouseover", () => layer.setStyle(highlightStyle()));
            layer.on("mouseout", () => geojsonLayer.resetStyle(layer));

            layer.on("click", () => {
                const infoBox = document.getElementById("info-box");
                const content = document.getElementById("info-box-content");
                const cost = feature.properties.Cost ? `£${feature.properties.Cost}` : "N/A";
                const score = feature.properties.LivabilityScore ?? "N/A";
                const green = feature.properties.GreenSpace ?? "Unknown";
                content.innerHTML = `
                    <h2>${areaName}</h2>
                    <p><strong>Livability Score:</strong> ${score}</p>
                    <p><strong>Monthly Rent:</strong> ${cost}</p>
                    <p><strong>Green Space:</strong> ${green}</p>
                `;
                infoBox.style.display = "block";
            });
        }

        geojsonLayer = L.geoJSON(data, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);

        document.getElementById('cost-range').addEventListener('input', (e) => {
            currentCostLimit = parseInt(e.target.value);
            geojsonLayer.setStyle(style);
        });

        document.getElementById('score-range').addEventListener('input', (e) => {
            currentScoreThreshold = Math.round(parseFloat(e.target.value) * 1000) / 1000;
            document.getElementById('score-value').textContent = currentScoreThreshold.toFixed(3);
            geojsonLayer.setStyle(style);
        });

        document.getElementById('score-select').addEventListener('change', (e) => {
            const selected = e.target.value;
            if (selected === 'schools') {
                activeFilter = 'score';
                document.getElementById('score-slider-container').style.display = 'block';
            } else if (selected === 'greenspace') {
                activeFilter = 'greenspace';
                document.getElementById('score-slider-container').style.display = 'none';
            } else {
                activeFilter = 'cost';
                document.getElementById('score-slider-container').style.display = 'none';
            }
            geojsonLayer.setStyle(style);
        });
    })
    .catch(err => console.error("Error loading GeoJSON:", err));
