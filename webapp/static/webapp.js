window.addEventListener('load', initialize);

let crimeChart, ageChart, sexChart;

function initialize() {
    loadTypesSelector();
    loadAreasSelector();
    loadStartDatesSelector();
    loadEndDatesSelector();

    const search = document.getElementById('search_button');
    if (search) {
        search.onclick = onCrimesSelectionChanged;
    }

    loadCrimeChart();
    loadAgeChart();
    loadSexChart();
}

function getAPIBaseURL() {
    return window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
}

function loadTypesSelector() {
    const url = getAPIBaseURL() + '/types';

    fetch(url)
        .then(res => res.json())
        .then(types => {
            let body = '';
            for (const type of types) {
                body += `<option>${type.toLowerCase()}</option>\n`;
            }
            document.getElementById('types_selector').innerHTML = body;
        });
}

function loadAreasSelector() {
    const url = getAPIBaseURL() + '/areas';

    fetch(url)
        .then(res => res.json())
        .then(areas => {
            let body = '';
            for (const area of areas) {
                body += `<option>${area}</option>\n`;
            }
            document.getElementById('areas_selector').innerHTML = body;
        });
}

function loadStartDatesSelector() {
    const url = getAPIBaseURL() + '/dates';

    fetch(url)
        .then(res => res.json())
        .then(dates => {
            let body = '';
            for (const date of dates) {
                body += `<option>${date}</option>\n`;
            }
            document.getElementById('start_dates_selector').innerHTML = body;
        });
}

function loadEndDatesSelector() {
    const url = getAPIBaseURL() + '/dates';

    fetch(url)
        .then(res => res.json())
        .then(dates => {
            let body = '';
            for (const date of dates) {
                body += `<option>${date}</option>\n`;
            }
            document.getElementById('end_dates_selector').innerHTML = body;
        });
}

function loadCrimeChart() {
    const ctx = document.getElementById('crimeChart').getContext('2d');
    crimeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["2025-01", "2025-02", "2025-03"],
            datasets: [{
                label: 'Crimes Per Month',
                data: [0, 0, 0],
                backgroundColor: 'rgba(54, 162, 235, 0.6)'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });
}

function loadAgeChart() {
    const ageCtx = document.getElementById('ageChart').getContext('2d');
    ageChart = new Chart(ageCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Victim Ages',
                data: [],
                backgroundColor: 'rgba(255, 99, 132, 0.6)'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });
}

function loadSexChart() {
    const sexCtx = document.getElementById('sexChart').getContext('2d');
    sexChart = new Chart(sexCtx, {
        type: 'pie',
        data: {
            labels: [],
            datasets: [{
                label: 'Victim Sex',
                data: [],
                backgroundColor: [
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)'
                ]
            }]
        },
        options: { responsive: true }
    });
}

function onCrimesSelectionChanged() {
    const type = document.getElementById('types_selector').value;
    const area = document.getElementById('areas_selector').value;
    const start_date = document.getElementById('start_dates_selector').value;
    const end_date = document.getElementById('end_dates_selector').value;

    const baseURL = getAPIBaseURL();

    const url = `${baseURL}/crimes?type=${type}&area=${area}&start_month=${start_date}&end_month=${end_date}`;
    fetch(url)
        .then(res => res.json())
        .then(crimes => {
            let tableBody = `<tr>
                <td>id</td>
                <td>victim age</td>
                <td>victim sex</td>
                <td>location</td>
            </tr>\n`;

            for (let i = 0; i < crimes.length; i++) {
                const crime = crimes[i];
                tableBody += `<tr>
                    <td>${i + 1}</td>
                    <td>${crime.victim_age}</td>
                    <td>${crime.victim_sex}</td>
                    <td>${crime.location}</td>
                </tr>\n`;
            }

            const crimesTable = document.getElementById('crimes_table');
            if (crimesTable) {
                crimesTable.innerHTML = tableBody;
            }
        });

    // Update charts with filtered data
    const chartUrl = `${baseURL}/charts/filtered?type=${type}&area=${area}&start_month=${start_date}&end_month=${end_date}`;
    fetch(chartUrl)
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            console.log('Received chart data:', data);

            // Update crime chart
            crimeChart.data.datasets[0].data = [
                data.month_counts["2025-01"] || 0,
                data.month_counts["2025-02"] || 0,
                data.month_counts["2025-03"] || 0
            ];
            crimeChart.update();

            // Update age chart
            if (data.age_buckets && Object.keys(data.age_buckets).length > 0) {
                const ageLabels = Object.keys(data.age_buckets);
                const ageData = Object.values(data.age_buckets);
                document.getElementById('age-text').innerHTML = "victim sex";
                ageChart.data.labels = ageLabels;
                ageChart.data.datasets[0].data = ageData;
                ageChart.update();
            } else {
                console.log('No age data available');
                document.getElementById('age-text').innerHTML = "victim age not available";
                ageChart.data.labels = [];
                ageChart.data.datasets[0].data = [];
                ageChart.update();
            }

            // Update sex chart
            if (data.sex_counts && Object.keys(data.sex_counts).length > 0) {
                const sexLabels = Object.keys(data.sex_counts);
                const sexData = Object.values(data.sex_counts);
                document.getElementById('sex-text').innerHTML = "victim sex";
                sexChart.data.labels = sexLabels;
                sexChart.data.datasets[0].data = sexData;
                sexChart.update();
            } else {
                console.log('No sex data available');
                document.getElementById('sex-text').innerHTML = "victim sex not available";
                sexChart.data.labels = [];
                sexChart.data.datasets[0].data = [];
                sexChart.update();
            }
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
        });
}
