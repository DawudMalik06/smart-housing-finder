let data = [];
let selectedNeighborhoods = [];

function getScoreColor(score){
    return score > 0.8 ? '#10b981' :
            score > 0.5 ? '#3b82f6' :
            score > 0.3 ? '#f59e0b' :
                            '#ef4444';
}

function getRating(score){
    return score > 0.8 ? 'Optimal Range' :
            score > 0.5 ? 'Balanced' :
            score > 0.3 ? 'Moderate' :
                            'Deprivation';
}

//fetch
d3.csv("../final_output/LivabilityScores_with_Greenspace.csv").then(loadedRows => {
    data = loadedRows.map(d => ({
        neighborhood: (d.Neighborhood || "Undefined Profile").replace(/\s+Ward$/i, ""), //removing ward append
        score: parseFloat(d.LivabilityScore || 0),
        cost: parseInt(d.Cost || 0),
        greenSpace: d.GreenSpace || "No"
    })).filter(d => d.neighborhood !== "Undefined Profile");

    updateVisualisation();
    updateComparisonView();
}).catch(err => {
    console.error("Pipeline Failure:", err);
    document.getElementById("chart-container").innerHTML = `
        <div class="text-xs text-red-400 p-4 bg-red-950/20 rounded-xl border border-red-900/50">
            Failed to initialise dataset. Verify target 'LivabilityScores_with_Greenspace.csv'.
        </div>`;
});

function createChart(){
    const container = d3.select("#chart");
    container.html("");
    d3.select(".chart-tooltip").remove();

    const margin = {top: 20, right: 20, bottom: 130, left: 65};
    const width = Math.max(data.length * 35, 600) - margin.left - margin.right;
    const height = 450 - margin.top - margin.bottom;
    
    const svg = container.append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
        .domain(data.map(d => d.neighborhood))
        .range([0, width])
        .padding(0.25);

    const y = d3.scaleLinear()
        .domain([0, 1.0])
        .range([height, 0]);

    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "rotate(-40)")
        .style("text-anchor", "end")
        .style("font-size", "9px")
        .style("fill", "#94a3b8")
        .style("font-family", "monospace");

    svg.append("g")
        .call(d3.axisLeft(y).ticks(5).tickFormat(d => d.toFixed(1)))
        .selectAll("text")
        .style("font-size", "10px")
        .style("fill", "#94a3b8");

    const tooltip = d3.select("body").append("div")
        .attr("class", "chart-tooltip absolute z-50 bg-slate-900 text-white border border-slate-700 p-3 rounded-xl text-xs space-y-1 pointer-events-none transition-opacity duration-200")
        .style("opacity", 0);

    svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar cursor-pointer transition-opacity duration-200 hover:opacity-80")
        .attr("x", d => x(d.neighborhood))
        .attr("width", x.bandwidth())
        .attr("y", d => y(d.score))
        .attr("height", d => height - y(d.score))
        .attr("fill", d => getScoreColor(d.score))
        .attr("rx", 4)
        .on("mouseover", function(event, d) {
            tooltip.style("opacity", 1)
                .html(`
                    <div class="font-bold text-white border-b border-slate-800 pb-1 mb-1">${d.neighborhood}</div>
                    <div class="flex justify-between gap-4"><span class="text-slate-400">Livability Index:</span> <span class="font-mono text-cyan-400">${d.score.toFixed(3)}</span></div>
                    <div class="flex justify-between gap-4"><span class="text-slate-400">Average Monthly Rent:</span> <span class="font-mono text-green-400">£${d.cost}</span></div>
                    <div class="flex justify-between gap-4"><span class="text-slate-400">Green Space:</span> <span class="font-mono text-green-400">${d.greenSpace}</span></div>
                    <div class="text-[10px] text-slate-500 pt-1">${getRating(d.score)}</div>
                `)
                .style("left", (event.pageX + 12) + "px")
                .style("top", (event.pageY - 40) + "px");
        })
        .on("mouseout", () => tooltip.style("opacity", 0))
        .on("click", (event, d) => toggleNeighborhoodSelection(d.neighborhood));
}

function createTable(){
    const tbody = document.getElementById("table-body");
    tbody.innerHTML = "";
    data.forEach(d => {
        const isSelected = selectedNeighborhoods.includes(d.neighborhood);
        const row = document.createElement("tr");
        row.className = `border-b border-slate-800/40 hover:bg-slate-700/20 transition ${isSelected ? 'bg-slate-800/60' : ''}`;

        row.innerHTML = `
            <td class="py-3 px-4 font-bold text-slate-100">${d.neighborhood}</td>
            <td class="py-3 px-4 font-mono text-cyan-400">${d.score.toFixed(3)}</td>
            <td class="py-3 px-4 font-mono text-green-400">£${d.cost}</td>
            <td class="py-3 px-4">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold ${d.greenSpace === 'Yes' ? 'bg-green-500/20 text-green-400' : 'bg-slate-800 text-slate-500'}">
                    ${d.greenSpace === 'Yes' ? 'Green Space' : 'Urban'}
                </span>
            </td>
            <td class="py-3 px-4 text-right">
                <button onclick="toggleNeighborhoodSelection('${d.neighborhood}')" 
                        class="px-3 py-1 rounded-lg text-xs font-bold transition ${isSelected ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30' : 'bg-slate-800 text-slate-400 hover:text-white'}">
                    ${isSelected ? 'Deselect' : 'Compare'}
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

//COMPARISONN VIEW
function toggleNeighborhoodSelection(name){
    const index = selectedNeighborhoods.indexOf(name);
    if (index === -1){
        if (selectedNeighborhoods.length < 2){
            selectedNeighborhoods.push(name);
        } else{
            alert("Selection buffer overflow. Deselect an active ward to push alternative targets.");
            return;
        }
    } else{
        selectedNeighborhoods.splice(index, 1);
    }
    updateVisualisation();
    updateComparisonView();
}

function updateComparisonView(){
    const container = document.getElementById("comparison-container");
    container.innerHTML = "";

    if (selectedNeighborhoods.length === 0){
        container.innerHTML = `
            <div class="text-xs text-slate-500 text-center py-8 border border-dashed border-slate-700/80 rounded-xl">
                Selection Empty.<br>Click graph bars or active table properties to cross-examine output metrics.
            </div>`;
        return;
    }

    selectedNeighborhoods.forEach(name => {
        const targetData = data.find(x => x.neighborhood === name);
        if (!targetData) return;

        const card = document.createElement("div");
        card.className = "bg-slate-900/80 border border-slate-700/80 p-4 rounded-2xl relative space-y-3";
        card.innerHTML = `
            <button onclick="toggleNeighborhoodSelection('${name}')" class="absolute top-3 right-3 text-slate-500 hover:text-white text-sm font-bold">&times;</button>
            <div class="border-b border-slate-800 pb-2">
                <h4 class="font-bold text-white text-sm">${targetData.neighborhood}</h4>
                <span class="text-[10px] text-slate-500 font-mono">${getRating(targetData.score)}</span>
            </div>
            <div class="space-y-1.5 text-xs">
                <div class="flex justify-between"><span class="text-slate-400">Livability Score:</span> <span class="font-mono text-cyan-400 font-bold">${targetData.score.toFixed(3)}</span></div>
                <div class="flex justify-between"><span class="text-slate-400">Average Monthly Rent:</span> <span class="font-mono text-green-400 font-bold">£${targetData.cost}</span></div>
                <div class="flex justify-between"><span class="text-slate-400">Green Space:</span> <span class="font-bold ${targetData.greenSpace === 'Yes' ? 'text-green-400' : 'text-slate-500'}">${targetData.greenSpace}</span></div>
            </div>
        `;
        container.appendChild(card);
    });
}

function updateVisualisation(){
    createChart();
    createTable();
}

//analysis mode
const sortName = document.getElementById("sortName");
const sortScore = document.getElementById("sortScore");

function setActive(activeBtn, inactiveBtn){
    activeBtn.classList.add("text-green-400");
    inactiveBtn.classList.remove("text-green-400");
}

sortName.addEventListener("click", () => {
    setActive(sortName, sortScore);
});

sortScore.addEventListener("click", () => {
    setActive(sortScore, sortName);
});

document.getElementById("sortName").onclick = () => {
    data.sort((a, b) => a.neighborhood.localeCompare(b.neighborhood));
    updateVisualisation();
};

document.getElementById("sortScore").onclick = () => {
    data.sort((a, b) => b.score - a.score);
    updateVisualisation();
};

//dynamic search
document.getElementById("search").oninput = function (){
    const term = this.value.toLowerCase();
    d3.selectAll(".bar").style("opacity", d => d.neighborhood.toLowerCase().includes(term) ? 1 : 0.15);
    document.querySelectorAll("#table-body tr").forEach(row => {
        const nameStr = row.cells[0].textContent.toLowerCase();
        row.style.display = nameStr.includes(term) ? "" : "none";
    });
};

document.querySelectorAll(".tab-button").forEach(button => {
    button.onclick = function () {
        document.querySelectorAll(".tab-button").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        this.classList.add("active");
        document.getElementById(this.dataset.tab).classList.add("active");
    };
});