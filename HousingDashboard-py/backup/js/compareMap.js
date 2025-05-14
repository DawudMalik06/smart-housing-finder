const map = L.map('map').setView([53.3811, -1.4701], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; OpenStreetMap contributors'}).addTo(map);
fetch('./sheffield.json')
.then(res => res.json())
.then(data => {
    const style = {
        color: "#3388ff",
        fillColor: "#3388ff",
        weight: 1,
        fillOpacity: 0.2
    };
    const highlightStyle = {
        fillOpacity: 0.6,
        weight: 2,
        color: "#1e90ff"
    };
    function onEachFeature(feature, layer){
        const areaName = feature.properties.WD13NM || "Unnamed Area";
        layer.bindTooltip(areaName, {
            permanent: false,
            direction: "top",
            opacity: 0.9
        });
        layer.on("mouseover", () => {
            layer.setStyle(highlightStyle);
        });
        layer.on("mouseout", () => {
            geojson.resetStyle(layer);
        });
    }
    const geojson = L.geoJSON(data, {style: style, onEachFeature: onEachFeature}).addTo(map);
})
.catch(err => console.error("Error loading GeoJSON:", err));