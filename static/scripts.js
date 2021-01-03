const $line = $("#line");
const $station = $("#station");
const $direction = $("#direction");
const $form = $("#transit-form");
const $predictionSidebar = $("#prediction-sidebar");
const $dashboard = $("#dashboard");

/* EVENT HANDLERS */

$line.on("change", changeLine);
$station.on("change", changeStation);
$form.on("submit", getAndDisplayPrediction);
$predictionSidebar.on("click", addToDashboard);

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
    const response = await axios.get(`http://127.0.0.1:5000/api/${lineID}/stations`);
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

async function getAndDisplayPrediction(evt) {
    evt.preventDefault();
    const response = await getPrediction();
    createPredictionCard(response);
    displayPredictionStop(response);
    displayPredictionTime(response);
    displayAddToDashboardButton();
}

async function getPrediction() {
    const stopID = $direction.val();
    const lineID = $line.val();
    const response = await axios.get("/transit/prediction", {
        params: {
            stopID: stopID,
            line: lineID
        }
    })
    return response;
}

function createPredictionCard(response) {
    $predictionSidebar.empty();
    const baseData = response.data.ctatt.eta[0];
    const line = baseData.rt;
    const stopID = baseData.stpId;
    const card = `<div class="card text-center mb-2" data-line=${line} data-stop=${stopID}></div>`;
    $predictionSidebar.append(card);
}

function displayPredictionStop(response) {
    const $sidebarCard = $("#prediction-sidebar .card");
    const baseData = response.data.ctatt.eta[0];
    const stationName = baseData.staNm;
    const destination = baseData.stpDe;
    const stationAndDirection = `
    <div class="card-header">
        <h3>${stationName}</h3>
        <p> ${destination}</p>
    </div>
    `;
    $sidebarCard.append(stationAndDirection);
}

function displayPredictionTime(response) {
    const $sidebarCard = $("#prediction-sidebar .card");
    const baseData = response.data.ctatt.eta[0];
    const predictionTime = new Date(baseData.prdt);
    const arrivalTime = new Date(baseData.arrT);
    const minutes = convertToMinutes(arrivalTime, predictionTime);
    const displayDate = `<h5 class="card-date">${arrivalTime.toDateString()}</h5>`
    const displayTime = `<h4 class="card-time">${arrivalTime.toLocaleTimeString("en-US")}</h4>`;
    const displayMinutes = `<h2 class="card-mins">${minutes} minutes</h2>`;
    $sidebarCard.append(displayDate, displayTime, displayMinutes);
}

function displayAddToDashboardButton() {
    const $sidebarCard = $("#prediction-sidebar .card");
    const button = `<a href="#" class="btn btn-secondary my-2" id="add-btn">Add to Dashboard</a>`;
    $sidebarCard.append(button);
}

function convertToMinutes(arrTime, prdTime) {
    const timeDifference = (arrTime.getTime() - prdTime.getTime());
    const minutes = Math.floor(timeDifference / 60000);
    return minutes;
}

/* DASHBOARD FUNCTIONALITY */

function addToDashboard(evt) {
    const $sidebarCard = $("#prediction-sidebar .card");
    const target = evt.target;
    if (target.id === "add-btn") {
        const $cardCopy = $sidebarCard.clone();
        $cardCopy.children("a").text("Delete");
        $dashboard.append($cardCopy);
        $predictionSidebar.empty();
        $form.trigger("reset");
    }
}
