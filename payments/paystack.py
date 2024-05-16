from django.conf import settings
import requests

# connect to paystack API
class PayStack:
    secrete_key =  settings.PAYSTACK_SECRETE_KEY 
    base_url = 'https://api.paystack.co/'
    
    
    def check_payment(self, ref, *args, **kwargs):
        path = f"transaction/{ref}/verify"
        headers = {
            'Authorization': f"Bearer{self.secrete_key}",
            'Content_Type':'application/json',
            
        }
        url = self.base_url + path
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'],response_data['data']
        
        response_data = response.json()
        return response_data['status'],response_data['message']
