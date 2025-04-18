from flask import Flask, render_template, request, redirect, url_for, session
import tempfile
import numpy as np
from pyswip.prolog import Prolog
from pyswip.easy import *
import re
import os
import sys

app = Flask(__name__)
app.secret_key = 'sf_restaurant_recommender'  # Needed for session management

# Set up Prolog
prolog = Prolog()
retractall = Functor("retractall")
known = Functor("known", 3)

# Dictionary of restaurant responses with Google Maps links
responses = {
    'nopalito': "Nopalito: https://goo.gl/maps/Lh23H8qdJZbB3KZYA",
    'zuni_cafe': "Zuni Café: https://goo.gl/maps/Q8nHYHJtHnRiNsus6",
    'farmhouse_kitchen': "Farmhouse Kitchen Thai: https://goo.gl/maps/u5v5wAA3ZPKsS7e47",
    'souvla': "Souvla: https://goo.gl/maps/ngnffrQ13SnGjJWY8",
    'la_taqueria': "La Taqueria: https://goo.gl/maps/qBTiL76dbA7dknLG6",
    'burma_superstar': "Burma Superstar: https://goo.gl/maps/vdKHLEESKZwCVQmP7",
    'liholiho_yacht_club': "Liholiho Yacht Club: https://goo.gl/maps/BJuEiNhLeJSPSvyC8",
    'nopa': "Nopa: https://goo.gl/maps/PVsUhTC9GJgfJbGr5",
    'foreign_cinema': "Foreign Cinema: https://goo.gl/maps/Ay55yVoVXYQ2RCJ86",
    'hog_island_oyster': "Hog Island Oyster Co: https://goo.gl/maps/KSLfpN9J8mCnE6U16",
}

# Questions and their options
questions = [
    {
        'text': "What kind of food are you in the mood for today?",
        'attribute': 'cuisine',
        'options': ["american", "chinese", "italian", "japanese", "mexican", "thai", "burmese", "greek", "hawaiian", "seafood"]
    },
    {
        'text': "Do you have any specific dietary requirements or preferences?",
        'attribute': 'diet',
        'options': ["standard", "vegetarian_options", "vegan_options", "gluten_free", "pescatarian", "halal"]
    },
    {
        'text': "What price range are you comfortable with for this meal?",
        'attribute': 'price',
        'options': ["affordable", "moderate", "expensive"]
    },
    {
        'text': "What kind of dining atmosphere would you prefer?",
        'attribute': 'atmosphere',
        'options': ["casual", "upscale", "cozy", "trendy", "quiet"]
    },
    {
        'text': "How far are you willing to travel from Minerva residence?",
        'attribute': 'distance',
        'options': ["walking_distance", "muni_required", "bart_required"]
    },
    {
        'text': "What noise level would be ideal for your dining experience?",
        'attribute': 'noise',
        'options': ["quiet", "moderate", "lively"]
    },
    {
        'text': "Do you have a preference for indoor or outdoor seating?",
        'attribute': 'seating',
        'options': ["indoor", "outdoor", "indoor_outdoor"]
    }
]

def initialize_kb():
    # Load KB from file
    with open('kb.pl', 'r') as f:
        KB = f.read()
    
    # Create a temporary file with the KB in it
    (FD, name) = tempfile.mkstemp(suffix='.pl', text="True")
    with os.fdopen(FD, "w") as text_file:
        text_file.write(KB)
    
    # Consult the KB
    prolog.consult(name)
    
    # Remove the temporary file
    os.unlink(name)
    
    # Clear the previous knowledge
    call(retractall(known))

@app.route('/')
def index():
    # Initialize or reset the session
    session.clear()
    initialize_kb()
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def location():
    is_in_sf = request.form.get('location') == 'yes'
    
    if is_in_sf:
        prolog.assertz("known(yes, location, san_francisco)")
        session['answers'] = {'location': 'san_francisco'}
        session['current_question'] = 0
        return redirect(url_for('question'))
    else:
        prolog.assertz("known(no, location, san_francisco)")
        return render_template('no_results.html', message="Sorry, we don't have any recommendations outside of San Francisco.")

@app.route('/question', methods=['GET', 'POST'])
def question():
    # Get the current answers and question index
    answers = session.get('answers', {'location': 'san_francisco'})
    current_question = session.get('current_question', 0)
    
    if current_question >= len(questions):
        # No more questions, show recommendation
        return redirect(url_for('recommendation'))
    
    if request.method == 'POST':
        # Process the answer
        attribute = questions[current_question]['attribute']
        value = request.form.get('option')
        
        if not value:
            return render_template('question.html', 
                                  question=questions[current_question],
                                  error="Please select an option")
        
        # Store the answer
        answers[attribute] = value
        session['answers'] = answers
        
        # Add to Prolog knowledge base
        prolog.assertz(f"known(yes, {attribute}, {value})")
        
        # Check if this answer triggers a recommendation
        restaurant = list(prolog.query("restaurant(X)", maxresult=1))
        
        if restaurant and restaurant[0]['X'] != "ask_others":
            # We have a recommendation, show it
            return redirect(url_for('recommendation'))
        
        # Move to next question
        session['current_question'] = current_question + 1
        return redirect(url_for('question'))
    
    # GET request, show the current question
    return render_template('question.html', question=questions[current_question])

@app.route('/recommendation')
def recommendation():
    restaurant = list(prolog.query("restaurant(X)", maxresult=1))
    
    if restaurant and restaurant[0]['X'] != "ask_others":
        restaurant_name = restaurant[0]['X']
        restaurant_info = responses.get(restaurant_name, restaurant_name)
        return render_template('recommendation.html', restaurant=restaurant_info)
    else:
        return render_template('no_results.html', 
                              message="Sorry, we don't have any recommendations based on your preferences, but you can ask others for suggestions.")

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create template files
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>SF Restaurant Recommender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        p {
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 20px;
        }
        .btn {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 16px;
            margin: 10px;
            cursor: pointer;
            border: none;
        }
        .btn-no {
            background-color: #F44336;
        }
        .btn-container {
            text-align: center;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>San Francisco Restaurant Recommender</h1>
        <p>Welcome to the SF Restaurant Recommender! I'll ask you some questions to find the perfect restaurant for you based on your preferences.</p>
        
        <form action="/location" method="post">
            <h2>Are you currently in San Francisco?</h2>
            <div class="btn-container">
                <button type="submit" name="location" value="yes" class="btn">Yes</button>
                <button type="submit" name="location" value="no" class="btn btn-no">No</button>
            </div>
        </form>
    </div>
</body>
</html>
        ''')
    
    with open('templates/question.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>SF Restaurant Recommender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .option {
            margin: 10px 0;
        }
        label {
            font-size: 16px;
            cursor: pointer;
        }
        .submit-btn {
            background-color: #2196F3;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
        }
        .error {
            color: red;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Let's Find You a Restaurant</h1>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form action="/question" method="post">
            <h2>{{ question.text }}</h2>
            
            {% for option in question.options %}
            <div class="option">
                <input type="radio" id="{{ option }}" name="option" value="{{ option }}">
                <label for="{{ option }}">{{ option.replace('_', ' ').capitalize() }}</label>
            </div>
            {% endfor %}
            
            <button type="submit" class="submit-btn">Next</button>
        </form>
    </div>
</body>
</html>
        ''')
    
    with open('templates/recommendation.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>SF Restaurant Recommender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .recommendation {
            font-size: 18px;
            margin: 30px 0;
        }
        .restaurant-link {
            color: #2196F3;
            text-decoration: none;
        }
        .restaurant-link:hover {
            text-decoration: underline;
        }
        .note {
            font-style: italic;
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .restart-btn {
            background-color: #673AB7;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Your Restaurant Recommendation</h1>
        
        <div class="recommendation">
            {% set parts = restaurant.split(': ', 1) %}
            <a href="{{ parts[1] }}" class="restaurant-link" target="_blank">{{ parts[0] }}</a>
        </div>
        
        <div class="note">(Click the restaurant name above to view the location on Google Maps)</div>
        
        <a href="/" class="restart-btn">Start Over</a>
    </div>
</body>
</html>
        ''')
    
    with open('templates/no_results.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>SF Restaurant Recommender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #333;
        }
        p {
            font-size: 18px;
            margin: 30px 0;
        }
        .restart-btn {
            background-color: #673AB7;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>No Matching Restaurants</h1>
        
        <p>{{ message }}</p>
        
        <a href="/" class="restart-btn">Start Over</a>
    </div>
</body>
</html>
        ''')
    
    app.run(debug=True, host='0.0.0.0', port=5000)