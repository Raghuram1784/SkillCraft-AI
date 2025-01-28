# email_handler.py
import requests

def send_email_to_admin(name, email):
    url = "http://localhost:3001/send-email"  # Use localhost in Codespaces
    data = {"name": name, "email": email}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print("Failed to send email:", response.text)
    except Exception as e:
        print("Error:", e)