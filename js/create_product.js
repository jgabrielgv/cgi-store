function create_product(data, event) {
    var form = document.getElementsByName(data);
    var data = {
        'code': document.getElementsByName('code')[0].value,
        'descr': document.getElementsByName('descr')[0].value,
        'price': document.getElementsByName('price')[0].value
    };
    sendData('createproduct_post.py', data);
    event.preventDefault();
}