(function IIFE(document) {
    console.log("test2");
    var center = document.getElementsByTagName('center')[0]
    var form = document.createElement("form");
    form.setAttribute("method", "POST");
    form.setAttribute("action", "#");

    var table = 
    `
    <fieldset>
        <legend><b>¡Si no estas de acuerdo con los precios de venta, deja tu comentario!</b></legend>
        <p>Parece que tu sesión ha expirado, pero <b>puedes iniciar sesión y enviar el comentario a la misma vez!</b></p>
        <table>
            <tr>
                <td>Usuario</td>
                <td><input type='text' name='username'></td>
            </tr>
            <tr>
                <td>Clave</td>
                <td><input type='password' name='password'></td>
            </tr>
            <tr>
                <td>Comentario</td>
                <td><textarea rows="4" cols="50" name="message"></textarea></td>
            </tr>
            <tr>
                <td><input type='submit' value='Enviar'></td>
            </tr>
        </table>
    </fieldset>
     `
    form.innerHTML = table;
    //insert element before h1 element
    center.insertBefore(form, document.getElementsByTagName('center')[0].children[0]);
})(document);