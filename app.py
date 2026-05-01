import json
import os
import random
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu

# ─── Constants ────────────────────────────────────────────────────────────────

DATA_FILE = os.path.join(os.path.dirname(__file__), "habit_data.json")

HABITS = [
    "⏰ Wake up at 5:00 AM",
    "🪥 Fresh routine (brush + face wash) – 10 min",
    "🏋️ Gym (15 min) + 🧘 Meditation (10 min) + 🙏 Surya Namaskar (5 min)",
    "🚿 Cold water bath – 10 min",
    "✅ Finish morning routine before 6:00 AM",
    "💻 DSA practice (6:00 – 8:30 AM)",
    "🏢 Office work (9:00 – 5:00)",
    "🎧 Relax + snacks + podcast + business learning (5:30 – 7:00 PM)",
    "📚 Study hacking / tips & tricks (7:00 – 9:00 PM)",
    "🍽️ Dinner (9:00 – 10:00 PM)",
    "📝 Fill tracker and sleep at 10:00 PM",
]

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

QUOTES = [
    "🌟 Discipline is the bridge between goals and accomplishment.",
    "🔥 Small daily improvements lead to stunning results.",
    "💪 Push yourself, because no one else is going to do it for you.",
    "🚀 Success is the sum of small efforts repeated day in and day out.",
    "🌅 Every morning is a fresh opportunity to build the life you want.",
    "🎯 Focus on progress, not perfection.",
    "⚡ The secret of your future is hidden in your daily routine.",
    "🏆 Winners are not people who never fail, but people who never quit.",
    "🌱 Invest in yourself — it pays the best interest.",
    "💡 A year from now you'll wish you had started today.",
    "🧠 Your habits shape your identity.",
    "✨ Be consistent. The results will speak for themselves.",
    "🌊 Ride the wave of discipline into the ocean of success.",
    "🦁 Wake up with determination. Go to bed with satisfaction.",
    "🎵 The rhythm of daily habits is the music of a great life.",
]

# ─── Data Layer ───────────────────────────────────────────────────────────────

def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            st.warning("⚠️ habit_data.json was corrupted — starting fresh.")
            return {}
    return {}


def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_week_key(ref_date: date = None) -> str:
    d = ref_date or date.today()
    return f"{d.isocalendar()[0]}-W{d.isocalendar()[1]:02d}"


def get_week_dates(ref_date: date = None) -> list[date]:
    d = ref_date or date.today()
    monday = d - timedelta(days=d.weekday())
    return [monday + timedelta(days=i) for i in range(7)]


def get_week_label(ref_date: date = None) -> str:
    days = get_week_dates(ref_date)
    start = days[0].strftime("%b %-d")
    end = days[-1].strftime("%b %-d")
    return f"{start} – {end}"


def ensure_week_initialized(data: dict, week_key: str):
    if week_key not in data:
        data[week_key] = {}
    for habit in HABITS:
        if habit not in data[week_key]:
            data[week_key][habit] = dict.fromkeys(DAYS, False)


def get_completion_pct(data: dict, week_key: str) -> float:
    total = len(HABITS) * len(DAYS)
    if total == 0:
        return 0.0
    done = sum(
        1
        for habit in HABITS
        for day in DAYS
        if data.get(week_key, {}).get(habit, {}).get(day, False)
    )
    return round(done / total * 100, 1)


def get_habit_completion(data: dict, week_key: str) -> dict:
    result = {}
    for habit in HABITS:
        done = sum(
            1 for day in DAYS if data.get(week_key, {}).get(habit, {}).get(day, False)
        )
        result[habit] = round(done / len(DAYS) * 100, 1)
    return result


def get_day_completion(data: dict, week_key: str) -> dict:
    return {
        day: sum(
            1
            for habit in HABITS
            if data.get(week_key, {}).get(habit, {}).get(day, False)
        )
        for day in DAYS
    }


def compute_streak(data: dict, habit: str, max_days: int = 365) -> int:
    today = date.today()
    streak = 0
    current = today
    for _ in range(max_days):
        week_key = get_week_key(current)
        day_name = current.strftime("%a")
        if day_name not in DAYS:
            break
        if data.get(week_key, {}).get(habit, {}).get(day_name, False):
            streak += 1
            current -= timedelta(days=1)
        else:
            break
    return streak


def _pct_color(pct: float) -> str:
    if pct >= 0.8:
        return "#22C55E"
    if pct >= 0.4:
        return "#F59E0B"
    return "#EF4444"

# ─── Shared CSS ───────────────────────────────────────────────────────────────

def inject_css():
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1A0533 0%, #0F0F1A 100%);
            border-right: 1px solid #2D2D4E;
        }
        div[data-testid="metric-container"] {
            background: #1A1A2E;
            border: 1px solid #2D2D4E;
            border-radius: 12px;
            padding: 16px 20px;
        }
        .habit-row-even { background: #12122A; border-radius: 8px; padding: 4px; }
        .habit-row-odd  { background: #1A1A2E; border-radius: 8px; padding: 4px; }
        .section-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #A78BFA;
            margin-bottom: 6px;
        }
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #7C3AED, #A78BFA);
            border-radius: 4px;
        }
        .block-container { padding-top: 1.5rem; }
        .quote-box {
            background: linear-gradient(135deg, #1E1040 0%, #12122A 100%);
            border-left: 4px solid #7C3AED;
            border-radius: 0 10px 10px 0;
            padding: 14px 20px;
            margin: 12px 0 20px 0;
            font-style: italic;
            color: #C4B5FD;
            font-size: 1.0rem;
        }
        .streak-badge {
            display: inline-block;
            background: #7C3AED;
            color: white;
            border-radius: 12px;
            padding: 2px 10px;
            font-size: 0.82rem;
            font-weight: 600;
            margin-left: 6px;
        }
        .stCheckbox label { font-size: 0.78rem !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ─── Tracker Page ─────────────────────────────────────────────────────────────

def _render_tracker_header(week_dates: list, overall: float):
    col_title, col_score = st.columns([3, 1])
    with col_title:
        st.markdown("## 📅 Weekly Habit Tracker")
        st.markdown(
            f"<p style='color:#A78BFA; font-size:1.05rem; margin-top:-12px;'>"
            f"<b>Week:</b> {get_week_label()}</p>",
            unsafe_allow_html=True,
        )
    with col_score:
        st.metric("📊 Week Score", f"{overall}%")

    if "quote" not in st.session_state:
        st.session_state.quote = random.choice(QUOTES)
    st.markdown(
        f'<div class="quote-box">{st.session_state.quote}</div>',
        unsafe_allow_html=True,
    )

    header_cols = st.columns([4] + [1] * 7 + [1.4])
    header_cols[0].markdown("<div class='section-title'>Habit</div>", unsafe_allow_html=True)
    for i, (day, d) in enumerate(zip(DAYS, week_dates)):
        is_today = d == date.today()
        color = "#A78BFA" if is_today else "#94A3B8"
        suffix = " 🔵" if is_today else ""
        header_cols[i + 1].markdown(
            f"<div style='text-align:center; color:{color}; font-size:0.82rem; font-weight:700;'>"
            f"{day}<br>{d.strftime('%-d')}{suffix}</div>",
            unsafe_allow_html=True,
        )
    header_cols[-1].markdown(
        "<div style='text-align:center; color:#94A3B8; font-size:0.82rem; font-weight:700;'>Done %</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#2D2D4E; margin: 4px 0 10px 0;'>", unsafe_allow_html=True)


def _render_habit_rows(data: dict, week_key: str) -> bool:
    changed = False
    for h_idx, habit in enumerate(HABITS):
        row_class = "habit-row-even" if h_idx % 2 == 0 else "habit-row-odd"
        st.markdown(f"<div class='{row_class}'>", unsafe_allow_html=True)
        row_cols = st.columns([4] + [1] * 7 + [1.4])

        row_cols[0].markdown(
            f"<div style='font-size:0.88rem; padding-top:6px; color:#E2E8F0;'>{habit}</div>",
            unsafe_allow_html=True,
        )

        for d_idx, day in enumerate(DAYS):
            current_val = data[week_key][habit][day]
            new_val = row_cols[d_idx + 1].checkbox(
                label=" ",
                value=current_val,
                key=f"cb_{week_key}_{h_idx}_{d_idx}",
            )
            if new_val != current_val:
                data[week_key][habit][day] = new_val
                changed = True

        done_count = sum(1 for day in DAYS if data[week_key][habit][day])
        pct = done_count / len(DAYS)
        color = _pct_color(pct)
        row_cols[-1].markdown(
            f"<div style='text-align:center; padding-top:6px; font-weight:700; "
            f"color:{color}; font-size:0.9rem;'>{int(pct*100)}%</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    return changed


def _render_reset_button(data: dict, week_key: str):
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🔄 Reset This Week", type="secondary"):
            st.session_state["confirm_reset"] = True

    if st.session_state.get("confirm_reset"):
        col_yes, col_no, _ = st.columns([1, 1, 4])
        with col_yes:
            if st.button("✅ Yes, reset", type="primary"):
                for habit in HABITS:
                    data[week_key][habit] = dict.fromkeys(DAYS, False)
                save_data(data)
                st.session_state["confirm_reset"] = False
                st.success("Week reset!")
                st.rerun()
        with col_no:
            if st.button("❌ Cancel"):
                st.session_state["confirm_reset"] = False
                st.rerun()


def show_tracker(data: dict, week_key: str, week_dates: list, overall: float):
    _render_tracker_header(week_dates, overall)

    changed = _render_habit_rows(data, week_key)
    if changed:
        save_data(data)

    st.markdown("<br>", unsafe_allow_html=True)
    current_overall = get_completion_pct(data, week_key)
    st.markdown(
        f"<div class='section-title'>📈 Overall Week Progress — {current_overall}%</div>",
        unsafe_allow_html=True,
    )
    st.progress(current_overall / 100)

    st.markdown("<br>", unsafe_allow_html=True)
    _render_reset_button(data, week_key)

# ─── Analytics Page ───────────────────────────────────────────────────────────

def show_analytics(data: dict, week_key: str, overall_pct: float):
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown(
        f"<p style='color:#A78BFA; font-size:1.05rem; margin-top:-12px;'>"
        f"Week: {get_week_label()}</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    total_possible = len(HABITS) * len(DAYS)
    total_done = round(overall_pct / 100 * total_possible)
    total_missed = total_possible - total_done

    best_streak_val = 0
    for habit in HABITS:
        s = compute_streak(data, habit)
        if s > best_streak_val:
            best_streak_val = s

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("✅ Tasks Done", total_done, f"of {total_possible}")
    col2.metric("❌ Tasks Missed", total_missed)
    col3.metric("🏆 Week Score", f"{overall_pct}%")
    col4.metric("🔥 Best Streak", f"{best_streak_val} days")

    st.markdown("<br>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("<div class='section-title'>📅 Completions Per Day</div>", unsafe_allow_html=True)
        day_data = get_day_completion(data, week_key)

        fig_bar = px.bar(
            x=DAYS,
            y=list(day_data.values()),
            labels={"x": "Day", "y": "Habits Completed"},
            color=list(day_data.values()),
            color_continuous_scale=["#3B1A7A", "#7C3AED", "#A78BFA", "#C4B5FD"],
            text=list(day_data.values()),
        )
        fig_bar.update_traces(textposition="outside", marker_line_width=0)
        fig_bar.update_layout(
            plot_bgcolor="#12122A",
            paper_bgcolor="#12122A",
            font_color="#E2E8F0",
            coloraxis_showscale=False,
            margin={"t": 20, "b": 20, "l": 10, "r": 10},
            yaxis={"range": [0, len(HABITS) + 1], "gridcolor": "#2D2D4E"},
            xaxis={"gridcolor": "#2D2D4E"},
            height=320,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.markdown("<div class='section-title'>🍩 Completed vs Missed</div>", unsafe_allow_html=True)
        fig_pie = px.pie(
            names=["Completed ✅", "Missed ❌"],
            values=[total_done, total_missed],
            color_discrete_sequence=["#7C3AED", "#EF4444"],
            hole=0.45,
        )
        fig_pie.update_traces(
            textinfo="percent+label",
            textfont_size=13,
            marker={"line": {"color": "#0F0F1A", "width": 2}},
        )
        fig_pie.update_layout(
            plot_bgcolor="#12122A",
            paper_bgcolor="#12122A",
            font_color="#E2E8F0",
            showlegend=True,
            legend={"orientation": "h", "yanchor": "bottom", "y": -0.2},
            margin={"t": 20, "b": 20, "l": 10, "r": 10},
            height=320,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<div class='section-title'>🎯 Per-Habit Completion Rate</div>", unsafe_allow_html=True)
    habit_pct = get_habit_completion(data, week_key)

    short_labels = [h[:38] for h in HABITS]
    colors = [_pct_color(v / 100) for v in habit_pct.values()]

    fig_habit = go.Figure(
        go.Bar(
            x=list(habit_pct.values()),
            y=short_labels,
            orientation="h",
            marker_color=colors,
            text=[f"{v}%" for v in habit_pct.values()],
            textposition="outside",
        )
    )
    fig_habit.update_layout(
        plot_bgcolor="#12122A",
        paper_bgcolor="#12122A",
        font_color="#E2E8F0",
        margin={"t": 10, "b": 10, "l": 10, "r": 60},
        xaxis={"range": [0, 115], "gridcolor": "#2D2D4E", "title": "Completion %"},
        yaxis={"gridcolor": "#2D2D4E"},
        height=420,
    )
    st.plotly_chart(fig_habit, use_container_width=True)

    st.markdown("<div class='section-title'>🔥 Current Streaks (consecutive days)</div>", unsafe_allow_html=True)
    streak_cols = st.columns(3)
    for i, habit in enumerate(HABITS):
        streak = compute_streak(data, habit)
        short = habit[:40]
        fire = "🔥" * min(streak, 5) if streak > 0 else "💤"
        streak_cols[i % 3].markdown(
            f"<div style='background:#1A1A2E; border:1px solid #2D2D4E; border-radius:10px; "
            f"padding:10px 14px; margin-bottom:10px;'>"
            f"<div style='font-size:0.8rem; color:#94A3B8;'>{short}</div>"
            f"<div style='font-size:1.1rem; font-weight:700; color:#A78BFA; margin-top:4px;'>"
            f"{fire} {streak} day{'s' if streak != 1 else ''}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    if len(data) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📈 Historical Weekly Scores</div>", unsafe_allow_html=True)
        weekly_scores = []
        for wk, habits in sorted(data.items()):
            done = sum(
                1
                for h in HABITS
                for d in DAYS
                if habits.get(h, {}).get(d, False)
            )
            score = round(done / (len(HABITS) * len(DAYS)) * 100, 1)
            weekly_scores.append({"Week": wk, "Score": score})

        df_hist = pd.DataFrame(weekly_scores)
        fig_hist = px.line(
            df_hist,
            x="Week",
            y="Score",
            markers=True,
            labels={"Score": "Productivity %"},
            color_discrete_sequence=["#A78BFA"],
        )
        fig_hist.update_traces(
            line={"width": 3},
            marker={"size": 8, "color": "#7C3AED"},
            fill="tozeroy",
            fillcolor="rgba(124,58,237,0.15)",
        )
        fig_hist.update_layout(
            plot_bgcolor="#12122A",
            paper_bgcolor="#12122A",
            font_color="#E2E8F0",
            yaxis={"range": [0, 105], "gridcolor": "#2D2D4E"},
            xaxis={"gridcolor": "#2D2D4E"},
            margin={"t": 10, "b": 10, "l": 10, "r": 10},
            height=300,
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Routine Tracker",
        page_icon="🌟",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_css()

    if "habit_data" not in st.session_state:
        st.session_state.habit_data = load_data()
    data = st.session_state.habit_data

    week_key = get_week_key()
    week_dates = get_week_dates()
    ensure_week_initialized(data, week_key)
    overall = get_completion_pct(data, week_key)

    with st.sidebar:
        st.markdown(
            "<div style='text-align:center; padding: 10px 0 20px 0;'>"
            "<div style='font-size:2.5rem;'>🌟</div>"
            "<div style='font-size:1.2rem; font-weight:800; color:#A78BFA;'>Routine Tracker</div>"
            "<div style='font-size:0.75rem; color:#64748B; margin-top:4px;'>Build. Track. Grow.</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        selected = option_menu(
            menu_title=None,
            options=["Tracker", "Analytics"],
            icons=["check2-square", "bar-chart-line"],
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "#A78BFA", "font-size": "18px"},
                "nav-link": {
                    "font-size": "15px",
                    "color": "#CBD5E1",
                    "border-radius": "8px",
                    "margin": "3px 0",
                },
                "nav-link-selected": {
                    "background-color": "#3B1A7A",
                    "color": "#fff",
                    "font-weight": "700",
                },
            },
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='background:#12122A; border:1px solid #2D2D4E; border-radius:10px; "
            f"padding:14px; text-align:center;'>"
            f"<div style='color:#94A3B8; font-size:0.78rem; margin-bottom:6px;'>THIS WEEK</div>"
            f"<div style='color:#A78BFA; font-size:2rem; font-weight:800;'>{overall}%</div>"
            f"<div style='color:#64748B; font-size:0.75rem;'>productivity score</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='color:#475569; font-size:0.72rem; text-align:center;'>"
            "Data saved locally · Resets never<br>"
            f"<span style='color:#7C3AED;'>{get_week_label()}</span>"
            "</div>",
            unsafe_allow_html=True,
        )

    if selected == "Tracker":
        show_tracker(data, week_key, week_dates, overall)
    else:
        show_analytics(data, week_key, overall)


main()
