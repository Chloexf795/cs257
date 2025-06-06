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

function createCheckbox(value, containerId) {
    const label = document.createElement('label');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = value;
    checkbox.checked = false; // Default to unchecked
    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(value));
    document.getElementById(containerId).appendChild(label);
}

function toggleAll(type) {
    const selectAllCheckbox = document.getElementById(`select-all-${type}`);
    const checkboxes = document.getElementById(`${type}_selector`).getElementsByTagName('input');
    
    for (let checkbox of checkboxes) {
        checkbox.checked = selectAllCheckbox.checked;
    }
}

function loadTypesSelector() {
    const url = getAPIBaseURL() + '/types';

    fetch(url)
        .then(res => res.json())
        .then(types => {
            const container = document.getElementById('types_selector');
            container.innerHTML = ''; // Clear existing content
            for (const type of types) {
                createCheckbox(type.toLowerCase(), 'types_selector');
            }
        });
}

function loadAreasSelector() {
    const url = getAPIBaseURL() + '/areas';

    fetch(url)
        .then(res => res.json())
        .then(areas => {
            const container = document.getElementById('areas_selector');
            container.innerHTML = ''; // Clear existing content
            for (const area of areas) {
                createCheckbox(area, 'areas_selector');
            }
        });
}

function loadStartDatesSelector() {
    const url = getAPIBaseURL() + '/dates';

    fetch(url)
        .then(res => res.json())
        .then(dates => {
            let options = '<option value="">Select Start Date</option>\n';
            for (const date of dates) {
                options += `<option value="${date}">${date}</option>\n`;
            }
            document.getElementById('start_dates_selector').innerHTML = options;
        });
}

function loadEndDatesSelector() {
    const url = getAPIBaseURL() + '/dates';

    fetch(url)
        .then(res => res.json())
        .then(dates => {
            let options = '<option value="">Select End Date</option>\n';
            for (const date of dates) {
                options += `<option value="${date}">${date}</option>\n`;
            }
            document.getElementById('end_dates_selector').innerHTML = options;
        });
}

function getSelectedValues(containerId) {
    const container = document.getElementById(containerId);
    const checkboxes = container.getElementsByTagName('input');
    const selectedValues = [];
    
    for (let checkbox of checkboxes) {
        if (checkbox.checked) {
            selectedValues.push(checkbox.value);
        }
    }
    
    return selectedValues;
}

function loadCrimeChart() {
    const ctx = document.getElementById('crimeChart').getContext('2d');
    crimeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03"],
            datasets: [{
                label: 'Crimes Per Month',
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                backgroundColor: 'rgba(54, 162, 235, 0.6)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
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
    const selectedTypes = getSelectedValues('types_selector');
    const selectedAreas = getSelectedValues('areas_selector');
    const start_date = document.getElementById('start_dates_selector').value;
    const end_date = document.getElementById('end_dates_selector').value;

    if (selectedTypes.length === 0 || selectedAreas.length === 0 || 
        !start_date || !end_date) {
        alert('Please select at least one type, one area, and both start and end dates');
        return;
    }

    const baseURL = getAPIBaseURL();
    const chartUrl = `${baseURL}/charts/filtered?types=${selectedTypes.join(',')}&areas=${selectedAreas.join(',')}&start_month=${start_date}&end_month=${end_date}`;

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
                data.month_counts["2024-06"] || 0,
                data.month_counts["2024-07"] || 0,
                data.month_counts["2024-08"] || 0,
                data.month_counts["2024-09"] || 0,
                data.month_counts["2024-10"] || 0,
                data.month_counts["2024-11"] || 0,
                data.month_counts["2024-12"] || 0,
                data.month_counts["2025-01"] || 0,
                data.month_counts["2025-02"] || 0,
                data.month_counts["2025-03"] || 0
            ];
            crimeChart.update();
            const allZero = crimeChart.data.datasets[0].data.every(value => value === 0);
            if (allZero) {
                document.getElementById('overall-text').innerHTML = "No crime data";
            } else {
                document.getElementById('overall-text').innerHTML = "";
            }
                
            

            // Update age chart
            if (data.age_buckets && Object.keys(data.age_buckets).length > 0) {
                const ageLabels = Object.keys(data.age_buckets);
                const ageData = Object.values(data.age_buckets);
                document.getElementById('age-text').innerHTML = "Victim Ages";
                ageChart.data.labels = ageLabels;
                ageChart.data.datasets[0].data = ageData;
                ageChart.update();
            } else {
                console.log('No age data available');
                document.getElementById('age-text').innerHTML = "No age data available";
                ageChart.data.labels = [];
                ageChart.data.datasets[0].data = [];
                ageChart.update();
            }

            // Update sex chart
            if (data.sex_counts && Object.keys(data.sex_counts).length > 0) {
                const sexLabels = Object.keys(data.sex_counts);
                const sexData = Object.values(data.sex_counts);
                document.getElementById('sex-text').innerHTML = "Victim Sex";
                sexChart.data.labels = sexLabels;
                sexChart.data.datasets[0].data = sexData;
                sexChart.update();
            } else {
                console.log('No sex data available');
                document.getElementById('sex-text').innerHTML = "No sex data available";
                sexChart.data.labels = [];
                sexChart.data.datasets[0].data = [];
                sexChart.update();
            }
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
            alert('Error fetching chart data');
        });
}
