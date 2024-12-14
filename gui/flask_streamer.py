# File: app.py
import time
from flask import Flask, Response, jsonify


# Initialize the Flask app
app = Flask(__name__)


@app.route("/generate", methods=["POST"])
def generate():
    try:

        def events():
            count = 0
            a = ""
            while count < 10:
                a = "new line" + str(count) + " "
                yield a
                time.sleep(1)  # an artificial delay
                count += 1

        # Use Flask's streaming Response
        return Response(events(), content_type="text/plain")

    except Exception as e:
        # Handle exceptions gracefully
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)
