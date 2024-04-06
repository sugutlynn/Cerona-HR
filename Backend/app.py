from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure mail settings using environment variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

# Endpoint for handling contact form submissions
@app.route('/contact', methods=['POST'])
def contact_form():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Send email
        msg = Message(subject='New Message from Contact Form',
                      sender=email,
                      recipients=['arthurbreck417@gmail.com'])  # Replace with your email address
        msg.body = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        
        return jsonify({'message': 'Message sent successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
