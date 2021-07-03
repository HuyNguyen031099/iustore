

// 
$('.qty-add').click(function() {
    let qty_value = $(this).closest('.qty-input').find('.qty-value');
    
    qty_value.val(+(qty_value.val()) + 1)

    let item_id = $(this).closest('.qty-input').find('.item-id').val();
    addToCart(item_id, 1)
})
$('.qty-minus').click(function() {
    let qty_value = $(this).closest('.qty-input').find('.qty-value');
    
    if (+(qty_value.val()) == 1) {
        return
    }

    let item_id = $(this).closest('.qty-input').find('.item-id').val();
    addToCart(item_id, -1)
    qty_value.val(+(qty_value.val()) - 1)
})

const addToCart = (item_id, qty) => {
    $.ajax({
        url: "http://127.0.0.1:8000/mystore/add-to-cart",
        type: 'GET',
        data: {
            'item_id': `${item_id}`,
            'qty': qty
        },
        dataType: 'json', 
        success: function (res) {
            console.log(res)
            const totalPrice = res.totalPrice.toLocaleString('it-IT', {style : 'currency', currency : 'VND'});
            $('#totalPrice').html(totalPrice)
        }
    });
}