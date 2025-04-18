
# San Francisco Restaurant Recommender

## Overview

This expert system recommends restaurants in **San Francisco** based on user preferences. It uses **Prolog** for logical inference and a **Flask** web interface for interaction. The system presents users with a series of natural-language questions to guide them through the recommendation process.

---

## 🔍 Features

- **Logical Inference**: Built on SWI-Prolog and PySWIP for rule-based recommendations  
- **Natural Language Questions**: Friendly, conversational prompts  
- **Responsive Web Interface**: Built with Flask, smooth on desktop or Codespaces  
- **Progressive Interaction**: Tracks answers and adapts flow dynamically  
- **Testable Backend**: Supports automated test cases and a debug mode

---

## 🧠 Technologies Used

- **SWI-Prolog**: Inference engine for rule logic  
- **Python 3.x**: Core language  
- **PySWIP**: Python–Prolog integration  
- **Flask**: Lightweight web framework  
- **HTML/CSS**: Simple templates for UI  
- **GitHub Codespaces**: Development environment

---

## 📁 Project Structure

```
sf-restaurant-expert-system/
├── app.py                  ← Main Flask web app (Extension 3)
├── recommender.py          ← CLI Prolog-based expert system
├── kb.pl                   ← Prolog knowledge base
├── templates/
│   ├── index.html          ← Welcome screen
│   ├── question.html       ← Askable prompts
│   ├── recommendation.html← Restaurant result page
│   ├── no_results.html     ← Shown when no match is found
│   └── redirect.html       ← JavaScript redirect for Codespaces
├── recommender_gui.py      ← ❌ Deprecated: old Tkinter GUI
└── web_gui.py              ← ❌ Deprecated: older Flask attempt
```

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/sf-restaurant-expert-system.git
cd sf-restaurant-expert-system
```

### 2. Set up virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install SWI-Prolog

- **macOS**: `brew install swi-prolog`
- **Ubuntu/Debian**: `sudo apt-get install swi-prolog`
- **Windows**: [Download here](https://www.swi-prolog.org/download/stable)

---

## 🚀 Usage

### Start the web app:

```bash
python app.py
```

Then open your browser to:

```
http://localhost:5000
```

### Follow the prompts:
- Answer a series of questions about your preferences
- Receive a tailored restaurant recommendation

---

## 💻 Command-Line Version (Optional)

Run the logic via CLI using:

```bash
python recommender.py
```

---

## ✅ Extension Implementations

This project implements all three possible extensions:

- **Menu-based responses**: Selectable options via buttons or radio inputs  
- **Natural language questions**: Intuitive, user-friendly prompts  
- **Web-based GUI**: Seamlessly integrated Flask frontend with real Prolog backend

---

## 📚 Knowledge Base Structure

The Prolog KB (`kb.pl`) defines restaurants with attributes like:

- `meal_type`: breakfast, lunch, dinner  
- `cuisine`: e.g., Indian, American, Thai  
- `diet`: standard, vegan, halal, etc.  
- `price`: affordable, moderate, expensive  
- `atmosphere`: cozy, upscale, casual  
- `distance`: from Minerva residence  
- `service_style`: dine-in, take-out, quick bite  
- `group_size`: solo, small, or large group  
- `noise`: quiet, moderate, lively

---

## 🧪 Test Cases (All Pass ✅)

| Test # | Description                         | Expected Result                  |
|--------|-------------------------------------|----------------------------------|
| 1      | **Breakfast at Tratto**             | Tratto                           |
| 2      | **Lunch at Raavi**                  | Raavi North Indian Cuisine       |
| 3      | **Quick Vegan Lunch at Mr. Charlie’s** | Mr. Charlie's                    |
| 4      | **Upscale Seafood Dinner**          | Scoma's Restaurant               |
| 5      | **No Match** (e.g., Thai + Breakfast + Upscale) | No matching restaurant found     |

---

## 👥 Contributors

- **Praise Ogwuche** – *Backend, Logic & Flask GUI*  
  📧 praiseogwuche@uni.minerva.edu  
- **Mohamed Abdelrazek** – *System Design & Data Collection*  
  📧 mohamed@uni.minerva.edu  
- **Nuray Nurkhojayeva** – *Testing & Real-world Validation*  
  📧 nuray.nurkhojayeva@uni.minerva.edu

---

## 🎓 Acknowledgements

This project was developed as part of:

> **CS152: Harnessing Artificial Intelligence Algorithms**  
> **Minerva University, Spring 2025**

Special thanks to the course team for guidance and feedback!
