# 🗓️ Personal Routine Tracker

> A visually attractive **weekly habit tracker** built with **Python & Streamlit** — track your daily routine and analyse your performance with beautiful charts and dashboards.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Pre-filled Habits](#pre-filled-habits)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Pages](#pages)
- [Data Storage](#data-storage)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 📖 Overview

The **Personal Routine Tracker** is a Streamlit web application that helps you build and maintain daily habits. It automatically organises your week (Monday → Sunday) based on the current date, lets you tick off habits as you complete them, and gives you rich analytics so you can see exactly how productive each week has been.

---

## ✨ Features

### 🗂️ Weekly Habit Tracker
- Interactive table — **habits as rows**, **Mon–Sun as columns**
- One-click **checkbox** to mark each habit complete
- Week **auto-resets** every 7 days based on today's date
- Week range displayed at the top → *e.g.* **Week: Apr 28 – May 4**

### 📊 Analytics Dashboard
| Metric | Description |
|---|---|
| ✅ Completion % | Percentage of habits completed for the week |
| 🔢 Total Tasks | Absolute number of completed tasks |
| 🏆 Productivity Score | Weighted weekly performance score |
| 🔥 Habit Streaks | Consecutive days a habit has been completed |

### 📈 Charts (Plotly / Streamlit)
- **Bar chart** — weekly progress per habit
- **Pie chart** — completed vs missed
- **Line / area chart** — daily productivity over the week

### 🎨 UI Design
- Emoji / icon labels for every habit
- Coloured progress bars
- Modern sidebar navigation
- Descriptive page titles & sections

### ⚡ Extra Features
- **Reset Week** button to clear current week's data
- **Motivational Quote** section (refreshes each visit)
- **Streak Counter** per habit
- **Completion % indicator** at a glance

---

## 🌅 Pre-filled Habits

| # | Habit | Time |
|---|---|---|
| 1 | ⏰ Wake up at 5:00 AM | 5:00 AM |
| 2 | 🪥 Fresh routine (brush + face wash) | ~10 min |
| 3 | 🏋️ Gym (15 min) + 🧘 Meditation (10 min) + 🙏 Surya Namaskar (5 min) | Morning |
| 4 | 🚿 Cold water bath | ~10 min |
| 5 | ✅ Finish morning routine before 6:00 AM | by 6:00 AM |
| 6 | 💻 DSA practice | 6:00 – 8:30 AM |
| 7 | 🏢 Office work | 9:00 – 5:00 PM |
| 8 | 🎧 Relax + snacks + podcast + business learning | 5:30 – 7:00 PM |
| 9 | 📚 Study hacking / tips & tricks | 7:00 – 9:00 PM |
| 10 | 🍽️ Dinner | 9:00 – 10:00 PM |
| 11 | 📝 Fill tracker and sleep at 10:00 PM | 10:00 PM |

---

## 📁 Project Structure

```
Persanal-Tracker/
│
├── app.py                  # Main Streamlit application
├── data/
│   └── habits.json         # Persisted habit completion data (auto-created)
├── utils/
│   ├── data_manager.py     # Load / save habit data (CSV or JSON)
│   ├── analytics.py        # Streak, score & percentage calculations
│   └── charts.py           # Plotly chart helpers
├── requirements.txt        # Python dependencies
└── README.md               # You are here 📍
```

---

## ⚙️ Installation

### Prerequisites
- Python **3.9+**
- `pip` package manager

### 1 — Clone the repository

```bash
git clone https://github.com/SreeCharan1234/Persanal-Tracker.git
cd Persanal-Tracker
```

### 2 — Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` contents:**

```
streamlit>=1.32.0
plotly>=5.20.0
pandas>=2.2.0
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501`.

---

## 📄 Pages

| Page | Description |
|---|---|
| 🏠 **Tracker** | Main weekly habit table with checkboxes |
| 📊 **Analytics** | Charts, streaks, scores and completion stats |

Navigate between pages using the **sidebar** on the left.

---

## 💾 Data Storage

Habit data is stored **locally** so nothing leaves your machine.

- **Format:** JSON (or CSV — configurable in `utils/data_manager.py`)
- **Location:** `data/habits.json`
- **Persistence:** Data is loaded automatically every time the app starts
- **Reset:** Use the **Reset Week** button to clear all checkboxes for the current week

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Python](https://python.org) | Core language |
| [Streamlit](https://streamlit.io) | UI framework |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data handling |
| JSON / CSV | Local data persistence |

---

## 🖼️ Screenshots

> *Add screenshots of your running app here.*

| Tracker Page | Analytics Page |
|---|---|
| *(screenshot)* | *(screenshot)* |

---

## 🤝 Contributing

Contributions, ideas and bug reports are welcome!

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ to boost productivity — one habit at a time 🚀
</p>
