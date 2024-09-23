from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/fitbit/callback", methods=["GET"])
def fitbit():
    code = request.args.get('code')
    state = request.args.get('state')

    #sending the code back to the main server
    
    if not code or not state:
        return render_template('400.html'), 400
    
    return render_template('200.html'), 200



@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
