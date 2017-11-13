
function place_order(frmId, event) {
    if (!confirm("¿Desea confirmar el pago de los productos en el carrito?")) {
        event.preventDefault();
        return;
    }
    var form  = document.getElementById(frmId);
    let data = { "address": form.getElementsByName('address')[0].value, };
    sendData('place_order.py', data);
    event.preventDefault();
}