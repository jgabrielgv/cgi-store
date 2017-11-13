function increase_cart_qty(data, event) {
    var data = {
        'code': document.getElementsByName('code')[0].value,
        'quantity': document.getElementsByName('quantity')[0].value,
    };
    sendData('increase_cart_qty.py', data);
    event.preventDefault();
}