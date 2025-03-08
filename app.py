from flask import Flask, redirect, render_template, request, jsonify, session, url_for, json

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/signup')
def login():
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)