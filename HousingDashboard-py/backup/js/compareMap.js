// Initialize the map
const map = L.map('map').setView([53.3811, -1.4701], 12);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Sample scores per area
const scores = {
  "Broomhill": { affordability: 3, transport: 4, airQuality: 4, greenSpace: 5 },
  "Ecclesall": { affordability: 2, transport: 4, airQuality: 5, greenSpace: 4 },
  "Sharrow":   { affordability: 4, transport: 5, airQuality: 2, greenSpace: 3 }
};

let selectedAreas = [];
const highlightColors = ["#e74c3c", "#f39c12"]; // Red, Orange

// Load GeoJSON and render neighborhood polygons
fetch('data/sheffield-neighborhoods-sample.geojson')
  .then(res => res.json())
  .then(geojsonData => {
    L.geoJSON(geojsonData, {
      style: {
        color: "#2980b9",
        weight: 2,
        fillOpacity: 0.3
      },
      onEachFeature: (feature, layer) => {
        const name = feature.properties.name;
        layer.bindPopup(`<strong>${name}</strong><br>Click to view or compare`);
        layer.on('click', () => handleAreaClick(name));
      }
    }).addTo(map);
  });

// Handle area selection
function handleAreaClick(name) {
  if (!scores[name]) return;

  // Deselect all first
  map.eachLayer(layer => {
    if (layer.setStyle && layer.feature && layer.feature.properties.name) {
      layer.setStyle({ color: "#2980b9" });
    }
  });

  // Add/remove selection
  if (selectedAreas.includes(name)) {
    selectedAreas = selectedAreas.filter(n => n !== name);
  } else if (selectedAreas.length < 2) {
    selectedAreas.push(name);
  } else {
    selectedAreas.shift();
    selectedAreas.push(name);
  }

  // Highlight selected areas
  selectedAreas.forEach((areaName, i) => {
    map.eachLayer(layer => {
      if (layer.setStyle && layer.feature && layer.feature.properties.name === areaName) {
        layer.setStyle({ color: highlightColors[i] });
      }
    });
  });

  // Show either single or comparison
  if (selectedAreas.length === 1) {
    const s = scores[selectedAreas[0]];
    document.getElementById("neighborhood-details").innerHTML = `
      <strong>${selectedAreas[0]}</strong><br>
      Affordability: ${s.affordability}/5<br>
      Transport: ${s.transport}/5<br>
      Air Quality: ${s.airQuality}/5<br>
      Green Space: ${s.greenSpace}/5<br>
      <em>Select one more to compare.</em>
    `;
  }

  if (selectedAreas.length === 2) {
    displayComparison(selectedAreas[0], selectedAreas[1]);
  }
}

// Show comparison table
function displayComparison(area1, area2) {
  const a1 = scores[area1];
  const a2 = scores[area2];

  document.getElementById("neighborhood-details").innerHTML = `
    <table border="1" cellpadding="8">
      <tr><th>Criteria</th><th>${area1}</th><th>${area2}</th></tr>
      <tr><td>Affordability</td><td>${a1.affordability}</td><td>${a2.affordability}</td></tr>
      <tr><td>Transport</td><td>${a1.transport}</td><td>${a2.transport}</td></tr>
      <tr><td>Air Quality</td><td>${a1.airQuality}</td><td>${a2.airQuality}</td></tr>
      <tr><td>Green Space</td><td>${a1.greenSpace}</td><td>${a2.greenSpace}</td></tr>
    </table>
    <button onclick="resetComparison()">Clear</button>
  `;
}

// Reset selections
function resetComparison() {
  selectedAreas = [];

  // Reset styles
  map.eachLayer(layer => {
    if (layer.setStyle && layer.feature && layer.feature.properties.name) {
      layer.setStyle({ color: "#2980b9" });
    }
  });

  document.getElementById("neighborhood-details").innerHTML = "Click a neighborhood to view or compare.";
}
