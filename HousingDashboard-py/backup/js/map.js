const map = L.map('map').setView([53.3811, -1.4701], 13);
setTimeout(() => {
    map.invalidateSize();
}, 0);
const linkUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
L.tileLayer(linkUrl, { attribution }).addTo(map);
