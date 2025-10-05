#!/usr/bin/env python3
"""
Space Quiz Application - ISS Cupola & NBL Training Quiz
========================================================

A comprehensive quiz application covering the International Space Station's Cupola module
and NASA's Neutral Buoyancy Laboratory (NBL) training facility.

Features:
- Multiple choice and True/False questions
- Different difficulty levels (Basic, Intermediate, Advanced, Expert)
- Topic selection (Cupola, NBL, or Mixed)
- Score tracking and detailed results
- Export functionality
- Professional GUI interface

Author: AI Assistant
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime

# Define the Cupola questions
cupola_questions = [
    # Basic Questions (1-25)
    {
        "question": "What is the Cupola's main role on the ISS?",
        "options": ["Propulsion system", "Crew sleeping area", "Observation and robotics control", "Laboratory for experiments"],
        "correct": 2,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The Cupola is attached to the Tranquility (Node 3) module.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "How many windows does the Cupola have?",
        "options": ["4", "5", "7", "9"],
        "correct": 2,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "Which space agency primarily designed the Cupola?",
        "options": ["NASA", "Roscosmos", "ESA", "JAXA"],
        "correct": 2,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The Cupola provides a 360-degree view of space.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "What shape is the Cupola module?",
        "options": ["Cylindrical", "Spherical", "Octagonal", "Rectangular"],
        "correct": 2,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The Cupola was launched in 2010.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "Which Space Shuttle mission delivered the Cupola to the ISS?",
        "options": ["STS-119", "STS-130", "STS-131", "STS-133"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The Cupola's windows are made of ordinary glass.",
        "options": ["True", "False"],
        "correct": 1,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "What is the Cupola's approximate diameter?",
        "options": ["1 meter", "3 meters", "5 meters", "7 meters"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "Astronauts use the Cupola for Earth photography.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "The Cupola weighs about how much?",
        "options": ["1 ton", "1.8 tons", "3 tons", "5 tons"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The Cupola is the largest continuous window in space.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "Who was the first astronaut to enter the Cupola?",
        "options": ["Scott Kelly", "Luca Parmitano", "Peggy Whitson", "Chris Hadfield"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The Cupola helps monitor spacewalks.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    # Intermediate Questions (26-50)
    {
        "question": "What material are the Cupola's windows primarily made of?",
        "options": ["Acrylic", "Fused silica", "Tempered glass", "Polycarbonate"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The Cupola includes protective shutters for debris protection.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    {
        "question": "How long is each Cupola window pane?",
        "options": ["0.5 meters", "0.8 meters", "1.2 meters", "1.5 meters"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The Cupola was originally planned for the ISS in the 1990s.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    {
        "question": "What is the thickness of the Cupola's inner window layer?",
        "options": ["2 cm", "4 cm", "6 cm", "8 cm"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The Cupola supports the Mobile Servicing System (Canadarm2).",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    {
        "question": "Which company manufactured the Cupola?",
        "options": ["Boeing", "Thales Alenia Space", "Lockheed Martin", "Airbus"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The Cupola's installation required three EVAs.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    {
        "question": "What gas is used in the Cupola's window interlayers?",
        "options": ["Oxygen", "Argon", "Nitrogen", "Helium"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The Cupola enhances crew psychological well-being.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    # Advanced Questions (51-75)
    {
        "question": "What engineering challenge did the Cupola's windows face?",
        "options": ["Thermal expansion", "Hypergolic fuel exposure", "Radiation hardening", "Vacuum sealing only"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Advanced"
    },
    {
        "question": "The Cupola uses a nadir window for ISS assembly views.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Advanced"
    },
    {
        "question": "How many redundant seals does each Cupola window have?",
        "options": ["1", "2", "3", "4"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Advanced"
    },
    {
        "question": "The Cupola's shutters are manually operated from inside.",
        "options": ["True", "False"],
        "correct": 1,
        "type": "True/False",
        "difficulty": "Advanced"
    },
    {
        "question": "What is the Cupola's thermal protection system rated for?",
        "options": ["-150°C to +120°C", "-200°C to +100°C", "-100°C to +200°C", "0°C to +50°C"],
        "correct": 0,
        "type": "MCQ",
        "difficulty": "Advanced"
    },
    {
        "question": "Finite element analysis was used in Cupola design for stress.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Advanced"
    },
    # Expert Questions (76-100)
    {
        "question": "The Cupola's window stress analysis used what model?",
        "options": ["Finite element", "Analytical only", "CFD", "Monte Carlo"],
        "correct": 0,
        "type": "MCQ",
        "difficulty": "Expert"
    },
    {
        "question": "The Cupola's ballistic limit equations predict debris penetration.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Expert"
    },
    {
        "question": "In hypervelocity impact tests, Cupola glass withstands up to what velocity?",
        "options": ["5 km/s", "10 km/s", "15 km/s", "20 km/s"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Expert"
    },
    {
        "question": "The Cupola's design incorporates Whipple shielding principles.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Expert"
    }
]

# Define the NBL questions
nbl_questions = [
    # Basic Questions (1-25)
    {
        "question": "What does NBL stand for?",
        "options": ["National Basketball League", "Neutral Buoyancy Laboratory", "NASA Buoyancy Lab", "Neutral Body Lab"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The NBL is located at Johnson Space Center.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "What is the NBL's primary purpose?",
        "options": ["Swimming pool", "Spacewalk training", "Fish research", "Water recycling"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "How large is the NBL pool?",
        "options": ["1 million gallons", "6.2 million gallons", "10 million gallons", "20 million gallons"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The NBL simulates zero gravity using buoyancy.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "Where is the NBL situated?",
        "options": ["Florida", "Houston, Texas", "California", "Alabama"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The NBL opened in 1997.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "What is the pool's depth?",
        "options": ["20 feet", "30 feet", "40 feet", "50 feet"],
        "correct": 2,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "Astronauts wear spacesuits in the NBL.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "The NBL is part of what facility?",
        "options": ["Kennedy Space Center", "Sonny Carter Training Facility", "Goddard", "Ames"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The NBL uses fresh water only.",
        "options": ["True", "False"],
        "correct": 1,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "How long is the NBL pool?",
        "options": ["100 feet", "202 feet", "300 feet", "400 feet"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "Divers assist astronauts in the NBL.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    {
        "question": "The NBL trains for what type of activities?",
        "options": ["Only launches", "EVAs (spacewalks)", "Orbit burns", "Docking"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Basic"
    },
    {
        "question": "The NBL has an on-site hyperbaric chamber.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Basic"
    },
    # Intermediate Questions (26-50)
    {
        "question": "From whom did NASA buy the NBL building?",
        "options": ["Boeing", "McDonnell Douglas", "Lockheed", "General Dynamics"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The NBL can simulate partial gravity.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    {
        "question": "How many support divers are typically in an NBL session?",
        "options": ["5–10", "10–20", "20–30", "50+"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The NBL has multiple control rooms.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    {
        "question": "What is the NBL's water turnover time?",
        "options": ["12 hours", "19.6 hours", "24 hours", "48 hours"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The NBL uses SCUBA for all dives.",
        "options": ["True", "False"],
        "correct": 1,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    {
        "question": "The NBL dedicated date was?",
        "options": ["1996", "May 1997", "1998", "2000"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The NBL trains for Hubble repairs.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    {
        "question": "What is the NBL's storage capacity for hardware?",
        "options": ["Indoor/outdoor areas", "Only indoor", "Garage only", "None"],
        "correct": 0,
        "type": "MCQ",
        "difficulty": "Intermediate"
    },
    {
        "question": "The NBL pool temperature is 88°F.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Intermediate"
    },
    # Advanced Questions (51-75)
    {
        "question": "The NBL's buoyancy adjustment uses what weights?",
        "options": ["Lead foam", "Steel plates", "Sandbags", "Air bladders"],
        "correct": 0,
        "type": "MCQ",
        "difficulty": "Advanced"
    },
    {
        "question": "The NBL simulates 1/6th gravity for lunar walks.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Advanced"
    },
    {
        "question": "What is the NBL's filtration system rated for?",
        "options": ["100 microns", "10 microns", "1 micron", "0.1 micron"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Advanced"
    },
    {
        "question": "The NBL's control rooms use fiber optics for data.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Advanced"
    },
    {
        "question": "The NBL's pH is maintained at?",
        "options": ["6.5–7.0", "7.0–7.5", "7.5–8.0", "8.0–8.5"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Advanced"
    },
    {
        "question": "Acoustic telemetry is used in NBL comms.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Advanced"
    },
    # Expert Questions (76-100)
    {
        "question": "The NBL's neutral buoyancy precision is within what %?",
        "options": ["1%", "0.1%", "0.01%", "10%"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Expert"
    },
    {
        "question": "The NBL uses particle image velocimetry for flow studies.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Expert"
    },
    {
        "question": "In expert training, NBL simulates what g-force?",
        "options": ["10^-6 g", "Variable 0–1 g", "1 g only", "9.8 g"],
        "correct": 1,
        "type": "MCQ",
        "difficulty": "Expert"
    },
    {
        "question": "The NBL's finite element models predict suit drag.",
        "options": ["True", "False"],
        "correct": 0,
        "type": "True/False",
        "difficulty": "Expert"
    }
]


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Quiz Application - Cupola & NBL")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')

        # Quiz state variables
        self.current_question = 0
        self.score = 0
        self.selected_topic = None
        self.questions = []
        self.user_answers = []
        self.quiz_completed = False

        # Create main UI
        self.create_main_menu()

    def create_main_menu(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = tk.Label(
            self.root, 
            text="🚀 SPACE QUIZ APPLICATION 🚀", 
            font=("Arial", 24, "bold"), 
            fg="#ffffff", 
            bg="#1a1a2e"
        )
        title_label.pack(pady=30)

        # Subtitle
        subtitle_label = tk.Label(
            self.root, 
            text="Test your knowledge about the ISS Cupola and Neutral Buoyancy Laboratory", 
            font=("Arial", 12), 
            fg="#a0a0a0", 
            bg="#1a1a2e"
        )
        subtitle_label.pack(pady=10)

        # Topic selection frame
        topic_frame = tk.Frame(self.root, bg="#1a1a2e")
        topic_frame.pack(pady=40)

        tk.Label(
            topic_frame, 
            text="Choose your topic:", 
            font=("Arial", 16, "bold"), 
            fg="#ffffff", 
            bg="#1a1a2e"
        ).pack(pady=10)

        # Topic buttons
        cupola_btn = tk.Button(
            topic_frame, 
            text="🔭 ISS CUPOLA QUIZ", 
            font=("Arial", 14, "bold"), 
            bg="#0f3460", 
            fg="#ffffff", 
            padx=20, 
            pady=10,
            command=lambda: self.start_quiz("cupola")
        )
        cupola_btn.pack(pady=10)

        nbl_btn = tk.Button(
            topic_frame, 
            text="🌊 NBL TRAINING QUIZ", 
            font=("Arial", 14, "bold"), 
            bg="#16537e", 
            fg="#ffffff", 
            padx=20, 
            pady=10,
            command=lambda: self.start_quiz("nbl")
        )
        nbl_btn.pack(pady=10)

        mixed_btn = tk.Button(
            topic_frame, 
            text="🚀 MIXED TOPICS QUIZ", 
            font=("Arial", 14, "bold"), 
            bg="#533483", 
            fg="#ffffff", 
            padx=20, 
            pady=10,
            command=lambda: self.start_quiz("mixed")
        )
        mixed_btn.pack(pady=10)

        # Difficulty selection
        difficulty_frame = tk.Frame(self.root, bg="#1a1a2e")
        difficulty_frame.pack(pady=20)

        tk.Label(
            difficulty_frame, 
            text="Select difficulty level:", 
            font=("Arial", 14, "bold"), 
            fg="#ffffff", 
            bg="#1a1a2e"
        ).pack(pady=5)

        self.difficulty_var = tk.StringVar(value="All")
        difficulties = ["All", "Basic", "Intermediate", "Advanced", "Expert"]

        difficulty_dropdown = ttk.Combobox(
            difficulty_frame, 
            textvariable=self.difficulty_var, 
            values=difficulties, 
            state="readonly",
            font=("Arial", 12)
        )
        difficulty_dropdown.pack(pady=5)

    def start_quiz(self, topic):
        self.selected_topic = topic
        self.current_question = 0
        self.score = 0
        self.user_answers = []
        self.quiz_completed = False

        # Select questions based on topic and difficulty
        if topic == "cupola":
            all_questions = cupola_questions.copy()
        elif topic == "nbl":
            all_questions = nbl_questions.copy()
        else:  # mixed
            all_questions = cupola_questions + nbl_questions

        # Filter by difficulty if not "All"
        selected_difficulty = self.difficulty_var.get()
        if selected_difficulty != "All":
            all_questions = [q for q in all_questions if q["difficulty"] == selected_difficulty]

        # Randomize and limit questions
        random.shuffle(all_questions)
        self.questions = all_questions[:min(15, len(all_questions))]  # Max 15 questions

        if not self.questions:
            messagebox.showwarning("No Questions", f"No questions available for {selected_difficulty} difficulty.")
            return

        self.create_quiz_interface()

    def create_quiz_interface(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Progress bar
        self.progress_var = tk.StringVar()
        self.progress_var.set(f"Question {self.current_question + 1} of {len(self.questions)}")

        progress_label = tk.Label(
            self.root, 
            textvariable=self.progress_var, 
            font=("Arial", 12, "bold"), 
            fg="#ffffff", 
            bg="#1a1a2e"
        )
        progress_label.pack(pady=10)

        # Score display
        self.score_var = tk.StringVar()
        self.score_var.set(f"Score: {self.score}")

        score_label = tk.Label(
            self.root, 
            textvariable=self.score_var, 
            font=("Arial", 12, "bold"), 
            fg="#00ff00", 
            bg="#1a1a2e"
        )
        score_label.pack(pady=5)

        # Question frame
        question_frame = tk.Frame(self.root, bg="#16213e", relief="raised", borderwidth=2)
        question_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Question text
        current_q = self.questions[self.current_question]

        question_label = tk.Label(
            question_frame, 
            text=f"Q{self.current_question + 1}: {current_q['question']}", 
            font=("Arial", 14, "bold"), 
            fg="#ffffff", 
            bg="#16213e",
            wraplength=800,
            justify="left"
        )
        question_label.pack(pady=20, padx=20)

        # Difficulty and type labels
        info_frame = tk.Frame(question_frame, bg="#16213e")
        info_frame.pack(pady=5)

        difficulty_label = tk.Label(
            info_frame, 
            text=f"Difficulty: {current_q['difficulty']}", 
            font=("Arial", 10), 
            fg="#ffaa00", 
            bg="#16213e"
        )
        difficulty_label.pack(side="left", padx=10)

        type_label = tk.Label(
            info_frame, 
            text=f"Type: {current_q['type']}", 
            font=("Arial", 10), 
            fg="#00aaff", 
            bg="#16213e"
        )
        type_label.pack(side="right", padx=10)

        # Answer options
        self.answer_var = tk.IntVar()
        self.answer_var.set(-1)  # No selection initially

        options_frame = tk.Frame(question_frame, bg="#16213e")
        options_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for i, option in enumerate(current_q['options']):
            radio_btn = tk.Radiobutton(
                options_frame, 
                text=f"{chr(65+i)}. {option}", 
                variable=self.answer_var, 
                value=i, 
                font=("Arial", 12), 
                fg="#ffffff", 
                bg="#16213e", 
                selectcolor="#0f3460",
                activebackground="#16213e",
                activeforeground="#ffffff"
            )
            radio_btn.pack(anchor="w", pady=5, padx=20)

        # Navigation buttons
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(pady=20)

        next_btn = tk.Button(
            button_frame, 
            text="Next Question" if self.current_question < len(self.questions) - 1 else "Finish Quiz", 
            font=("Arial", 12, "bold"), 
            bg="#0f3460", 
            fg="#ffffff", 
            padx=20, 
            pady=10,
            command=self.next_question
        )
        next_btn.pack(side="right", padx=10)

        back_btn = tk.Button(
            button_frame, 
            text="Back to Menu", 
            font=("Arial", 12, "bold"), 
            bg="#8b0000", 
            fg="#ffffff", 
            padx=20, 
            pady=10,
            command=self.create_main_menu
        )
        back_btn.pack(side="left", padx=10)

    def next_question(self):
        # Check if an answer is selected
        if self.answer_var.get() == -1:
            messagebox.showwarning("No Selection", "Please select an answer before proceeding.")
            return

        # Record the answer
        current_q = self.questions[self.current_question]
        selected_answer = self.answer_var.get()
        is_correct = selected_answer == current_q['correct']

        self.user_answers.append({
            'question': current_q['question'],
            'selected': selected_answer,
            'correct': current_q['correct'],
            'is_correct': is_correct,
            'options': current_q['options'],
            'difficulty': current_q['difficulty'],
            'type': current_q['type']
        })

        if is_correct:
            self.score += 1

        # Move to next question or finish quiz
        self.current_question += 1

        if self.current_question >= len(self.questions):
            self.show_results()
        else:
            self.create_quiz_interface()

    def show_results(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Calculate percentage
        percentage = (self.score / len(self.questions)) * 100

        # Results title
        tk.Label(
            self.root, 
            text="🎯 QUIZ RESULTS 🎯", 
            font=("Arial", 24, "bold"), 
            fg="#ffffff", 
            bg="#1a1a2e"
        ).pack(pady=20)

        # Score display
        score_text = f"You scored {self.score} out of {len(self.questions)} ({percentage:.1f}%)"
        tk.Label(
            self.root, 
            text=score_text, 
            font=("Arial", 16, "bold"), 
            fg="#00ff00" if percentage >= 70 else "#ffaa00" if percentage >= 50 else "#ff4444", 
            bg="#1a1a2e"
        ).pack(pady=10)

        # Performance message
        if percentage >= 90:
            message = "🌟 Outstanding! You're a space expert!"
        elif percentage >= 80:
            message = "🚀 Excellent! Great knowledge of space technology!"
        elif percentage >= 70:
            message = "👍 Good job! You know your space facts!"
        elif percentage >= 60:
            message = "📚 Not bad! Keep studying space technology!"
        else:
            message = "💪 Keep learning! Space is fascinating!"

        tk.Label(
            self.root, 
            text=message, 
            font=("Arial", 14), 
            fg="#ffffff", 
            bg="#1a1a2e"
        ).pack(pady=10)

        # Results summary frame
        results_frame = tk.Frame(self.root, bg="#16213e", relief="raised", borderwidth=2)
        results_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Create scrollable text widget for detailed results
        canvas = tk.Canvas(results_frame, bg="#16213e")
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#16213e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add detailed results
        tk.Label(
            scrollable_frame, 
            text="Detailed Results:", 
            font=("Arial", 14, "bold"), 
            fg="#ffffff", 
            bg="#16213e"
        ).pack(pady=10)

        for i, answer in enumerate(self.user_answers):
            result_color = "#00ff00" if answer['is_correct'] else "#ff4444"
            status = "✓ Correct" if answer['is_correct'] else "✗ Incorrect"

            question_frame = tk.Frame(scrollable_frame, bg="#0f1419", relief="solid", borderwidth=1)
            question_frame.pack(pady=5, padx=10, fill="x")

            tk.Label(
                question_frame, 
                text=f"Q{i+1}: {answer['question']}", 
                font=("Arial", 10, "bold"), 
                fg="#ffffff", 
                bg="#0f1419",
                wraplength=700,
                justify="left"
            ).pack(pady=5, padx=10, anchor="w")

            tk.Label(
                question_frame, 
                text=f"Your answer: {answer['options'][answer['selected']]}", 
                font=("Arial", 9), 
                fg=result_color, 
                bg="#0f1419"
            ).pack(padx=10, anchor="w")

            if not answer['is_correct']:
                tk.Label(
                    question_frame, 
                    text=f"Correct answer: {answer['options'][answer['correct']]}", 
                    font=("Arial", 9), 
                    fg="#00ff00", 
                    bg="#0f1419"
                ).pack(padx=10, anchor="w")

            tk.Label(
                question_frame, 
                text=f"{status} | {answer['difficulty']} | {answer['type']}", 
                font=("Arial", 8), 
                fg="#a0a0a0", 
                bg="#0f1419"
            ).pack(padx=10, anchor="w")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame, 
            text="Take Another Quiz", 
            font=("Arial", 12, "bold"), 
            bg="#0f3460", 
            fg="#ffffff", 
            padx=20, 
            pady=10,
            command=self.create_main_menu
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame, 
            text="Export Results", 
            font=("Arial", 12, "bold"), 
            bg="#16537e", 
            fg="#ffffff", 
            padx=20, 
            pady=10,
            command=self.export_results
        ).pack(side="right", padx=10)

    def export_results(self):
        try:
            # Create results summary
            results_data = {
                'quiz_info': {
                    'topic': self.selected_topic,
                    'difficulty': self.difficulty_var.get(),
                    'total_questions': len(self.questions),
                    'score': self.score,
                    'percentage': (self.score / len(self.questions)) * 100,
                    'timestamp': datetime.now().isoformat()
                },
                'detailed_results': self.user_answers
            }

            # Save to JSON file
            with open('quiz_results.json', 'w') as f:
                json.dump(results_data, f, indent=2)

            messagebox.showinfo("Export Successful", "Results exported to 'quiz_results.json'")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export results: {str(e)}")


def main():
    """Main function to run the quiz application."""
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
