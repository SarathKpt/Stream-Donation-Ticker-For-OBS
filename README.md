# \# OBS Smooth Donation Ticker  

# A fully smooth, zero-jump, auto-updating donation ticker designed for streamers.  

# Works perfectly inside OBS Browser Source and updates without ever restarting the animation.

# 

# \## 🚀 Features

# \- \*\*Perfectly smooth scrolling ticker\*\*  

# &nbsp; No jumps, no resets, no visual stutter — even when new donations arrive.

# &nbsp; 

# \- \*\*Auto-updating donations\*\*  

# &nbsp; The ticker reads from `donations.json` and updates only at the \*\*end of the current loop\*\*, creating a seamless experience.

# 

# \- \*\*Two-strip seamless engine\*\*  

# &nbsp; Uses a twin-strip mechanism (A → B → A) to guarantee:

# &nbsp; - fully scrolls out of the left side,

# &nbsp; - pauses,

# &nbsp; - then glides in from the right,

# &nbsp; - with no overlapping content.

# 

# \- \*\*Works in OBS\*\*  

# &nbsp; Open the HTML as a browser source and you're done.

# 

# \- \*\*Simple backend included\*\*  

# &nbsp; A lightweight Flask server (`server.py`) handles:

# &nbsp; - hosting the HTML \& JSON  

# &nbsp; - writing new donations via `/add-donation`  

# &nbsp; - serving fresh, no-cache JSON

# 

# \- \*\*Mobile / Web UI to add donations manually\*\*  

# &nbsp; Type a name + amount → saved instantly → appears in next loop.

# 

# ---

# 

# \## 📁 Project Structure

# /

# ├── obs-ticker.html # The main ticker UI (OBS Browser Source)

# ├── server.py # Backend server (Flask)

# ├── donations.json # Stored donation data

# ├── run.bat

# └── README.md # Documentation

### 



---



\## 🛠️ Requirements



\- Python 3.8+

\- Pip installed

\- OBS Studio (if using it inside OBS)

\- Any modern browser



---



\## 📦 Installation



\### 1. Clone the repository

```sh

git clone https://github.com/yourusername/obs-smooth-donation-ticker.git

cd obs-smooth-donation-ticker



\###2. Install dependencies

pip install flask

