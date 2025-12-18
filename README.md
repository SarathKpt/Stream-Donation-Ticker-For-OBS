# 🎉 OBS Smooth Donation Ticker

> **Zero Jitter. Zero Stutter. Professional Grade.**

A smooth, zero-jump, auto-updating donation ticker optimized for OBS Browser Source. Updates appear only at the end of each loop for a seamless broadcast-quality experience.

---

## ✨ Overview

This project provides an animation-stable donation ticker with a simple backend. It ensures no stutter, no reset, and no duplicate scroll artifacts when new donations are added.

## 🚀 Key Features

* **🎬 Smooth Animation**: Continuous scrolling without jumps using a custom two-strip engine.
* **🎛️ Admin Dashboard**: New dedicated control panel (`/admin`) to manage data and settings.
* **🎨 Live Customization**: Change colors, fonts, scroll speed, and currency symbols in real-time.
* **📅 Time Filtering**: Show donations from "Today", "Past Week", "Past Month", or a custom range.
* **🏆 Top Donation Badge**: Automatically displays the highest donor for the selected period.
* **🛠️ Donation Management**: Edit or delete past donations directly from the admin list.
* **⚡ Pro Mode**: Inject custom CSS directly from the dashboard for advanced styling.
* **💾 Local Data**: All data is stored in `donations.json` on your machine. No third-party accounts required.
* **📱 Mobile Friendly**: Add manual donations from your phone via the local network.

---

## 📁 Project Structure

```
/
├── obs-ticker.html     # The visual ticker source for OBS
├── admin.html          # The Admin Control Panel
├── server.py           # Python Flask backend
├── donations.json      # Your donation database (auto-created)
├── config.json         # Your settings (auto-created)
├── run.bat             # Windows launcher script
└── README.md           # Documentation
```

---

## 🛠️ Requirements

* **Python 3.8+**
* `pip` (Python package manager)
* OBS Studio (optional but recommended)
* Any modern web browser

---

## 📦 Installation & Setup

### 1. Download
Clone or download this repository to a folder on your computer.

### 2. Install Dependencies
Open a terminal in the folder and run:
```sh
pip install flask
```

### 3. Start the Server

* **Windows**: Double-click `run.bat`.
* **Linux / macOS**: Run `python3 server.py`.

The server will start at port **8000**.

---

## 🎥 Using with OBS Studio

1.  Open OBS.
2.  Add a **Browser Source**.
3.  Set URL to: `http://localhost:8000`
4.  Set Width to **1920** (or your canvas width).
5.  Set Height to **150** (or desired height).
6.  **Optional**: Enable “Refresh browser when scene becomes active”.

The ticker will load and begin scrolling automatically!

---

## 🎛️ The Admin Dashboard

Navigate to **[http://localhost:8000/admin](http://localhost:8000/admin)** in your browser to manage everything.

### 🎚️ Controls (Left Panel)

* **💰 Add Donation**: Manual entry for cash/offline donations.
* **📅 Data Filter**: Choose to show "Lifetime", "Today", "Week", "Month", or "Custom Range". This instantly updates the ticker list and the "Top Donation" badge.
* **⚙️ General Settings**:
    * **Currency**: Select your symbol (₹, $, €, £, etc.).
    * **Speed**: Slider control for scroll speed (px/s).
* **🎨 Appearance**:
    * **Colors**: Pickers for Ticker Background, Text, Accent, and Page Background.
    * **Typography**: Change Font Family (Inter, Courier, Impact) and Size.
* **⚡ Pro Mode**: A text area to inject raw CSS (e.g., `.donor { color: red; }`) for advanced styling.

### 💬 Live History (Right Panel)

* A chat-style list of all donations matching your filter.
* **✏️ Edit**: Click to fix typos in names or amounts.
* **🗑️ Delete**: Click to remove a donation entry.

---

## ➕ How to Add Donations

### 1. Manual Entry
Use the form on the **Admin Dashboard** (`/admin`). Great for reading out donations from chat!

### 2. Programmatic Entry (API)
Perfect for bots, scripts, or external automation tools like **Tasker** or **MacroDroid**.

**Endpoint:** `POST /add-donation`
**Header:** `Content-Type: application/json`

**Example Payload:**
```json
{
  "name": "SuperFan",
  "tip": 500,
  "date": "2025-11-15T16:20:00Z"
}
```

---

## 🔁 How the Smooth Loop Works

The system uses a smart logic to ensure professional broadcast quality:

1.  **Two Alternating Strips**: Uses an 'A' and 'B' strip system.
2.  **Wait-For-Exit**: Updates are *queued* and only applied when a text strip has fully left the screen.
3.  **Out-Then-In**: The system forces a strip to animate completely out before the new strip animates in.

**This prevents:**
* ❌ Mid-loop resets
* ❌ Flicker gaps
* ❌ Layout jumps
* ❌ Scroll-speed anomalies

Duration limits:

```js
MIN_DURATION_MS = 300;
MAX_DURATION_MS = 60000;
```

---

## 🔒 Data File

* `donations.json`: Stores the donation history. Created automatically.
* `config.json`: Stores your styling preferences. Created automatically.

---

## 🔮 Future Plans

### 🤖 Automatic Donation Capture (Tasker / MacroDroid)

Planned integration for mobile automation tools:

1.  Phone receives donation/UPI notification
2.  Automation reads notification text
3.  Extracts name, amount, timestamp
4.  Sends JSON to `/add-donation`
5.  Ticker updates automatically on next loop

Enables hands-free real-time donation tracking.

---

## 🛡️ Security Notes

* The server runs on `0.0.0.0`, making it accessible to your local network.
* **Do not expose this port to the public internet** without a firewall or reverse proxy.
* The `/add-donation` endpoint writes directly to your disk.

---

## 📜 License

MIT License. Free to use, modify, and stream with!

---

## ❤️ Contributions

Pull requests are welcome!
* 🐛 Bug fixes
* 🎨 UI themes
* 🔌 Integrations
* ✨ Improvements

---

## 🙌 Credits

Created by **Sarath**. Designed for a stable, professional donation ticker experience in OBS.