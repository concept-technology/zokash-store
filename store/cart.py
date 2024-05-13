class SessionCart():
    cart = ''
    def __init__(self, request):
        cart = request.session.get('session_key')
        self.session = request.session
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            self.cart = cart
        
    def add(self, product):
        product_id = str(product.id)
        if str(product_id) in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}
        self.session.modified = True