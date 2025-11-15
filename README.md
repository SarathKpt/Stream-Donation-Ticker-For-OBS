# OBS Smooth Donation Ticker  
A fully smooth, zero-jump, auto-updating donation ticker designed for streamers.  
Works perfectly inside OBS Browser Source and updates without ever restarting the animation.


## 🚀 Features
- **Perfectly smooth scrolling ticker**  
  No jumps, no resets, no visual stutter — even when new donations arrive.
  
- **Auto-updating donations**  
  The ticker reads from `donations.json` and updates only at the **end of the current loop**, creating a seamless experience.

- **Two-strip seamless engine**  
  Uses a twin-strip mechanism (A → B → A) to guarantee:
  - fully scrolls out of the left side,
  - pauses,
  - then glides in from the right,
  - with no overlapping content.

- **Works in OBS**  
  Open the HTML as a browser source and you're done.

- **Simple backend included**  
  A lightweight Flask server (`server.py`) handles:
  - hosting the HTML & JSON  
  - writing new donations via `/add-donation`  
  - serving fresh, no-cache JSON

- **Mobile / Web UI to add donations manually**  
  Type a name + amount → saved instantly → appears in next loop.

---

## 📁 Project Structure

```

/
├── obs-ticker.html     # The main ticker UI (OBS Browser Source)
├── server.py           # Backend server (Flask)
├── donations.json      # Stored donation data
└── README.md           # Documentation

````

---

## 🛠️ Requirements

- Python 3.8+
- Pip installed
- OBS Studio (if using it inside OBS)
- Any modern browser

---

## 📦 Installation

### 1. Clone the repository
```sh
git clone https://github.com/ySarathKpt/Stream-Donation-Ticker-For-OBS.git
cd Stream-Donation-Ticker-For-OBS
````

### 2. Install dependencies

```sh
pip install flask
```

### 3. Start the server
Open
```sh
run.bat
```

You will see:

```
Starting server at http://0.0.0.0:8000
Open http://localhost:8000
```

---

## 🌐 Using in OBS

1. Open OBS → Add → **Browser Source**
2. Set URL to:

```
http://localhost:8000
```

3. Set width: **1920**
4. Set height: **150** (or whatever fits your layout)
5. Enable **Refresh Browser when scene becomes active** (optional)

Now the ticker appears at the bottom and updates automatically.

---

## ➕ Adding a Donation (Manually)

There is a built-in input form on the webpage.

Enter:

* **Name**
* **Amount**

Click **Add Donation**.

The entry is written to `donations.json` via the Flask backend and will appear in the **next loop**, without any visual jump.

---

## ⚙️ Adding Donations Programmatically

POST to:

```
POST /add-donation
Content-Type: application/json
```

Example payload:

```json
{
  "name": "John Doe",
  "tip": 500,
  "date": "2025-11-15T16:20:00Z"
}
```

This lets you integrate with bots, APIs, or custom scripts.

---

## 🔁 How the Smooth Loop Works

Traditional tickers duplicate text and use CSS animations — which causes jumps, resets, and glitches when updated.

This ticker uses:

* **Two independent strips (A and B)**
* **Dynamic measurement of content width**
* **Controlled transform-based transitions**
* **“Out → pause → in” sequence**
* **Queued updates (applied only at loop end)**

This produces a professional, broadcast-quality, zero-glitch ticker.

---

## 🧩 Technical Notes

### The ticker guarantees:

* No overlapping text
* No mid-loop animation resets
* No flickering gaps
* No jump when window resizes
* No jump when new donations arrive

### The system enforces scroll duration limits:

```js
const MIN_DURATION_MS = 300;       // prevents teleport-fast scrolling
const MAX_DURATION_MS = 60000;     // prevents extremely slow 2-minute scrolls
```

---

## 🔒 Data File

`donations.json` is automatically created if missing.

Example:

```json
[
  {
    "name": "Alice",
    "tip": 100,
    "date": "2025-11-14T18:00:00Z"
  }
]
```

---

## 📜 License

MIT License.
Use it freely in your streams and commercial projects.

---

## ❤️ Contributions

Pull requests are welcome.
You can contribute:

* bug fixes
* feature improvements
* CSS themes
* integrations with StreamElements, Streamlabs, or UPI/Pay links

---

## 🙌 Credits

Created by Sarath.
Designed for **smoothest possible donation ticker experience** in OBS.

---

```
