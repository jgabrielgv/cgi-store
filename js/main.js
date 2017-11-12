function sendData(url, params) {
    var esc = encodeURIComponent;
    var query = Object.keys(params)
        .map(k => esc(k) + '=' + esc(params[k]))
        .join('&');
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: query
    }).then(response => {
        return response.json().then(data => {
            if (response.ok) {
                return data;
            } else {
                return Promise.reject({ status: response.status, data });
            }
        });
    })
        .then(result => console.log('success:', result))
        .catch(error => mapErrors(params, error.data));
}
function cleanupCurrentControls(fields) {
    for (let item in fields) {
        let element = document.getElementById(`invalid_${item}`);
        if (!element) { continue; }
        element.children[1].style.display = "none";
        if (element.className && element.className.includes("form-invalid-data")) {
            element.className = "";
            element.children[1].lastElementChild.innerHTML = '';
        }
    }
    let element = document.getElementById(`validation_error`);
    if (!element) { return; }
    element.children[0].style.display = "none";
    if (element.className && element.className.includes("form-invalid-data")) {
        element.className = "";
        element.children[1].lastElementChild.innerHTML = '';
    }
}
function mapErrors(fields, response) {
    if (!response) { return; }
    cleanupCurrentControls(fields);
    for (let item in response) {
        let element = document.getElementById(item);
        if (!element) { continue; }
        element.className = "form-invalid-data";
        if (item == 'validation_error') {
            element.children[0].lastElementChild.innerHTML = response[item];
            element.children[0].style.display = "block";
        } else {
            element.children[1].lastElementChild.innerHTML = response[item];
            element.children[1].style.display = "block";
        }
    }
}