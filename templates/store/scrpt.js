<script>
    $(document).ready(function(){
        function debounce(func, wait) {
            let timeout;
            return function(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func.apply(this, args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
    
        const updateCart = debounce(function(){
            let cartId = $('#product-id').val();
            let quantity = $('#cart-quantity-input').val();
            let size = $('#size').val();
    
            console.log('Cart update triggered', {'id': cartId, 'qty': quantity, 'size': size});
            
            $.ajax({
                url: "{% url 'store:update_cart_quantity' %}",  // Update this to your actual URL
                method: 'POST',
                data: {
                    id: cartId,
                    quantity: quantity,
                    size: size,
                    csrfmiddlewaretoken: "{{ csrf_token }}"
                },
                success: function(response){
                    // Handle success, maybe update the cart UI
                    console.log('Success response:', response);
                    alert('Cart updated successfully.');
                },
                error: function(response){
                    console.log('Error response:', response);
                    alert('There was an error updating the cart.');
                }
            });
        }, 300);  // Adjust debounce time as necessary
    
        $('#cart-quantity-input').off('change').on('change', updateCart);
    });
</script>



$(document).ready(function(){
    $('#next-button').click(function(){
        var currentProductSlug = $(this).data('slug');
        $.ajax({
            url: '{% url "store:next_product" slug=product.slug %}',
            method: 'GET',
            success: function(data) {
                if (data.slug) {
                    $('#product-title').text(data.title);
                    $('#product-description').text(data.description);
                    $('#product-price').html('&#8358;' + data.price);
                    $('#average-rating').text('Average Rating: ' + data.average_rating);
                    $('#rating-count').text('Rating Count: ' + data.rating_count);
                    $('#next-button').data('slug', data.slug);
                    window.history.pushState({}, '', '/product/' + data.slug + '/');

                    $('#product-images').empty();
                    if (data.img_1) {
                        $('#product-images').append('<img src="' + data.img_1 + '" alt="' + data.title + ' Image 1">');
                    }
                    if (data.img_2) {
                        $('#product-images').append('<img src="' + data.img_2 + '" alt="' + data.title + ' Image 2">');
                    }
                    if (data.img_3) {
                        $('#product-images').append('<img src="' + data.img_3 + '" alt="' + data.title + ' Image 3">');
                    }
                    if (data.img_4) {
                        $('#product-images').append('<img src="' + data.img_4 + '" alt="' + data.title + ' Image 4">');
                    }
                } else {
                    alert('No more products.');
                }
            }
        });
    });
});




<!-- CSS only -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
<!-- JavaScript Bundle with Popper -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>


    
<div class="container">
    <div class="row text-center w-50">
        <div class="col-sm-6 col-sm-offset-3">
        <br><br> <h2 style="color:#0fad00">Success</h2>
        {% if message %}
        <br><br> <h2 style="color:#0fad00">{{ message }}</h2>
        {% endif %}
        
        <h3>Dear {{ request.user.username }}</h3>
        <p style="font-size:20px;color:#5C5C5C;">transaction successful</p>
        <a href="{% url 'store:index' %}" class="btn btn-success"> ok </a>
    <br><br>
        </div>
        
    </div>
</div>
    
<div class="invoice-box">
    <table cellpadding="0" cellspacing="0">
        <tr class="top">
            <td colspan="2">
                <table>
                    <tr>
                        <td class="title">
                            <h2>Zokash household ventures </h2>
                        </td>
                        <td>
                            Invoice #: {{ invoice.invoice_number }}<br>
                            Issued: {{ invoice.issued_at|date:"F j, Y" }}<br>
                            Due: {{ invoice.issued_at|date:"F j, Y" }}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        
        <tr class="information">
            <td colspan="2">
                <table>
                    <tr>
                        <td>
                            Company Name, Inc.<br>
                            12345 Sunny Road<br>
                            Sunnyville, TX 12345
                        </td>
                        <td>
                            {{ order.user.get_full_name }}<br>
                            {{ order.user.email }}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        
        <tr class="heading">
            <td>Payment Method</td>
            <td>Check #</td>
        </tr>
        
        <tr class="details">
            <td>Paystack</td>
            <td>{{ payment.ref }}</td>
        </tr>
        
        <tr class="heading">
            <td>Item</td>
            <td>Price</td>
        </tr>
        
        {% for item in order.product.all %}
        <tr class="item">
            <td>{{ item.product.title }}</td>
            <td>{{ item.price }}</td>
        </tr>
        {% endfor %}
        
        <tr class="total">
            <td></td>
            <td>Total: {{ order.get_total_with_delivery }}</td>
        </tr>
    </table>

</div>


<style>
    body {
        font-family: Arial, sans-serif;
    }
    .invoice-box {
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
        font-size: 16px;
        line-height: 24px;
        color: #555;
    }
    .invoice-box table {
        width: 100%;
        line-height: inherit;
        text-align: left;
    }
    .invoice-box table td {
        padding: 5px;
        vertical-align: top;
    }
    .invoice-box table tr td:nth-child(2) {
        text-align: right;
    }
    .invoice-box table tr.top table td {
        padding-bottom: 20px;
    }
    .invoice-box table tr.top table td.title {
        font-size: 45px;
        line-height: 45px;
        color: #333;
    }
    .invoice-box table tr.information table td {
        padding-bottom: 40px;
    }
    .invoice-box table tr.heading td {
        background: #eee;
        border-bottom: 1px solid #ddd;
        font-weight: bold;
    }
    .invoice-box table tr.details td {
        padding-bottom: 20px;
    }
    .invoice-box table tr.item td {
        border-bottom: 1px solid #eee;
    }
    .invoice-box table tr.item.last td {
        border-bottom: none;
    }
    .invoice-box table tr.total td:nth-child(2) {
        border-top: 2px solid #eee;
        font-weight: bold;
    }
    .invoice-box .invoice-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .invoice-box .invoice-header .invoice-title {
        font-size: 30px;
        font-weight: bold;
        color: #333;
    }
    .invoice-box .invoice-header .invoice-number {
        font-size: 18px;
        color: #555;
    }
    .invoice-box .invoice-info {
        display: flex;
        justify-content: space-between;
        margin-bottom: 40px;
    }
    .invoice-box .invoice-info .company-info {
        flex: 1;
        margin-right: 20px;
    }
    .invoice-box .invoice-info .customer-info {
        flex: 1;
    }
    .invoice-box .invoice-info .info-title {
        font-weight: bold;
        color: #555;
    }
    .invoice-box .invoice-info .info-value {
        color: #777;
    }
    .invoice-box .invoice-items {
        margin-bottom: 20px;
    }
    .invoice-box .invoice-items .item-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .invoice-box .invoice-items .item-row .item-name {
        flex: 1;
        color: #333;
    }
    .invoice-box .invoice-items .item-row .item-price {
        flex: 0 0 100px;
        text-align: right;
        color: #555;
    }
    .invoice-box .invoice-total {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #eee;
    }
    .invoice-box .invoice-total .total-label {
        font-weight: bold;
        color: #555;
    }
    .invoice-box .invoice-total .total-value {
        font-weight: bold;
        color: #333;
    }
    .invoice-box .invoice-footer {
        margin-top: 40px;
        text-align: center;
    }
    .invoice-box .invoice-footer .success-message {
        font-size: 20px;
        color: #5C5C5C;
    }
    .invoice-box .invoice-footer .btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: #fff;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
