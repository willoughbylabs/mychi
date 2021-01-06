const $line = $("#line");
const $station = $("#station");
const $direction = $("#direction");
const $form = $("#transit-form");
const $predictionSidebar = $("#prediction-sidebar");
const $dashboard = $("#dashboard");
let savedStops;
if (typeof stops !== "undefined") {
    savedStops = stops;
}

/* EVENT HANDLERS */

$line.on("change", changeLine);
$station.on("change", changeStation);
$form.on("submit", getAndDisplayPrediction);
$predictionSidebar.on("click", predictionClick);
$dashboard.on("click", dashboardClick);

/* RESTORE DASHBOARD */
restoreDashboard();

/* DROPDOWN FUNCTIONALITY */

// Get and display stations for selected line.
async function changeLine() {
    const stations = await getStations();
    displayStations(stations);
    changeStation();
}

// Get JSON of stations in database for selected line.
async function getStations() {
    const lineID = $line.val();
    const response = await axios.get(`/api/${lineID}/stations`);
    return response;
}

// Display stations in dropdown for selected line.
function displayStations(stations) {
    $station.empty();
    const stationsArr = stations.data.stations;
    const selected = '<option value="" selected>Choose...</option>';
    $station.append(selected);
    stationsArr.forEach(station => {
        const option = `<option value="${station.station_name}">${station.station_name}</option>`;
        $station.append(option);
    });
}

// Get and display stops (direction) for a selected line and station.
async function changeStation() {
    const stops = await getStops();
    displayStops(stops);
}

// Get JSON of stops (direction) for a selected line and station.
async function getStops() {
    const lineID = $line.val();
    const stationName = $station.val();
    const response = await axios.get("/api/stops", {
        params: {
            line: lineID,
            station: stationName
        }
    });
    return response;
}

// Display stops (direction) in dropdown for selected line and station.
function displayStops(stops) {
    $direction.empty();
    const stopsArr = stops.data.stops;
    const selected = '<option value="" selected>Choose...</option>';
    $direction.append(selected);
    stopsArr.forEach(stop => {
        const option = `<option value="${stop.stop_id}">${stop.stop_name}</option>`;
        $direction.append(option);
    })
}

/* PREDICTION FUNCTIONALITY */

// Display card with prediction data in sidebar.
async function getAndDisplayPrediction(evt) {
    evt.preventDefault();
    const response = await getPrediction("sidebar");
    createPredictionCard(response, "sidebar");
    displayPredictionStop(response, "sidebar");
    displayPredictionTime(response, "sidebar");
    displayPredictionButton("sidebar");
}

// Get prediction from CTA Arrivals API.
async function getPrediction(source, stop = undefined) {
    let stopID, lineID, response;
    // New prediction from sidebar.
    if (source === "sidebar") {
        stopID = $direction.val();
        lineID = $line.val();
    }
    // Restore prediciton from dashboard.
    if (source === "dashboard") {
        stopID = stop.stop;
        lineID = stop.line;
    }
    response = await axios.get("/transit/prediction", {
        params: {
            stopID: stopID,
            line: lineID
        }
    })
    return response;
}

// Create prediction card to display prediction data.
function createPredictionCard(response, location) {
    const baseData = response.data.ctatt.eta[0];
    const line = baseData.rt;
    const stopID = baseData.stpId;
    const card = `<div class="card text-center mb-2" data-line=${line} data-stop=${stopID}></div>`;
    // If displaying prediction card in sidebar.
    if (location === "sidebar") {
        $predictionSidebar.empty();
        $predictionSidebar.append(card);
    }
    // If restoring prediction card to dashboard.
    if (location === "dashboard") {
        $dashboard.append(card);
    }
}

// Append station name and destination to prediction card.
function displayPredictionStop(response, location, stop = undefined) {
    const baseData = response.data.ctatt.eta[0];
    const stationName = baseData.staNm;
    const destination = baseData.stpDe;
    const stationAndDirection = `
    <div class="card-header">
        <h3>${stationName}</h3>
        <p> ${destination}</p>
    </div>
    `;
    // If displaying station and direction for sidebar card.
    if (location === "sidebar") {
        const $sidebarCard = $("#prediction-sidebar .card");
        $sidebarCard.append(stationAndDirection);
    }
    // If restoring station and direction for dashboard card.
    if (location === "dashboard") {
        const $dashboardCard = $(`div[data-line=${stop.line}][data-stop=${stop.stop}]`);
        $dashboardCard.append(stationAndDirection);
    }
}

// Append arrival time and tim in minutes to prediction card.
function displayPredictionTime(response, location, stop = undefined) {
    const baseData = response.data.ctatt.eta[0];
    const predictionTime = new Date(baseData.prdt);
    const arrivalTime = new Date(baseData.arrT);
    const minutes = convertToMinutes(arrivalTime, predictionTime);
    const displayDate = `<h5 class="card-date">${arrivalTime.toDateString()}</h5>`
    const displayTime = `<h4 class="card-time">${arrivalTime.toLocaleTimeString("en-US")}</h4>`;
    const displayMinutes = `<h2 class="card-mins">${minutes} minutes</h2>`;
    // If displaying arrival prediction for sidebar card.
    if (location === "sidebar") {
        const $sidebarCard = $("#prediction-sidebar .card");
        $sidebarCard.append(displayDate, displayTime, displayMinutes);
    }
    // If restoring arrival prediction for dashboard card.
    if (location === "dashboard") {
        const $dashboardCard = $(`div[data-line=${stop.line}][data-stop=${stop.stop}]`);
        $dashboardCard.append(displayDate, displayTime, displayMinutes);
    }
}

// Append button to add prediction to dashboard.
function displayPredictionButton(location, stop = undefined) {
    if (location === "sidebar") {
        const button = `<a href="#" class="btn btn-secondary my-2" id="add-btn">Add to Dashboard</a>`;
        const $sidebarCard = $("#prediction-sidebar .card");
        $sidebarCard.append(button);
    }
    if (location === "dashboard") {
        const button = `<a href="#" class="btn btn-secondary my-2" id="dlt-btn">Delete</a>`;
        const $dashboardCard = $(`div[data-line=${stop.line}][data-stop=${stop.stop}]`);
        $dashboardCard.append(button);
    }
}

// Get arrival time in minutes by subtracting predicted time from arrival time. 
function convertToMinutes(arrTime, prdTime) {
    const timeDifference = (arrTime.getTime() - prdTime.getTime());
    const minutes = Math.floor(timeDifference / 60000);
    return minutes;
}

// Event handler function for add prediction to dashboard button. 
function predictionClick(evt) {
    const target = evt.target;
    if (target.id === "add-btn") {
        addOrDeletePRDTSession(target.parentElement, "add");
        addToDashboard();
    }
}
/* DASHBOARD FUNCTIONALITY */

// Event handler function for delete prediction from dashboard button.
function dashboardClick(evt) {
    const target = evt.target;
    if (target.id === "dlt-btn") {
        addOrDeletePRDTSession(target.parentElement, "delete");
        deleteFromDashboard(target);
    }
}

// Add prediction card to dashboard.
function addToDashboard() {
    const $sidebarCard = $("#prediction-sidebar .card");
    const $cardCopy = $sidebarCard.clone();
    $cardCopy.children("a").text("Delete");
    $cardCopy.children("a").attr("id", "dlt-btn");
    $dashboard.append($cardCopy);
    $predictionSidebar.empty();
    $form.trigger("reset");
}

// Delete prdiction card from dashboard. 
function deleteFromDashboard(target) {
    target.parentElement.remove();
}

/* SESSION/COOKIE SAVED STOPS FUNCTIONALITY */

// Add or delete saved stop from session.
async function addOrDeletePRDTSession(card, action) {
    const line = card.dataset.line;
    const stop = card.dataset.stop;
    if (action === "add") {
        const response = await axios.post("/transit/prediction/session", {
            data: { line, stop }
        });
    }
    if (action === "delete") {
        const response = await axios.delete("/transit/prediction/session", {
            data: { line, stop }
        });
    }
}

// If saved stops in session, restore prediction cards on dashboard.
async function restoreDashboard() {
    if (savedStops === undefined) {
        return;
    }
    else {
        for (const stop of savedStops) {
            response = await getPrediction("dashboard", stop);
            createPredictionCard(response, "dashboard");
            displayPredictionStop(response, "dashboard", stop);
            displayPredictionTime(response, "dashboard", stop);
            displayPredictionButton("dashboard", stop);
        }
    }
}