# LINEに通知
import requests
import sys
import os

IN_COLAB = 'google.colab' in sys.modules
IN_KAGGLE = 'kaggle_web_client' in sys.modules
LOCAL = not (IN_KAGGLE or IN_COLAB)
print(f'IN_COLAB:{IN_COLAB}, IN_KAGGLE:{IN_KAGGLE}, LOCAL:{LOCAL}')

def send_line_notification(message):
    env = ""
    if IN_COLAB: env = "colab"
    elif IN_KAGGLE: env = "kaggle"
    elif LOCAL: env = "local"
        
    line_token = os.getenv('LINE_API_KEY')
    endpoint = 'https://notify-api.line.me/api/notify'
    message = f"[{env}]{message}"
    payload = {'message': message}
    headers = {'Authorization': 'Bearer {}'.format(line_token)}
    requests.post(endpoint, data=payload, headers=headers)

if __name__ == '__main__':
    send_line_notification("test")