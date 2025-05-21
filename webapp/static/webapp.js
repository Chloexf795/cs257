window.addEventListener('load', initialize);

function initialize() {
    var element = document.getElementById('types_button');
    if (element) {
        element.onclick = onTypesButton;
    }
    var element = document.getElementById('areas_button');
    if (element) {
        element.onclick = onAreasButton;
    }
    var element = document.getElementById('start_dates_button');
    if (element) {
        element.onclick = onStartDatesButton;
    }
    var element = document.getElementById('end_dates_button');
    if (element) {
        element.onclick = onEndDatesButton;
    }
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL
}

function onTypesButton() {
    var url = getAPIBaseURL() + '/types/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(types) {
        var listBody = '';
        for (var k = 0; k < types.length; k++) {
            var type = types[k];
            listBody += '<li>' + type.toLowerCase()
                      + '</li>\n';
        }

        var typesListElement = document.getElementById('types_list');
        if (typesListElement) {
            typesListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onAreasButton() {
    var url = getAPIBaseURL() + '/areas/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(areas) {
        var listBody = '';
        for (var k = 0; k < areas.length; k++) {
            var area = areas[k];
            listBody += '<li>' + area
                      + '</li>\n';
        }

        var areasListElement = document.getElementById('areas_list');
        if (areasListElement) {
            areasListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onStartDatesButton() {
    var url = getAPIBaseURL() + '/dates/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(dates) {
        var listBody = '';
        for (var k = 0; k < dates.length; k++) {
            var date = dates[k];
            listBody += '<li>' + date
                      + '</li>\n';
        }

        var StartdatesListElement = document.getElementById('start_dates_list');
        if (StartdatesListElement) {
            StartdatesListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onEndDatesButton() {
    var url = getAPIBaseURL() + '/dates/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(dates) {
        var listBody = '';
        for (var k = 0; k < dates.length; k++) {
            var date = dates[k];
            listBody += '<li>' + date
                      + '</li>\n';
        }

        var endDatesListElement = document.getElementById('end_dates_list');
        if (endDatesListElement) {
            endDatesListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}