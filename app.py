from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

app.secret_key = "your_secret_key"  # Required for session to work


IDS = []

@app.route("/save_user_id", methods=["POST"])
def save_user_id():
    data = request.get_json()
    uid = data.get("user_id")
    session['user_id'] = uid  # Save user_id to session
    print("saving user id in session.")
    return jsonify(message="Success!"), 200

@app.route("/fitbit/callback", methods=["GET"])
def fitbit():
    code = request.args.get("code")
    state = request.args.get("state")
    code_verifier = request.args.get("code_verifier")
    if not code or not state:
        return render_template("400.html")

    # call endpoint on google web app to start the auth flow
    print(
        f"call endpoint on google web app to start the auth flow and send the code => {code} \
        and the state => {state} and the code_verifier => {code_verifier}"
    )
    
    user_id = session.get("user_id")
    if not user_id:
        print("No user id was saved in session")
        return render_template("400.html")
    
    payload = {
        "code": code,
        "user_id": user_id
    }

    try:
        # Call the Google web app's endpoint
        response = requests.post("http://34.175.7.148:5000/start-oauth", json=payload)
        
        print(response.text)

        # Check for success or handle failure
        if response.status_code == 200 or response.status_code == 201:
            print(f"Successfully sent the code and state. Response: {response.json()}")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            return render_template("400.html")

    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template("500.html")

    # return html page
    session.pop('user_id', None)
    return render_template("200.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
