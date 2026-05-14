const map = L.map('map').setView([53.3811, -1.4701], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let geojsonLayer;

let currentCostLimit = 0; 
let currentScoreThreshold = 0.1;
let requireGreen = false;

function getColor(score) {
    return score > 0.8 ? '#10b981' :
           score > 0.5 ? '#3b82f6' :
           score > 0.3 ? '#f59e0b' :
                         '#ef4444';
}

fetch('../dashboard/sheffield.json') 
    .then(res => res.json())
    .then(data => {

        const costs = data.features
            .map(f => parseFloat(f.properties.Cost || 0))
            .filter(c => c > 0); //to not crash

        const minCost = Math.min(...costs);
        const maxCost = Math.max(...costs);

        currentCostLimit = maxCost;

        const costRange = document.getElementById('cost-range');
        costRange.min = minCost;
        costRange.max = maxCost;
        costRange.value = maxCost;
        
        //update on load
        document.getElementById('cost-value').textContent = `£${maxCost}`;
        document.getElementById('cost-min-label').textContent = `£${minCost} (Min)`;
        document.getElementById('cost-max-label').textContent = `£${maxCost} (Max)`;

        function style(feature){
            const cost = parseFloat(feature.properties.Cost || 0);
            const score = parseFloat(feature.properties.LivabilityScore || 0);
            const hasGreen = (feature.properties.GreenSpace || "").toLowerCase() === "yes";

            const passesCost = cost <= currentCostLimit;
            const passesScore = score >= currentScoreThreshold;
            const passesGreen = !requireGreen || hasGreen;

            const isVisible = passesCost && passesScore && passesGreen;
            
            return{
                color: isVisible ? "#ffffff" : "transparent",
                weight: isVisible ? 1.5 : 0,
                fillColor: isVisible ? getColor(score) : "transparent",
                fillOpacity: isVisible ? 0.65 : 0
            };
        }

        //polygon border on click
        function highlightStyle(feature){
            const score = parseFloat(feature.properties.LivabilityScore || 0);
            return{
                fillOpacity: 1,
                weight: 2,
                color: "#000000", 
                fillColor: getColor(score)
            };
        }

        function onEachFeature(feature, layer){
            const areaName = feature.properties.WD13NM || "Unnamed Ward";
            
            //hover tip
            layer.bindTooltip(areaName, {
                permanent: false,
                direction: "top",
                className: "bg-slate-900 border-slate-700 text-white font-bold px-3 py-1 rounded-lg text-xs"
            });

            layer.on("mouseover", () => layer.setStyle(highlightStyle(feature)));
            layer.on("mouseout", () => geojsonLayer.resetStyle(layer));

            layer.on("click", () => {
                const infoBox = document.getElementById("info-box");
                const content = document.getElementById("info-box-content");
                const cost = feature.properties.Cost ? `£${feature.properties.Cost}` : "N/A";
                const score = feature.properties.LivabilityScore ? parseFloat(feature.properties.LivabilityScore).toFixed(3) : "N/A";
                const green = feature.properties.GreenSpace || "No";
                
                content.innerHTML = `
                    <div class="border-b border-slate-200 pb-2">
                        <h3 class="text-lg font-bold text-white">${areaName}</h3>
                        <span class="text-[10px] uppercase font-bold px-2 py-0.5 rounded ${green === 'Yes' ? 'bg-green-500/20 text-green-400' : 'bg-slate-700 text-slate-400'}">
                            ${green === 'Yes' ? 'Green Space' : 'Urban Sector'}
                        </span>
                    </div>
                    <div class="space-y-1.5 pt-1 text-sm font-medium">
                        <div class="flex justify-between"><span class="text-slate-400">Average Monthly Rent:</span> <span class="font-mono text-green-400">${cost}</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">Livability Index:</span> <span class="font-mono text-cyan-400">${score}</span></div>
                    </div>
                `;
                infoBox.style.display = "block";
            });
        }

        geojsonLayer = L.geoJSON(data, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);

        //highlight if within
        costRange.addEventListener('input', (e) => {
            currentCostLimit = parseInt(e.target.value);
            document.getElementById('cost-value').textContent = `£${currentCostLimit}`;
            geojsonLayer.setStyle(style);
        });

        const scoreRange = document.getElementById('score-range');
        const scoreValue = document.getElementById('score-value');
        scoreRange.addEventListener('input', (e) => {
            currentScoreThreshold = parseFloat(e.target.value);
            scoreValue.textContent = currentScoreThreshold.toFixed(2);
            geojsonLayer.setStyle(style);
        });

        const greenToggle = document.getElementById('green-toggle');
        greenToggle.addEventListener('change', (e) => {
            requireGreen = e.target.checked;
            geojsonLayer.setStyle(style);
        });

        document.getElementById("close-info").addEventListener("click", () => {
            document.getElementById("info-box").style.display = "none";
        });
    })
    .catch(err => console.error("Error loading Map Layers:", err));