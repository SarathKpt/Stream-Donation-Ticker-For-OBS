# 🎉 OBS Smooth Donation Ticker

A smooth, zero-jump, auto-updating donation ticker optimized for OBS Browser Source. Updates appear only at the end of each loop for a seamless broadcast-quality experience.

## ✨ Overview

This project provides an animation-stable donation ticker with a simple backend. It ensures no stutter, no reset, and no duplicate scroll artifacts when new donations are added.

---

## 🚀 Features

* Smooth continuous scrolling without jumps
* Updates applied only at loop end for visual stability
* Two-strip seamless engine (A → B → A)
* Fully compatible with OBS Browser Source
* Lightweight Flask backend for hosting files and writing donations
* Built-in mobile-friendly UI for manual donations

---

## 📁 Project Structure

```
/
├── obs-ticker.html     # Ticker UI
├── server.py           # Flask backend
├── donations.json      # Donation database
├── run.bat             # Windows launcher
└── README.md
```

---

## 🛠️ Requirements

* Python 3.8+
* pip
* OBS Studio (optional but recommended)
* Any modern browser

---

## 📦 Installation

### Clone the repository

```sh
git clone https://github.com/SarathKpt/Stream-Donation-Ticker-For-OBS.git
cd Stream-Donation-Ticker-For-OBS
```

### Install dependencies

```sh
pip install flask
```

### Start the server (Windows)

```
run.bat
```

### Start the server (Linux / macOS)

```sh
python3 server.py
```

Default server port: **8000**

---

## 🎥 Using with OBS

1. Open OBS → Add → Browser Source
2. Set URL:

```
http://localhost:8000
```

3. Width: 1920
4. Height: 150 (adjust as needed)
5. Optional: enable “Refresh browser when scene becomes active”

The ticker will load and auto-update between loops.

---

## ➕ Adding Donations

### Manual Entry

Use the built-in form on `http://localhost:8000`.

Enter:

* Name
* Amount

The ticker updates at the end of its current scroll cycle.

### Programmatic Entry

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

Useful for bots, scripts, or external automation.

---

## 🔁 How the Smooth Loop Works

The system uses:

* Two alternating strips
* Automatic width calculation
* Controlled transform-based timing
* A three-stage sequence (out → pause → in)
* Queued updates (applied only at loop end)

This prevents:

* mid-loop resets
* flicker gaps
* layout jumps
* scroll-speed anomalies

Duration limits:

```js
MIN_DURATION_MS = 300;
MAX_DURATION_MS = 60000;
```

---

## 🔒 Data File

`donations.json` is created automatically.

Example:

```json
[
  {"name": "Alice", "tip": 100, "date": "2025-11-14T18:00:00Z"}
]
```

---

## 🔮 Future Plans

### Automatic Donation Capture (Tasker / MacroDroid)

Planned integration for mobile automation tools:

1. Phone receives donation/UPI notification
2. Automation reads notification text
3. Extracts name, amount, timestamp
4. Sends JSON to `/add-donation`
5. Ticker updates automatically on next loop

Enables hands-free real-time donation tracking.

---

## 🛡️ Security Notes

* Do not expose the server publicly without protection.
* The `/add-donation` endpoint writes to disk.
* Use firewalls or reverse proxies if hosting externally.

---

## 📜 License

MIT License

---

## ❤️ Contributions

Pull requests are welcome: bug fixes, UI themes, integrations, improvements.

---

## 🙌 Credits

Created by Sarath. Designed for a stable, professional donation ticker experience in OBS.
