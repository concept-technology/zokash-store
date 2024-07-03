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



