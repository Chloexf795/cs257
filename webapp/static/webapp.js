window.addEventListener('load', initialize);

function initialize() {
    var elementTypes = document.getElementById('types_selector');
    if (elementTypes) {
        elementTypes.onclick = loadTypesSelector();
    }
    
    var elementAreas = document.getElementById('areas_selector');
    if (elementAreas) {
        elementAreas.onclick = loadAreasSelector();
    }
    var elementStartDates = document.getElementById('start_dates_selector');
    if (elementStartDates) {
        elementStartDates.onclick = loadStartDatesSelector();
    }
    var elementEndDates = document.getElementById('end_dates_selector');
    if (elementEndDates) {
        elementEndDates.onclick = loadEndDatesSelector();
    }
    var search = document.getElementById('search_button');
    if (search) {
        search.onclick = onCrimesSelectionChanged;
    }
    
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL
}

//onTypesButton()
function loadTypesSelector() {
    var url = getAPIBaseURL() + '/types';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(types) {
        var selectorBody = '';
        for (var k = 0; k < types.length; k++) {
            var type = types[k];
            selectorBody += '<option>' + type.toLowerCase() + '</option>\n' 
        }

        var selector = document.getElementById('types_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function loadAreasSelector() {
    var url = getAPIBaseURL() + '/areas';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(areas) {
        var selectorBody = '';
        for (var k = 0; k < areas.length; k++) {
            var area = areas[k];
            selectorBody += '<option>' + area + '</option>\n';
        }

        var selector = document.getElementById('areas_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function loadStartDatesSelector() {
    var url = getAPIBaseURL() + '/dates';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(dates) {
        var selectorBody = '';
        for (var k = 0; k < dates.length; k++) {
            var date = dates[k];
            selectorBody += '<option>' + date + '</option>\n';
        }

        var selector = document.getElementById('start_dates_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function loadEndDatesSelector() {
    var url = getAPIBaseURL() + '/dates';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(dates) {
        var selectorBody = '';
        for (var k = 0; k < dates.length; k++) {
            var date = dates[k];
            selectorBody += '<option>' + date
                      + '</option>\n';
        }

        var endDatesSelectorElement = document.getElementById('end_dates_selector');
        if (endDatesSelectorElement) {
            endDatesSelectorElement.innerHTML = selectorBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onCrimesSelectionChanged() {
    var elementTypes = document.getElementById('types_selector');
    var elementAreas = document.getElementById('areas_selector');
    var elementStartDates = document.getElementById('start_dates_selector');
    var elementEndDates = document.getElementById('end_dates_selector');
    type = elementTypes.value
    area = elementAreas.value
    start_date = elementStartDates.value
    end_date = elementEndDates.value

    let url = getAPIBaseURL() + '/crimes?' + 'type=' + type 
    + '&area=' + area 
    + '&start_date=' + start_date 
    + '&end_date=' + end_date

    fetch(url, {method:'get'})

    .then((response) => response.json())

    .then (function(crimes) {

        tableBody  = '<tr>'
        + '<td>' + 'id' + '</td>'
        + '<td>' + 'victim age' + '</td>'
        + '<td>' + 'victim sex' + '</td>'
        + '<td>' + 'location' + '</td>'
        + '</tr>\n';
        for (let k = 0; k < crimes.length; k++) {
            let crime = crimes[k];
            tableBody += '<tr>'
                            + '<td>' + k+1 + '</td>'
                            + '<td>' + crime['victim_age'] + '</td>'
                            + '<td>' + crime['victim_sex'] + '</td>'
                            + '<td>' + crime['location'] + '</td>'
                            + '</tr>\n';
        }
    })
    
    let crimesTable = document.getElementById('crimes_table');
    if (crimesTable) {
        crimesTable.innerHTML = tableBody
    }
}