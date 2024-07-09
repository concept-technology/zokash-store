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
        let updateCartUrl = $('#cart-btn').data('update-cart-quantity-url');

        console.log('Cart update triggered', {'id': cartId, 'qty': quantity, 'size': size});
        
        $.ajax({
            url: updateCartUrl,
            method: 'POST',
            data: {
                id: cartId,
                quantity: quantity,
                size: size,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function(response){
                console.log('Success response:', response);
                $('#new-price').text(`₦${response.total_price.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`);
                $('#cart-quantity-input').val(response.qty);
            },
            error: function(response){
                console.log('Error response:', response);
            }
        });
    }, 300);  // Adjust debounce time as necessary

    $('#cart-quantity-input').off('change').on('change', updateCart);

    function addToCart() {
        let productSlug = $('#product-slug').val();
        let addToCartUrl = $('#cart-btn').data('add-to-cart-url');
        console.log('Add to cart triggered', { 'slug': productSlug });

        $.ajax({
            url: addToCartUrl,
            method: 'POST',
            data: {
                slug: productSlug,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function(response) {
                console.log('Success response:', response);
                $('#cart-count').html(response.cart_count);
                
                $('#cart-btn').attr('id', 'delete-btn').text('Delete from Cart');
                
                response.messages.forEach(function(message) {
                    Swal.fire({
                        text: message.message,
                        icon: message.tags.includes('success') ? 'success' : 'error',
                        timer: 3000,
                        showConfirmButton: false
                    });
                });

                $('#delete-btn').off('click').on('click', deleteFromCart);
            },
            error: function(response) {
                console.log('Error response:', response);
            }
        });
    }

    function deleteFromCart() {
        let productSlug = $('#product-slug').val();
        let deleteFromCartUrl = $('#delete-btn').data('delete-from-cart-url');
        console.log('Delete from cart triggered', { 'slug': productSlug });

        $.ajax({
            url: deleteFromCartUrl,
            method: 'POST',
            data: {
                slug: productSlug,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function(response) {
                console.log('Success response:', response);
                $('#cart-count').html(response.cart_count);
                
                $('#delete-btn').attr('id', 'cart-btn').text('Add to Cart');

                response.messages.forEach(function(message) {
                    Swal.fire({
                        text: message.message,
                        icon: message.tags.includes('success') ? 'success' : 'error',
                        timer: 3000,
                        showConfirmButton: false
                    });
                });

                $('#cart-btn').off('click').on('click', addToCart);
            },
            error: function(response) {
                console.log('Error response:', response);
            }
        });
    }

    $(document).ready(function() {
        $('#cart-btn').off('click').on('click', addToCart);
    });

    $('#cart-btn').off('click').on('click', addToCart);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
