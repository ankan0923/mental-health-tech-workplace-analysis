from html import escape
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import chi2_contingency


st.set_page_config(
    page_title="MindScope | Mental Health in Tech",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).with_name("cleaned_mental_health_survey.csv")
NAVY = "#08111F"
CARD = "#101C2F"
BLUE = "#38BDF8"
TEAL = "#2DD4BF"
PURPLE = "#A78BFA"
AMBER = "#FBBF24"
RED = "#FB7185"
MUTED = "#94A3B8"
PALETTE = [BLUE, TEAL, PURPLE, AMBER, RED, "#60A5FA"]


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(56,189,248,.13), transparent 24%),
            radial-gradient(circle at 90% 4%, rgba(167,139,250,.12), transparent 22%),
            linear-gradient(145deg, #050A13 0%, #08111F 48%, #071525 100%);
        color: #F8FAFC;
    }
    .block-container { max-width: 1500px; padding-top: 1.4rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15,28,48,.98), rgba(7,17,31,.98));
        border-right: 1px solid rgba(148,163,184,.16);
    }
    [data-testid="stSidebar"] * { color: #E2E8F0; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255,255,255,.045); border-color: rgba(148,163,184,.22);
    }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    .hero {
        position: relative; overflow: hidden; padding: 32px 34px; margin-bottom: 20px;
        border: 1px solid rgba(125,211,252,.18); border-radius: 24px;
        background: linear-gradient(115deg, rgba(14,165,233,.18), rgba(45,212,191,.07) 48%, rgba(167,139,250,.13));
        box-shadow: 0 24px 70px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.06);
    }
    .hero:after {
        content: ''; position: absolute; width: 280px; height: 280px; right: -75px; top: -110px;
        background: radial-gradient(circle, rgba(56,189,248,.30), transparent 67%); border-radius: 50%;
    }
    .eyebrow { color: #7DD3FC; font-size: 12px; letter-spacing: .18em; font-weight: 800; text-transform: uppercase; }
    .hero h1 { margin: 8px 0 8px; font-size: clamp(30px, 4vw, 54px); line-height: 1.03; color: #F8FAFC; }
    .hero p { color: #B8C6D9; font-size: 15px; max-width: 760px; margin: 0; }
    .hero-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
    .hero-tag { padding: 7px 11px; border-radius: 999px; background: rgba(255,255,255,.065); border: 1px solid rgba(255,255,255,.09); color: #DCE9F8; font-size: 12px; }

    .kpi-card {
        position: relative; overflow: hidden; min-height: 168px; padding: 19px;
        border-radius: 20px; border: 1px solid rgba(148,163,184,.16);
        background: linear-gradient(145deg, rgba(19,34,55,.96), rgba(10,23,40,.93));
        box-shadow: 0 18px 38px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.04);
        transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: var(--accent); box-shadow: 0 22px 45px rgba(0,0,0,.32), 0 0 26px color-mix(in srgb, var(--accent) 16%, transparent); }
    .kpi-glow { position: absolute; width: 110px; height: 110px; right: -42px; top: -42px; background: var(--accent); opacity: .12; filter: blur(18px); border-radius: 50%; }
    .kpi-top { display: flex; align-items: center; justify-content: space-between; }
    .kpi-icon { display: grid; place-items: center; width: 42px; height: 42px; border-radius: 13px; background: color-mix(in srgb, var(--accent) 16%, transparent); font-size: 21px; }
    .kpi-chip { color: var(--accent); background: color-mix(in srgb, var(--accent) 11%, transparent); border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent); border-radius: 999px; padding: 4px 8px; font-size: 10px; font-weight: 800; }
    .kpi-label { color: #94A3B8; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .07em; margin-top: 13px; }
    .kpi-value { color: #F8FAFC; font-size: clamp(25px, 2.25vw, 38px); font-weight: 800; line-height: 1.05; margin-top: 5px; }
    .kpi-track { height: 5px; background: rgba(148,163,184,.13); border-radius: 8px; margin-top: 14px; overflow: hidden; }
    .kpi-fill { height: 100%; border-radius: 8px; background: linear-gradient(90deg, var(--accent), #E0F2FE); box-shadow: 0 0 12px var(--accent); }
    .kpi-note { color: #718096; font-size: 10px; margin-top: 7px; }

    .section-title { margin: 24px 0 12px; }
    .section-kicker { color: #38BDF8; text-transform: uppercase; font-size: 11px; font-weight: 800; letter-spacing: .15em; }
    .section-title h2 { color: #F8FAFC; font-size: 25px; margin: 4px 0; }
    .section-title p { color: #94A3B8; font-size: 13px; margin: 0; }

    .insight-card { padding: 18px 20px; border-radius: 16px; background: linear-gradient(120deg, rgba(56,189,248,.10), rgba(167,139,250,.08)); border: 1px solid rgba(125,211,252,.17); margin: 8px 0 16px; }
    .insight-card b { color: #7DD3FC; }
    .insight-card span { color: #CBD5E1; font-size: 13px; }
    .filter-count { padding: 12px 14px; border-radius: 13px; background: rgba(56,189,248,.08); border: 1px solid rgba(56,189,248,.15); color: #BAE6FD; font-size: 12px; }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: rgba(15,28,48,.65); border: 1px solid rgba(148,163,184,.13); border-radius: 15px; padding: 6px; }
    .stTabs [data-baseweb="tab"] { height: 43px; border-radius: 11px; padding: 0 18px; color: #94A3B8; font-weight: 700; }
    .stTabs [aria-selected="true"] { background: linear-gradient(100deg, rgba(56,189,248,.18), rgba(45,212,191,.12)); color: #F0F9FF; }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    [data-testid="stPlotlyChart"] { background: linear-gradient(145deg, rgba(16,28,47,.93), rgba(8,19,34,.92)); border: 1px solid rgba(148,163,184,.14); border-radius: 20px; padding: 10px; box-shadow: 0 15px 35px rgba(0,0,0,.18); }
    .stDownloadButton button { border: 0; border-radius: 12px; background: linear-gradient(90deg, #0EA5E9, #14B8A6); color: white; font-weight: 800; padding: .65rem 1.25rem; box-shadow: 0 10px 25px rgba(14,165,233,.22); }
    hr { border-color: rgba(148,163,184,.13); }
    @media (max-width: 900px) { .hero { padding: 24px; } .kpi-card { min-height: 150px; } }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)

    # The cleaned CSV already contains standardized gender groups.
    if "gender_group" in df.columns:
        df = df.rename(columns={"gender_group": "gender_clean"})

    # Remove the Excel/WPS protection wrapper: ="6-25" becomes 6-25.
    df["no_employees"] = (
        df["no_employees"]
        .astype(str)
        .str.strip()
        .str.replace('="', "", regex=False)
        .str.replace('"', "", regex=False)
    )

    # Validate and complete Age before rebuilding Age Group.
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df.loc[~df["age"].between(18, 75), "age"] = np.nan
    df["age"] = df["age"].fillna(df["age"].median()).astype(int)
    df["age_group"] = pd.cut(
        df["age"], [17, 24, 34, 44, 54, 64, 75],
        labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65-75"],
        include_lowest=True,
    )

    df["country"] = df["country"].fillna("Unknown").astype(str).str.strip()
    df["state"] = df["state"].fillna("Unknown")
    df.loc[df["country"] != "United States", "state"] = "Not Applicable"
    df["self_employed"] = df["self_employed"].fillna("Unknown")
    df["work_interfere"] = df["work_interfere"].fillna("Not Applicable/Unknown")

    required_columns = [
        "age", "age_group", "gender_clean", "country", "treatment",
        "benefits", "work_interfere", "no_employees",
    ]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Required columns are missing: {missing_columns}")

    return df


def chart_style(fig, height=410):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#CBD5E1", size=12),
        title=dict(font=dict(color="#F8FAFC", size=17), x=0.03, y=0.95),
        margin=dict(l=35, r=25, t=65, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.18, x=0),
        hoverlabel=dict(bgcolor="#0F1C30", font_color="#F8FAFC", bordercolor="#334155"),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,.10)", zeroline=False, title_font_color=MUTED)
    fig.update_yaxes(gridcolor="rgba(148,163,184,.10)", zeroline=False, title_font_color=MUTED)
    return fig


def count_bar(df, column, title, order=None, horizontal=False):
    counts = df[column].value_counts().rename_axis(column).reset_index(name="Respondents")
    if order:
        counts[column] = pd.Categorical(counts[column], categories=order, ordered=True)
        counts = counts.sort_values(column)
    if horizontal:
        fig = px.bar(counts, x="Respondents", y=column, orientation="h", text="Respondents", color="Respondents", color_continuous_scale=["#163A5F", BLUE])
        fig.update_layout(coloraxis_showscale=False, yaxis_title="")
    else:
        fig = px.bar(counts, x=column, y="Respondents", text="Respondents", color=column, color_discrete_sequence=PALETTE)
        fig.update_layout(showlegend=False, xaxis_title="")
    fig.update_traces(textposition="outside", marker_line_width=0, hovertemplate="%{x}<br>Respondents: %{y}<extra></extra>")
    fig.update_layout(title=title)
    return chart_style(fig)


def percentage_bar(df, group, title, order=None):
    table = pd.crosstab(df[group], df["treatment"], normalize="index").mul(100).reset_index()
    frame = table.melt(id_vars=group, var_name="Treatment", value_name="Percentage")
    if order:
        frame[group] = pd.Categorical(frame[group], categories=order, ordered=True)
        frame = frame.sort_values(group)
    frame["Label"] = frame["Percentage"].map(lambda x: f"{x:.1f}%")
    fig = px.bar(frame, x=group, y="Percentage", color="Treatment", barmode="stack", text="Label", color_discrete_map={"Yes": TEAL, "No": "#2563EB"})
    fig.update_layout(title=title, xaxis_title="", yaxis_title="Share of respondents", yaxis_range=[0, 100])
    fig.update_traces(hovertemplate="%{x}<br>%{fullData.name}: %{y:.1f}%<extra></extra>")
    return chart_style(fig)


def donut(series, title, colors=PALETTE):
    counts = series.value_counts().reset_index()
    counts.columns = ["Response", "Respondents"]
    fig = px.pie(counts, names="Response", values="Respondents", hole=.70, color_discrete_sequence=colors)
    fig.update_traces(textinfo="percent+label", textposition="outside", pull=[.03] * len(counts), marker=dict(line=dict(color=NAVY, width=2)))
    fig.add_annotation(text=f"<b>{counts['Respondents'].sum():,}</b><br><span style='font-size:10px'>responses</span>", x=.5, y=.5, showarrow=False, font=dict(color="#F8FAFC", size=18))
    fig.update_layout(title=title, showlegend=False)
    return chart_style(fig)


def kpi_card(icon, label, value, accent, progress, note, chip):
    progress = max(0, min(float(progress), 100))
    return f"""
    <div class="kpi-card" style="--accent:{accent}">
      <div class="kpi-glow"></div>
      <div class="kpi-top"><div class="kpi-icon">{icon}</div><div class="kpi-chip">{escape(chip)}</div></div>
      <div class="kpi-label">{escape(label)}</div>
      <div class="kpi-value">{escape(value)}</div>
      <div class="kpi-track"><div class="kpi-fill" style="width:{progress:.1f}%"></div></div>
      <div class="kpi-note">{escape(note)}</div>
    </div>
    """


def section(kicker, title, description):
    st.markdown(
        f'<div class="section-title"><div class="section-kicker">{escape(kicker)}</div><h2>{escape(title)}</h2><p>{escape(description)}</p></div>',
        unsafe_allow_html=True,
    )


def cramers_v(first, second):
    table = pd.crosstab(first, second)
    if table.shape[0] < 2 or table.shape[1] < 2:
        return np.nan, np.nan, np.nan
    chi2, p_value, dof, _ = chi2_contingency(table)
    n = table.to_numpy().sum()
    rows, columns = table.shape
    phi2 = chi2 / n
    corrected_phi2 = max(0, phi2 - ((columns - 1) * (rows - 1)) / (n - 1))
    corrected_rows = rows - ((rows - 1) ** 2) / (n - 1)
    corrected_columns = columns - ((columns - 1) ** 2) / (n - 1)
    denominator = min(corrected_rows - 1, corrected_columns - 1)
    value = np.sqrt(corrected_phi2 / denominator) if denominator > 0 else 0
    return value, p_value, dof


def association_strength(value):
    if pd.isna(value):
        return "Unavailable"
    if value < 0.10:
        return "Very weak"
    if value < 0.20:
        return "Weak"
    if value < 0.40:
        return "Moderate"
    if value < 0.60:
        return "Strong"
    return "Very strong"


def calculate_associations(df):
    candidates = {
        "Work interference": "work_interfere",
        "Family history": "family_history",
        "Care options": "care_options",
        "Benefits": "benefits",
        "Gender": "gender_clean",
        "Observed consequences": "obs_consequence",
        "Ease of leave": "leave",
        "Anonymity": "anonymity",
        "Supervisor comfort": "supervisor",
        "Coworker comfort": "coworkers",
        "Help resources": "seek_help",
        "Wellness program": "wellness_program",
        "Company size": "no_employees",
        "Remote work": "remote_work",
        "Age group": "age_group",
    }
    results = []
    for label, column in candidates.items():
        value, p_value, dof = cramers_v(df[column], df["treatment"])
        if not pd.isna(value):
            results.append({
                "Factor": label,
                "Column": column,
                "Cramer's V": value,
                "Association": association_strength(value),
                "P-value": p_value,
                "Degrees of freedom": dof,
                "Significant": "Yes" if p_value < 0.05 else "No",
            })
    return pd.DataFrame(results).sort_values("Cramer's V", ascending=False).reset_index(drop=True)


try:
    data = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"{DATA_PATH.name} was not found. "
        f"Keep {DATA_PATH.name} and main.py in the same folder."
    )
    st.stop()
except ValueError as error:
    st.error(str(error))
    st.stop()


with st.sidebar:
    st.markdown("## 🧠 MindScope")
    st.caption("Interactive survey intelligence")
    st.divider()
    st.markdown("### Filter the story")
    countries = st.multiselect("Country", sorted(data["country"].unique()), placeholder="All countries")
    genders = st.multiselect("Gender", sorted(data["gender_clean"].unique()), placeholder="All genders")
    age_groups = st.multiselect("Age group", [str(v) for v in data["age_group"].cat.categories], placeholder="All ages")
    companies = st.multiselect("Company size", sorted(data["no_employees"].unique()), placeholder="All company sizes")
    remote = st.multiselect("Remote work", sorted(data["remote_work"].unique()), placeholder="All work modes")
    tech = st.multiselect("Tech company", sorted(data["tech_company"].unique()), placeholder="All employers")
    st.divider()
    st.caption("Every chart and KPI updates with your selection.")


filtered = data.copy()
filter_map = {
    "country": countries,
    "gender_clean": genders,
    "no_employees": companies,
    "remote_work": remote,
    "tech_company": tech,
}
for column, values in filter_map.items():
    if values:
        filtered = filtered[filtered[column].isin(values)]
if age_groups:
    filtered = filtered[filtered["age_group"].astype(str).isin(age_groups)]
if filtered.empty:
    st.warning("No responses match these filters. Remove one or more selections.")
    st.stop()


total = len(filtered)
treatment_rate = filtered["treatment"].eq("Yes").mean() * 100
benefits_rate = filtered["benefits"].eq("Yes").mean() * 100
median_age = filtered["age"].median()
consequence_rate = filtered["mental_health_consequence"].eq("Yes").mean() * 100
support_awareness = filtered["care_options"].eq("Yes").mean() * 100
active_filters = sum(bool(v) for v in [countries, genders, age_groups, companies, remote, tech])


st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">2014 Technology Workplace Survey</div>
      <h1>Workplace Mental Health<br>Intelligence Dashboard</h1>
      <p>Explore treatment-seeking behaviour, employee confidence and the workplace systems that shape access to mental-health support.</p>
      <div class="hero-tags"><span class="hero-tag">Interactive EDA</span><span class="hero-tag">Employee Wellbeing</span><span class="hero-tag">Policy Awareness</span><span class="hero-tag">Portfolio Project</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

if active_filters:
    st.markdown(f'<div class="filter-count">✦ {active_filters} active filter group(s) · Showing <b>{total:,}</b> of {len(data):,} survey responses</div>', unsafe_allow_html=True)

section("Executive pulse", "Five signals that frame the story", "A quick health check of the currently selected workforce segment.")
cols = st.columns(5)
cards = [
    ("👥", "Respondents", f"{total:,}", BLUE, total / len(data) * 100, f"{total / len(data) * 100:.1f}% of full survey", "SAMPLE"),
    ("🩺", "Sought treatment", f"{treatment_rate:.1f}%", TEAL, treatment_rate, "Self-reported treatment seeking", "ACCESS"),
    ("🛡️", "Benefits available", f"{benefits_rate:.1f}%", PURPLE, benefits_rate, "Reported employer coverage", "SUPPORT"),
    ("🎂", "Median age", f"{median_age:.0f}", AMBER, median_age / 75 * 100, "Median within selected group", "PROFILE"),
    ("⚠️", "Expected consequences", f"{consequence_rate:.1f}%", RED, consequence_rate, "Fear of negative workplace impact", "RISK"),
]
for col, card in zip(cols, cards):
    with col:
        st.markdown(kpi_card(*card), unsafe_allow_html=True)

highest_interference = filtered["work_interfere"].value_counts().idxmax()
st.markdown(
    f'<div class="insight-card"><b>Live insight:</b> <span>{treatment_rate:.1f}% sought treatment, while only {benefits_rate:.1f}% report available benefits. The most common work-interference response is <b>{escape(str(highest_interference))}</b>, and {100-support_awareness:.1f}% are either unaware of or uncertain about their care options.</span></div>',
    unsafe_allow_html=True,
)

overview, treatment, support, attitudes, statistics = st.tabs([
    "◉ Overview",
    "✚ Treatment & impact",
    "◆ Employer support",
    "◎ Workplace attitudes",
    "Σ Statistical evidence",
])

with overview:
    section("Who responded", "Workforce profile", "Understand the population behind every percentage before interpreting the findings.")
    c1, c2 = st.columns([1.05, .95])
    with c1:
        age_fig = px.histogram(filtered, x="age", nbins=20, color_discrete_sequence=[BLUE], marginal="box")
        age_fig.update_traces(marker_line_width=0, opacity=.88)
        age_fig.update_layout(title="Age distribution", xaxis_title="Age", yaxis_title="Respondents")
        st.plotly_chart(chart_style(age_fig, 430), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(donut(filtered["gender_clean"], "Gender composition", [BLUE, TEAL, PURPLE]), use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns([1.1, .9])
    with c1:
        country_counts = filtered["country"].value_counts().head(10).sort_values().rename_axis("Country").reset_index(name="Respondents")
        country_fig = px.bar(country_counts, x="Respondents", y="Country", orientation="h", text="Respondents", color="Respondents", color_continuous_scale=["#163A5F", BLUE])
        country_fig.update_layout(title="Top 10 countries", coloraxis_showscale=False, yaxis_title="")
        country_fig.update_traces(textposition="outside")
        st.plotly_chart(chart_style(country_fig), use_container_width=True, config={"displayModeBar": False})
    with c2:
        company_order = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
        st.plotly_chart(count_bar(filtered, "no_employees", "Company size", company_order), use_container_width=True, config={"displayModeBar": False})

with treatment:
    section("Behaviour & impact", "Treatment-seeking patterns", "Compare treatment behaviour with family history, age and reported work interference.")
    c1, c2 = st.columns([.8, 1.2])
    with c1:
        st.plotly_chart(donut(filtered["treatment"], "Treatment status", [TEAL, "#2563EB"]), use_container_width=True, config={"displayModeBar": False})
    with c2:
        work_order = ["Never", "Rarely", "Sometimes", "Often", "Not Applicable/Unknown"]
        st.plotly_chart(count_bar(filtered, "work_interfere", "Mental health interference with work", work_order), use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(percentage_bar(filtered, "family_history", "Treatment by family history", ["No", "Yes"]), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(percentage_bar(filtered, "age_group", "Treatment by age group"), use_container_width=True, config={"displayModeBar": False})

    matrix = pd.crosstab(filtered["work_interfere"], filtered["treatment"], normalize="index").mul(100).reindex(work_order).fillna(0)
    heat = go.Figure(go.Heatmap(z=matrix.values, x=matrix.columns, y=matrix.index, colorscale=[[0, "#10263D"], [.5, "#2563EB"], [1, "#2DD4BF"]], text=np.round(matrix.values, 1), texttemplate="%{text}%", hovertemplate="%{y}<br>Treatment %{x}: %{z:.1f}%<extra></extra>"))
    heat.update_layout(title="Treatment share across work-interference levels", xaxis_title="Sought treatment", yaxis_title="Work interference")
    st.plotly_chart(chart_style(heat, 390), use_container_width=True, config={"displayModeBar": False})

with support:
    section("Access & clarity", "Employer support ecosystem", "Separate actual support coverage from employee awareness of that support.")
    support_columns = {
        "Benefits": "benefits",
        "Care options": "care_options",
        "Wellness program": "wellness_program",
        "Help resources": "seek_help",
        "Anonymity": "anonymity",
    }
    support_rows = []
    for label, column in support_columns.items():
        support_rows.append({"Support area": label, "Yes": filtered[column].eq("Yes").mean() * 100, "Uncertain": filtered[column].isin(["Don't know", "Not sure"]).mean() * 100})
    support_df = pd.DataFrame(support_rows)
    support_long = support_df.melt("Support area", var_name="Response signal", value_name="Percentage")
    support_fig = px.bar(support_long, x="Support area", y="Percentage", color="Response signal", barmode="group", text_auto=".1f", color_discrete_map={"Yes": TEAL, "Uncertain": AMBER})
    support_fig.update_layout(title="Coverage versus uncertainty", xaxis_title="", yaxis_title="Percentage", yaxis_range=[0, 100])
    support_fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
    st.plotly_chart(chart_style(support_fig, 440), use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns([.95, 1.05])
    with c1:
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=benefits_rate, number={"suffix": "%", "font": {"color": "#F8FAFC", "size": 44}}, title={"text": "Reported benefits coverage", "font": {"color": MUTED}}, gauge={"axis": {"range": [0, 100], "tickcolor": MUTED}, "bar": {"color": PURPLE}, "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0, "steps": [{"range": [0, 40], "color": "rgba(251,113,133,.13)"}, {"range": [40, 70], "color": "rgba(251,191,36,.13)"}, {"range": [70, 100], "color": "rgba(45,212,191,.13)"}]}))
        st.plotly_chart(chart_style(gauge, 390), use_container_width=True, config={"displayModeBar": False})
    with c2:
        leave_order = ["Very easy", "Somewhat easy", "Somewhat difficult", "Very difficult", "Don't know"]
        st.plotly_chart(count_bar(filtered, "leave", "Ease of taking mental-health leave", leave_order), use_container_width=True, config={"displayModeBar": False})

with attitudes:
    section("Trust & disclosure", "Workplace attitudes", "Measure the distance between support on paper and psychological safety in practice.")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(donut(filtered["mental_health_consequence"], "Expected negative consequences", [TEAL, AMBER, RED]), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(donut(filtered["anonymity"], "Confidence in anonymity", [TEAL, AMBER, RED]), use_container_width=True, config={"displayModeBar": False})

    discussion = []
    for audience, column in {"Coworkers": "coworkers", "Supervisors": "supervisor"}.items():
        for response, value in filtered[column].value_counts(normalize=True).mul(100).items():
            discussion.append({"Audience": audience, "Response": response, "Percentage": value})
    discussion_df = pd.DataFrame(discussion)
    discuss_fig = px.bar(discussion_df, x="Audience", y="Percentage", color="Response", barmode="group", text_auto=".1f", color_discrete_sequence=[TEAL, AMBER, RED])
    discuss_fig.update_layout(title="Comfort discussing mental health", yaxis_title="Percentage", yaxis_range=[0, 100])
    discuss_fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
    st.plotly_chart(chart_style(discuss_fig, 420), use_container_width=True, config={"displayModeBar": False})

    interview_rows = []
    for topic, column in {"Mental health": "mental_health_interview", "Physical health": "phys_health_interview"}.items():
        for response in ["Yes", "Maybe", "No"]:
            interview_rows.append({"Health topic": topic, "Response": response, "Percentage": filtered[column].eq(response).mean() * 100})
    interview_df = pd.DataFrame(interview_rows)
    interview_fig = px.bar(interview_df, x="Response", y="Percentage", color="Health topic", barmode="group", text_auto=".1f", color_discrete_map={"Mental health": PURPLE, "Physical health": TEAL})
    interview_fig.update_layout(title="Willingness to discuss health during interviews", yaxis_title="Percentage", yaxis_range=[0, 100])
    interview_fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
    st.plotly_chart(chart_style(interview_fig, 420), use_container_width=True, config={"displayModeBar": False})


with statistics:
    section(
        "Statistical evidence",
        "Factors associated with treatment",
        "Chi-square tests assess dependence. Cramér's V measures the strength of each categorical association.",
    )

    if len(filtered) < 30:
        st.warning("The current filter contains fewer than 30 responses. Statistical results may be unstable.")

    association_df = calculate_associations(filtered)

    if association_df.empty:
        st.warning("The selected filters do not contain enough category variation for statistical testing.")
    else:
        strongest = association_df.iloc[0]
        strongest_v = float(strongest["Cramer's V"])
        significant_count = int(association_df["Significant"].eq("Yes").sum())

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.markdown(kpi_card("Σ", "Factors tested", f"{len(association_df)}", BLUE, 100, "Compared with treatment status", "TESTS"), unsafe_allow_html=True)
        with s2:
            st.markdown(kpi_card("✓", "Significant factors", f"{significant_count}", TEAL, significant_count / len(association_df) * 100, "Based on p < 0.05", "EVIDENCE"), unsafe_allow_html=True)
        with s3:
            st.markdown(kpi_card("◆", "Strongest factor", str(strongest["Factor"]), PURPLE, strongest_v * 100, association_strength(strongest_v), "TOP LINK"), unsafe_allow_html=True)
        with s4:
            st.markdown(kpi_card("V", "Cramér's V", f"{strongest_v:.3f}", AMBER, strongest_v * 100, "0 = none, 1 = strongest", "STRENGTH"), unsafe_allow_html=True)

        top_associations = association_df.head(10).sort_values("Cramer's V")
        association_fig = px.bar(
            top_associations,
            x="Cramer's V",
            y="Factor",
            orientation="h",
            color="Cramer's V",
            text="Association",
            color_continuous_scale=["#163A5F", BLUE, TEAL],
        )
        association_fig.update_layout(
            title="Association strength with treatment status",
            coloraxis_showscale=False,
            xaxis_title="Cramér's V",
            yaxis_title="",
            xaxis_range=[0, max(0.75, top_associations["Cramer's V"].max() + 0.05)],
        )
        association_fig.update_traces(textposition="outside", hovertemplate="%{y}<br>Cramér's V: %{x:.3f}<extra></extra>")
        st.plotly_chart(chart_style(association_fig, 470), use_container_width=True, config={"displayModeBar": False})

        c1, c2 = st.columns([1.15, .85])
        with c1:
            display_table = association_df[["Factor", "Cramer's V", "Association", "P-value", "Significant"]].copy()
            display_table["Cramer's V"] = display_table["Cramer's V"].round(3)
            display_table["P-value"] = display_table["P-value"].map(lambda x: "<0.0001" if x < 0.0001 else f"{x:.4f}")
            st.markdown("#### Statistical test results")
            st.dataframe(
                display_table,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Cramer's V": st.column_config.ProgressColumn("Cramér's V", min_value=0, max_value=1, format="%.3f"),
                    "Significant": st.column_config.TextColumn("Significant at 5%"),
                },
            )
        with c2:
            st.markdown("#### Inspect one relationship")
            selected_factor = st.selectbox("Factor", association_df["Factor"].tolist(), label_visibility="collapsed")
            selected = association_df.loc[association_df["Factor"] == selected_factor].iloc[0]
            selected_v = float(selected["Cramer's V"])
            selected_p = float(selected["P-value"])
            selected_column = selected["Column"]
            selected_table = pd.crosstab(filtered[selected_column], filtered["treatment"], normalize="index").mul(100).round(1)
            selected_fig = px.imshow(
                selected_table,
                text_auto=".1f",
                aspect="auto",
                color_continuous_scale=["#10263D", "#2563EB", TEAL],
                labels={"x": "Treatment", "y": selected_factor, "color": "%"},
            )
            selected_fig.update_traces(hovertemplate="%{y}<br>Treatment %{x}: %{z:.1f}%<extra></extra>")
            st.plotly_chart(chart_style(selected_fig, 330), use_container_width=True, config={"displayModeBar": False})
            p_label = "<0.0001" if selected_p < 0.0001 else f"{selected_p:.4f}"
            significance_text = "statistically significant" if selected["Significant"] == "Yes" else "not statistically significant"
            st.markdown(
                f'<div class="insight-card"><b>{escape(selected_factor)}</b><br><span>'
                f'Cramér\'s V = {selected_v:.3f} ({selected["Association"].lower()}). '
                f'Chi-square p-value = {p_label}. This relationship is {significance_text} at the 5% level.'
                f'</span></div>',
                unsafe_allow_html=True,
            )

        with st.expander("How to interpret the statistical section"):
            st.markdown(
                """
                - **Chi-square test:** checks whether two categorical variables are statistically associated.
                - **P-value below 0.05:** provides evidence of an association in this survey sample.
                - **Cramér's V:** measures association strength from 0 to 1.
                - The results show association, not causation. Treatment is self-reported rather than a diagnosis.
                """
            )

        st.download_button(
            "Download current statistical results",
            association_df.drop(columns="Column").to_csv(index=False).encode("utf-8"),
            "filtered_treatment_associations.csv",
            "text/csv",
            use_container_width=True,
        )


st.divider()
c1, c2 = st.columns([1.2, .8])
with c1:
    st.markdown("### Export your filtered view")
    st.caption("Download the same records currently represented by the dashboard.")
with c2:
    st.download_button("⬇ Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_mental_health_survey.csv", "text/csv", use_container_width=True)

st.info("Educational survey analysis only. Treatment is self-reported, not a medical diagnosis, and observed associations do not establish causation.")
