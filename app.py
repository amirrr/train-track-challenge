# Description: This file contains the Flask API for the Train Track project.

# Import the required libraries
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from traintrack import TrainTrack

import json
import argparse

import os


app = Flask(__name__)
api = Api(app)


@app.route("/", methods=["GET"])
def index():
    return "Welcome to the Train Track API!"


@app.route("/edges", methods=["POST", "GET"])
def get_edges():
    if request.method == "POST":
        json_data = request.get_json()
        train_track = TrainTrack(json_data)
    edges = train_track.get_edges()
    return jsonify(edges)


@app.route("/occupied_edges", methods=["POST"])
def get_occupied_edges():
    if request.method == "POST":
        json_data = request.get_json()
        train_track = TrainTrack(json_data)
    edges = train_track.get_occupied_edges()
    return jsonify(edges)


@app.route("/unoccupied_edges", methods=["POST", "GET"])
def get_unoccupied_edges():
    if request.method == "POST":
        json_data = request.get_json()
        train_track = TrainTrack(json_data)
    edges = train_track.get_unoccupied_edges()
    return jsonify(edges)


@app.route("/interested_edges", methods=["POST", "GET"])
def get_interested_edges():
    if request.method == "POST":
        json_data = request.get_json()
        train_track = TrainTrack(json_data)
    edges = train_track.get_interested_edges()
    return jsonify(edges)


@app.route("/connectedness", methods=["POST", "GET"])
def check_connectedness():
    if request.method == "POST":
        json_data = request.get_json()
        train_track = TrainTrack(json_data)
    connected = train_track.check_graph_connectedness()
    return jsonify(connected)


@app.route("/possible_to_travel", methods=["POST", "GET"])
def check_possible_to_travel():
    if request.method == "POST":
        json_data = request.get_json()
        train_track = TrainTrack(json_data)
    possible = train_track.is_it_possible_to_travle()
    return jsonify(possible)


@app.route("/load_data", methods=["POST"])
def load_data():
    json_string = request.get_json()
    try:
        data = json.loads(json_string)
        train_track = TrainTrack(data)
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "error", "message": "Invalid JSON data"})
