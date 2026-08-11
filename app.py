from io import BytesIO
import matplotlib.pyplot as plt
import base64
from flask import Flask, render_template, jsonify, request
from players import Players

# Initialize the Flask application
app = Flask(__name__)

players_app = None

# Define the route for the home/root URL
@app.route('/')
def home():
    return render_template('index.html')


@app.route("/heatmap")
def heatmap():
    num_players = request.args.get("num-players")

    if num_players is None:
        return "Please select the number of players first.", 400

    try:
        num_players = int(num_players)
    except (TypeError, ValueError):
        return "Invalid number of players.", 400

    if num_players < 15 or num_players > 150:
        return "Number of players must be between 15 and 150.", 400

    players_app = Players(num=num_players)

    image = players_app.comparism()

    return render_template(
        "heatmap.html",
        heatmap=image
    )

@app.route('/num-players', methods=["POST"])
def get_players():
    data = request.get_json()

    try:
        num_players = int(data.get("num-players"))
    except (TypeError, ValueError):
        return jsonify({
            "error": "Number of players must be an integer."
        }), 400

    if num_players < 15 or num_players > 150:
        return jsonify({
            "error": "Number of players must be between 15 and 150."
        }), 400

    num_players = data.get("num-players")

    players_app = Players(num=num_players)

    return jsonify({
        "player_names": players_app.get_player_names(),
        # "num_players": num_players
    })

@app.route('/similar-players', methods=["POST"])
def get_selected_player():
    data = request.get_json()

    player_name = data.get("player", "")
    num = data.get("num", 3)
    num_players = data.get("num-players")



    if num_players is None:
        return jsonify({
            "error": "Please select the number of players first."
        }), 400

    players_app = Players(num=num_players)

    similar_players = players_app.similar_to(
        player_name,
        num
    )

    return jsonify({
        "similar_players": similar_players
    })

@app.route("/compare", methods=["POST"])
def compare_players():
    data = request.get_json()

    player1 = data.get("player1", "")
    player2 = data.get("player2", "")

    num_players = data.get("num-players")
    if num_players is None:
        return jsonify({
            "error": "Please select the number of players first."
        }), 400

    players_app = Players(num=num_players)

    stats1 = players_app.get_player_stats(player1)
    stats2 = players_app.get_player_stats(player2)

    graph = players_app.create_radar_chart(
        player1,
        player2
    )

    return jsonify({
        "player1": stats1,
        "player2": stats2,
        "graph": graph
    })


if __name__ == '__main__':
    # Run the local development server in debug mode
    app.run(debug=True, port=8080)
