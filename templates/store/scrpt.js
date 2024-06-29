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
    

    $('#cart-quantity-input').on('change', function(){
        let cartId = $('#product-id').val();
        let quantity = $(this).val();
        let size = $('#size').val()

        console.log({'id':cartId, 'qty':quantity, 'size':size})
        
        $.ajax({
            url: "{% url 'store:update_cart_quantity'%}",  // Update this to your actual URL
            method: 'POST',
            data: {
                id: cartId,
                quantity: quantity,
                size: size,
                csrfmiddlewaretoken:"{{csrf_token}}"
            },
            success: function(response){
                // Handle success, maybe update the cart UI
                console.log(response)
                
            },
            error: function(response){
                console.log('error')
            }
        });
    });
});
</script>