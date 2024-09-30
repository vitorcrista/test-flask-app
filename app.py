import os
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Path to the JSON file to store user IDs
JSON_FILE_PATH = "user_ids.json"


# Helper function to read user IDs from JSON file
def read_user_ids():
    if not os.path.exists(JSON_FILE_PATH):
        return []
    with open(JSON_FILE_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_user_ids(user_ids):
    with open(JSON_FILE_PATH, "w") as file:
        json.dump(user_ids, file)


@app.route("/save_user_id", methods=["POST"])
def save_user_id():
    data = request.get_json()
    uid = data.get("user_id")

    # Read the existing user IDs
    user_ids = read_user_ids()

    # Append the new user ID to the list
    user_ids.append(uid)

    # Save the updated list back to the JSON file
    save_user_ids(user_ids)

    print("Saving user ID in JSON file.")
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

    # Read the user IDs from the JSON file
    user_ids = read_user_ids()

    print(f"user_ids={user_ids}")

    if len(user_ids) == 0:
        print("No user ID was received and saved in the JSON file")
        return render_template("400.html")

    payload = {
        "code": code,
        "user_id": user_ids[0],  # Use the first user ID (or modify as per your need)
    }

    print(f"payload ={payload}")

    try:
        # Call the Google web app's endpoint
        response = requests.post("https://chat4elderly-service-v0-69627867300.europe-southwest1.run.app/start-oauth", json=payload)

        print(f"response.text = {response.text}")

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
    save_user_ids([])
    return render_template("200.html")


@app.route("/health", methods=["GET"])
def health_check():
    return (
        jsonify(
            {
                "status": "OK",
                "message": "Service is running",
                "uptime": "100%",  # Example, you can track uptime if needed
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
