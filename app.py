from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


@app.route("/fitbit/callback", methods=["GET"])
def fitbit():
    code = request.args.get("code")
    state = request.args.get("state")

    
    # sending the code back to the main server

    if not code or not state:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error 404</title>
        </head>
        <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: Arial, sans-serif;">
            <div style="text-align: center;">
                <h1>Page Not Found</h1>
                <p>The requested resource was not found.</p>
            </div>
        </body>
        </html>
        """

    # Send the code back to the main server
    main_server_url = "http://34.175.7.148:5000/receive_code"  # Change to your main server's URL
    response = requests.post(main_server_url, json={"code": code, "state": state})
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Authorization Successful</title> 
        <meta name="code" content="{code}">

    </head>
    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: Arial, sans-serif;">
        <div style="text-align: center;">
            <h1>Authorization Successful!</h1>
            <p>You can now close this window.</p>
        </div>
    </body>
    </html>
    """


@app.errorhandler(404)
def not_found(e):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Error 404</title>
    </head>
    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: Arial, sans-serif;">
        <div style="text-align: center;">
            <h1>Page Not Found</h1>
            <p>The requested resource was not found.</p>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run()
