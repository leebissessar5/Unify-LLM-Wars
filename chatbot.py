from unify import Unify
import requests

class ChatBot:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        self.client = Unify(api_key=api_key, endpoint=endpoint)
        self.message_history = []

    def send_message(self, message):
        self.message_history.append({'role': 'user', 'content': message})
        try:
            response = self.client.generate(messages=self.message_history)
            self.message_history.append({'role': 'assistant', 'content': response})
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def get_credits(self):
        """Retrieve the credit balance using the Unify API."""
        url = 'https://api.unify.ai/v0/get_credits'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['credits']
        else:
            return f"Error fetching credits: {response.json().get('error', 'Unknown error')}"