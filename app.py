from io import BytesIO
import matplotlib.pyplot as plt
import base64
from flask import Flask, render_template, jsonify, request
from players import Players

# Initialize the Flask application
app = Flask(__name__)

players_app = Players(num = 15)

# Define the route for the home/root URL
@app.route('/')
def home():
    return render_template('index.html', player_names=players_app.get_player_names())

@app.route('/similar-players', methods=["POST"])
def get_selected_player():
  data = request.get_json()
  player_name = data.get('text', '')
  similar_players = players_app.similar_to(player_name, 5)

  if similar_players is None:
        return jsonify({
            "error": "Player not found."
        }), 404

  return jsonify({
      "similar_players": similar_players
  })


@app.route("/compare", methods=["POST"])
def compare_players():
    data = request.get_json()

    player1 = data.get("player1", "")
    player2 = data.get("player2", "")

    stats1 = players_app.get_player_stats(player1)
    stats2 = players_app.get_player_stats(player2)

    graph = players_app.create_radar_chart(player1, player2)

    return jsonify({
        "player1": stats1,
        "player2": stats2,
        "graph": graph
    })

if __name__ == '__main__':
    # Run the local development server in debug mode
    app.run(debug=True)
