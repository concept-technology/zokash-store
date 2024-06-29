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