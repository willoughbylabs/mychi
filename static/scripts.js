const $line = $("#line");
const $station = $("#station");
const $direction = $("#direction");
const $form = $("#transit-form");
const $predictionSidebar = $("#prediction-sidebar");

/* EVENT HANDLERS */

$line.on("change", changeLine);
$station.on("change", changeStation);
$form.on("submit", getAndDisplayPrediction);

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

function displayPredictionStop(response) {
    const baseData = response.data.ctatt.eta[0];
    const stationName = baseData.staNm;
    const destination = baseData.stpDe;
    const line = baseData.rt;
    const stopID = baseData.stpId;
    const card = `<div class="card text-center" id="card-sidebar" data-line="${line}" data-stopID="${stopID}"></div>`;
    $predictionSidebar.append(card);
    const $displayCard = $("#card-sidebar");
    const displayStationAndDirection = `
    <div class="card-header">
        <h5>${stationName}</h5>
        <p> ${destination}</p>
    </div>
    `;
    $displayCard.append(displayStationAndDirection);
}

function displayPredictionTime(response) {
    const baseData = response.data.ctatt.eta[0];
    const predictionTime = baseData.prdt;
    const arrivalTime = baseData.arrT;
    const $displayCard = $("#card-sidebar");
    $displayCard.append(predictionTime, arrivalTime);
}

function displayAddToDashboardButton() {
    const $displayCard = $("#card-sidebar");
    const button = `<a href="#" class="btn btn-secondary mb-3">Add to Dashboard</a>`;
    $displayCard.append(button);
}
