# Description: This file contains the Flask API for the Train Track project.

# Import the required libraries
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_restful import Resource, Api

from traintrack import TrainTrack

import json
import argparse
import traceback
import os


app = Flask(__name__, template_folder="templates")
api = Api(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/check_conflicts", methods=["POST"])
def check_possible_to_travel():
    json_string = request.get_json()
    try:
        train_track = TrainTrack(json_string)
        if train_track.is_it_possible_to_travle():
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})


@app.route("/upload_json", methods=["POST"])
def upload_json():
    if "json_file" in request.files:
        json_file = request.files["json_file"]
        # Process the uploaded JSON file here

        # Example: Read the contents of the file
        file_contents = json_file.read()
        t = TrainTrack(json.loads(file_contents))
        pic_url = t.plot_web_graph()
        is_avaialble = t.is_it_possible_to_travle()
        return render_template(
            "result.html", picture_url=pic_url, is_available=is_avaialble
        )

    return "File upload failed."


@app.route("/process_json", methods=["POST"])
def process_json():
    """
    Processes JSON data received via POST request and returns a rendered template with the result.

    Returns:
        str: A rendered HTML template with the result of processing the JSON data.
    """
    if "json_input" in request.form:
        json_data = request.form["json_input"]

        try:
            # You can parse and process the JSON data here
            parsed_data = json.loads(json_data)
            t = TrainTrack(parsed_data)
            pic_url = t.plot_web_graph()
            is_avaialble = t.is_it_possible_to_travle()
            return render_template(
                "result.html", picture_url=pic_url, is_available=is_avaialble
            )

        except Exception as e:
            return f"JSON parsing error: {str(e)}"

    return "No JSON data provided."


@app.route("/test_plot", methods=["GET"])
def test_plot():
    json_string = """
        {
            "station_graph": [
                {"start": "Station West", "end": "Entry Signal West" },
                {"start": "Entry Signal West", "end": "Point 1" },
                {"start": "Point 1", "end": "Exit Signal West 1" },
                {"start": "Point 1", "end": "Exit Signal West 2" },
                {"start": "Exit Signal West 1", "end": "Exit Signal East 1" },
                {"start": "Exit Signal West 2", "end": "Exit Signal East 2" },
                {"start": "Exit Signal East 1", "end": "Point 2" },
                {"start": "Exit Signal East 2", "end": "Point 2" },
                {"start": "Point 2", "end": "Entry Signal East" },
                {"start": "Entry Signal East", "end": "Station East" }
            ],
            "routes": [
                {"start": "Entry Signal West", "end": "Exit Signal East 1", "occupied": false },
                {"start": "Entry Signal West", "end": "Exit Signal East 2", "occupied": false },
                {"start": "Exit Signal East 1", "end": "Station East", "occupied": false },
                {"start": "Exit Signal East 2", "end": "Station East", "occupied": false },
                {"start": "Entry Signal East", "end": "Exit Signal West 1", "occupied": false },
                {"start": "Entry Signal East", "end": "Exit Signal West 2", "occupied": false },
                {"start": "Point 1", "end": "Exit Signal East 1", "occupied": true },
                {"start": "Exit Signal West 2", "end": "Station West", "occupied": false }
            ],
            "check_route": {"start": "Exit Signal East 1", "end": "Point 2" }
        }
        """

    t = TrainTrack(json.loads(json_string))
    pic_url = t.plot_web_graph()
    is_avaialble = t.is_it_possible_to_travle()
    return render_template(
        "result.html", picture_url=pic_url, is_available=is_avaialble
    )
    # return redirect(url_for('display_picture', picture_url=pic_url))


if __name__ == "__main__":
    app.run(debug=True)

