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
        /*}).then(function (response) {
            var json = response.json();
            if(response.ok)
                return json;
            else
                json.then(Promise.reject.bind(Promise));
        }).then(function(data){
            console.log(data);
        }).catch(function (err) {
            mapErrors(params, err);
        });*/
        /*}).then(response => Promise.all([response.ok, response.json()]))
            .then(([responseOk, body]) => {
                if (responseOk) {
                    // handle success case 
                } else { throw new Error(body); }
            })
            .catch(error => { // catches error case and if fetch itself rejects 
                mapErrors(params, error);
            });*/
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
function mapErrors(fields, response) {
    for (let item in fields) {
        let element = document.getElementById(`invalid_${item}`);
        element.children[1].style.display = "none";
        if (element.className && element.className.includes("form-invalid-data")) {
            element.className = "";
            element.children[1].lastElementChild.innerHTML = '';
        }
    }
    for (let item in response) {
        let element = document.getElementById(item);
        element.className = "form-invalid-data";
        element.children[1].lastElementChild.innerHTML = response[item];
        element.children[1].style.display = "block";
    }
}