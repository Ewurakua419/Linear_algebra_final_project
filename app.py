from flask import Flask, render_template, jsonify, request
from players import Players

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home/root URL
players_app = Players(num = 15)

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


@app.route('/stats', methods=["POST"])
def get_stats():

    data = request.get_json()
    player_name = data.get("player", "")

    stats = players_app.get_player_stats(player_name)

    if stats is None:
        return jsonify({
            "error": "Player not found"
        }), 404

    return jsonify(stats)


if __name__ == '__main__':
    # Run the local development server in debug mode
    app.run(debug=True)
