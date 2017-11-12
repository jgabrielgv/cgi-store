file = '';
function create_sugge(data, event){
    var form = document.getElementById(data);
    params = findFormField(data, form);
    sendData(file, params);
    event.preventDefault();
}

function findFormField(formName, form){
    var params = {};
    switch(formName){
        case "suge":
            params = createSugeFormParams(form);
            file = 'survey_post.py';
            break;
        case "sugeLog":
            params = createSugeLogFormParams(form);
            file = 'survey1_post.py'
            break;
        default:
            break;
    }
    return params;
}
function createSugeFormParams(form){

    var params = {
        name: form.name.value,
        reason: form.reason.value,
        message:form.message.value,
        email: form.email.value
    };
    return params;
}
function createSugeLogFormParams(form){
    
        var params = {
            reason: form.reason.value,
            message:form.message.value
        };
        return params;
    }