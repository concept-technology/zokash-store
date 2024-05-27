from django.conf import settings
import requests


class Paystack:
    def verify_payment(self, ref,):
        path = f'transaction/verify/{ref}'
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        url = "https://api.paystack.co/" + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']['amount']

        response_data = response.json()

        return response_data['status'], response_data['message']

