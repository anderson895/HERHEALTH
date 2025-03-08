import random
import smtplib
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'rksdjghsekuhh'  
CORS(app)

# Flask-Mail Configuration (Replace with your SMTP details)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'angeladeniseflores199@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'rpbm yjls katl wcrt'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'angeladeniseflores199@gmail.com'

mail = Mail(app)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

# Generate a 6-digit OTP
def generate_verification_code():
    return str(random.randint(100000, 999999))  

# Send OTP via Email
def send_verification_email(email, otp):
    try:
        msg = Message("Your Verification Code", recipients=[email])
        msg.body = f"Your verification code is: {otp}. Please enter this code to verify your account."
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/createAccount', methods=['POST'])
def createAccount():
    data = request.get_json()

    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')

    if not fullname or not email or not password:
        return jsonify({"status": "failed", "message": "Missing required fields"}), 400

    verification_code = generate_verification_code()

    # Store user data in session
    session['fullname'] = fullname
    session['email'] = email
    session['password'] = generate_password_hash(password)
    session['verification_code'] = verification_code 

    # Send OTP email
    if send_verification_email(email, verification_code):
        return jsonify({
            "status": "success",
            "message": "Account created successfully. Verification code sent.",
            "redirect": "/verify"
        })
    else:
        return jsonify({"status": "failed", "message": "Failed to send verification email"}), 500

@app.route('/verificationCode', methods=['GET'])
def get_verification_code():
    if 'email' in session:
        return jsonify({
            "status": "success",
            "fullname": session.get('fullname'),
            "email": session.get('email'),
            "password": session.get('password'),  
            "verification_code": session.get('verification_code')
        })
    
    return jsonify({"status": "failed", "message": "No account data found"}), 404

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    user_otp = data.get('otp')

    if user_otp == session.get('verification_code'):
        return jsonify({"status": "success", "message": "Verification successful!"})
    else:
        return jsonify({"status": "failed", "message": "Invalid verification code"}), 400
    
@app.route('/verify', methods=['GET'])
def verify_page():
    if 'email' in session:
        return render_template('verificationCode.html', email=session.get('email'))
    return redirect(url_for('signup'))  # Redirect if session expired




@app.route('/resendOtp', methods=['POST'])
def resend_otp():
    if 'email' not in session:
        return jsonify({"status": "failed", "message": "Session expired. Please sign up again."}), 400

    new_otp = generate_verification_code()
    session['verification_code'] = new_otp

    if send_verification_email(session['email'], new_otp):
        return jsonify({"status": "success", "message": "New OTP sent!"})
    else:
        return jsonify({"status": "failed", "message": "Failed to send email. Try again later."}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
