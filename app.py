from flask import Flask, render_template, jsonify, request
from players import Players

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home/root URL
@app.route('/')
def home():
    players_app = Players(num = 15)
    return render_template('index.html', player_names=players_app.get_player_names())

@app.route('/process', methods=["POST"])
def get_selected_player():
  data = request.get_json()
  player_name = data.get('text', '')

  
if __name__ == '__main__':
    # Run the local development server in debug mode
    app.run(debug=True)
