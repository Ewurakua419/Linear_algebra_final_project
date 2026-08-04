from flask import Flask, render_template
from project import player_names

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home/root URL
@app.route('/')
def home():
    return render_template('index.html', player_names=player_names)

if __name__ == '__main__':
    # Run the local development server in debug mode
    app.run(debug=True)
