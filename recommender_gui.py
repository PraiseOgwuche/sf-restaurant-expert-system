import tkinter as tk
from tkinter import ttk, messagebox
import tempfile
import numpy as np
from pyswip.prolog import Prolog
from pyswip.easy import *
import re
import os
import sys

class RestaurantRecommenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SF Restaurant Recommender")
        self.root.geometry("600x500")
        self.root.configure(bg="#f5f5f5")  # Light gray background
        
        # Set up Prolog
        self.prolog = Prolog()
        self.retractall = Functor("retractall")
        self.known = Functor("known", 3)
        
        # Dictionary of restaurant responses with Google Maps links
        self.responses = {
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
        
        # Set up the welcome frame
        self.setup_welcome_frame()
        
        # Initialize KB
        self.initialize_kb()
        
        # Current question index
        self.current_question = 0
        
        # Track which questions have been asked
        self.questions_asked = []
        
        # Store user answers
        self.user_answers = {}
        
    def initialize_kb(self):
        # Load KB from file
        with open('kb.pl', 'r') as f:
            KB = f.read()
        
        # Create a temporary file with the KB in it
        (FD, name) = tempfile.mkstemp(suffix='.pl', text="True")
        with os.fdopen(FD, "w") as text_file:
            text_file.write(KB)
        
        # Consult the KB
        self.prolog.consult(name)
        
        # Remove the temporary file
        os.unlink(name)
        
        # Clear the previous knowledge
        call(self.retractall(self.known))
    
    def setup_welcome_frame(self):
        # Create welcome frame
        self.welcome_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.welcome_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_label = tk.Label(
            self.welcome_frame, 
            text="San Francisco Restaurant Recommender",
            font=("Arial", 18, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        header_label.pack(pady=(0, 20))
        
        # Welcome message
        welcome_text = "Welcome to the SF Restaurant Recommender!\n\nI'll ask you some questions to find the perfect restaurant for you based on your preferences."
        message_label = tk.Label(
            self.welcome_frame,
            text=welcome_text,
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#333333",
            wraplength=500,
            justify="center"
        )
        message_label.pack(pady=(0, 30))
        
        # First question
        self.first_question_label = tk.Label(
            self.welcome_frame,
            text="Are you currently in San Francisco?",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        self.first_question_label.pack(pady=(0, 20))
        
        # Buttons frame
        button_frame = tk.Frame(self.welcome_frame, bg="#f5f5f5")
        button_frame.pack(pady=10)
        
        # Yes Button
        yes_button = tk.Button(
            button_frame,
            text="Yes",
            font=("Arial", 12),
            command=lambda: self.answer_location_question(True),
            width=10,
            bg="#4CAF50",  # Green
            fg="white",
            relief=tk.RAISED,
            bd=0
        )
        yes_button.pack(side=tk.LEFT, padx=10)
        
        # No Button
        no_button = tk.Button(
            button_frame,
            text="No",
            font=("Arial", 12),
            command=lambda: self.answer_location_question(False),
            width=10,
            bg="#F44336",  # Red
            fg="white",
            relief=tk.RAISED,
            bd=0
        )
        no_button.pack(side=tk.LEFT, padx=10)
    
    def answer_location_question(self, is_in_sf):
        if is_in_sf:
            self.prolog.assertz("known(yes, location, san_francisco)")
            self.user_answers['location'] = 'san_francisco'
            # Clear welcome frame and set up question frame
            self.welcome_frame.pack_forget()
            self.setup_question_frame()
            self.ask_next_question()
        else:
            self.prolog.assertz("known(no, location, san_francisco)")
            self.user_answers['location'] = 'not_san_francisco'
            # Show message for non-SF users
            messagebox.showinfo(
                "Outside SF",
                "Sorry, we don't have any recommendations outside of San Francisco."
            )
    
    def setup_question_frame(self):
        # Create question frame
        self.question_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.question_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_label = tk.Label(
            self.question_frame, 
            text="Let's Find You a Restaurant",
            font=("Arial", 18, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        header_label.pack(pady=(0, 20))
        
        # Question text
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            wraplength=500
        )
        self.question_label.pack(pady=(0, 20))
        
        # Options frame
        self.options_frame = tk.Frame(self.question_frame, bg="#f5f5f5")
        self.options_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Result panel (hidden initially)
        self.result_frame = tk.Frame(self.root, bg="#f5f5f5")
        
    def ask_next_question(self):
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
        
        if self.current_question >= len(questions):
            # No more questions, show recommendation
            self.show_recommendation()
            return
        
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Get current question
        question = questions[self.current_question]
        self.question_label.config(text=question['text'])
        
        # Create radio buttons for options
        self.selected_option = tk.StringVar()
        for i, option in enumerate(question['options']):
            option_display = option.replace('_', ' ').capitalize()
            radio_btn = tk.Radiobutton(
                self.options_frame,
                text=option_display,
                variable=self.selected_option,
                value=option,
                font=("Arial", 12),
                bg="#f5f5f5",
                activebackground="#f5f5f5",
                selectcolor="#e0e0e0"
            )
            radio_btn.pack(anchor='w', pady=5)
        
        # Next button
        next_button = tk.Button(
            self.options_frame,
            text="Next",
            font=("Arial", 12),
            command=lambda: self.answer_question(question['attribute']),
            width=10,
            bg="#2196F3",  # Blue
            fg="white",
            relief=tk.RAISED,
            bd=0
        )
        next_button.pack(pady=20)
    
    def answer_question(self, attribute):
        value = self.selected_option.get()
        if not value:
            messagebox.showwarning("Selection Required", "Please select an option before continuing.")
            return
        
        # Store the answer
        self.user_answers[attribute] = value
        self.prolog.assertz(f"known(yes, {attribute}, {value})")
        
        # Check if this answer triggers a recommendation
        restaurant = list(self.prolog.query("restaurant(X)", maxresult=1))
        
        if restaurant and restaurant[0]['X'] != "ask_others":
            # We have a recommendation, show it
            self.show_recommendation(restaurant[0]['X'])
            return
        
        # Move to next question
        self.current_question += 1
        self.ask_next_question()
    
    def show_recommendation(self, restaurant_name=None):
        # Hide question frame
        self.question_frame.pack_forget()
        
        # Show result frame
        self.result_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if restaurant_name:
            restaurant_info = self.responses.get(restaurant_name, restaurant_name)
            
            # Result title
            result_label = tk.Label(
                self.result_frame,
                text="Your Restaurant Recommendation",
                font=("Arial", 18, "bold"),
                bg="#f5f5f5",
                fg="#333333"
            )
            result_label.pack(pady=(0, 20))
            
            # Restaurant name and info
            restaurant_label = tk.Label(
                self.result_frame,
                text=restaurant_info,
                font=("Arial", 14),
                bg="#f5f5f5",
                fg="#333333",
                wraplength=500
            )
            restaurant_label.pack(pady=(0, 30))
            
            # Add hyperlink-style formatting
            restaurant_label.config(fg="blue", cursor="hand2")
            restaurant_label.bind("<Button-1>", lambda e: self.open_url(restaurant_info.split(": ")[1]))
            
            # Instructions for link
            instructions = tk.Label(
                self.result_frame,
                text="(Click the link above to view the location on Google Maps)",
                font=("Arial", 10, "italic"),
                bg="#f5f5f5",
                fg="#666666"
            )
            instructions.pack(pady=(0, 20))
        else:
            # No recommendation found
            result_label = tk.Label(
                self.result_frame,
                text="No Matching Restaurants",
                font=("Arial", 18, "bold"),
                bg="#f5f5f5",
                fg="#333333"
            )
            result_label.pack(pady=(0, 20))
            
            # Message
            no_result_label = tk.Label(
                self.result_frame,
                text="Sorry, we don't have any recommendations based on your preferences, but you can ask others for suggestions.",
                font=("Arial", 14),
                bg="#f5f5f5",
                fg="#333333",
                wraplength=500
            )
            no_result_label.pack(pady=(0, 30))
        
        # Restart button
        restart_button = tk.Button(
            self.result_frame,
            text="Start Over",
            font=("Arial", 12),
            command=self.restart,
            width=15,
            bg="#673AB7",  # Purple
            fg="white",
            relief=tk.RAISED,
            bd=0
        )
        restart_button.pack(pady=20)
    
    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
    
    def restart(self):
        # Hide result frame
        self.result_frame.pack_forget()
        
        # Reset variables
        self.current_question = 0
        self.questions_asked = []
        self.user_answers = {}
        
        # Re-initialize KB
        self.initialize_kb()
        
        # Show welcome frame again
        self.setup_welcome_frame()

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantRecommenderGUI(root)
    root.mainloop()