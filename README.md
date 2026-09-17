# Mental Health in the Technology Workplace

An end-to-end exploratory data analysis and interactive Streamlit dashboard examining treatment-seeking behaviour, workplace support, employee attitudes, and statistical associations in the Mental Health in Tech Survey.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-22C55E)
Streamlit Dashboard[https://mainpy-56ciycdtkrtbymkqiywadu.streamlit.app/]
## Project overview

Mental health can influence employee wellbeing, productivity, retention, and psychological safety. This project turns 1,259 survey responses into a decision-oriented dashboard that identifies treatment patterns, workplace barriers, and gaps in employer support.

The project focuses on exploratory analysis and statistical association—not prediction. It does not require regression, classification, or clustering.

## Business objective

Help technology employers understand which workplace factors are associated with employees seeking mental-health treatment and identify practical opportunities to improve benefits, communication, anonymity, manager support, and psychological safety.

## Key findings

| KPI | Result |
|---|---:|
| Total respondents | 1,259 |
| Sought treatment | 50.60% |
| Mental-health benefits available | 37.89% |
| Family history reported | 39.08% |
| Remote workers | 29.86% |
| Expected negative consequences | 23.19% |

- Work interference had the strongest observed association with treatment-seeking (Cramér's V = 0.685).
- Family history was the next strongest association (Cramér's V = 0.377).
- Only 35.27% reported knowing about available care options.
- Anonymity was a major communication gap: 65.05% were unsure whether anonymity was protected.
- Almost one in four respondents expected negative workplace consequences for discussing mental health.

## Dashboard highlights

- Animated, filter-aware KPI cards
- Filters for country, gender, age, company size, remote work, and treatment
- Treatment, work-impact, employer-support, and workplace-attitude views
- Interactive Plotly charts with hover details
- Dynamic chi-square tests and Cramér's V effect-size analysis
- Country comparison and filtered-data download
- Responsive dark interface designed for portfolio presentation

## Statistical approach

The dashboard uses chi-square tests of independence for categorical variables and Cramér's V to describe association strength. Statistical significance is evaluated at an alpha level of 0.05.

These tests identify relationships in the survey sample; they do not establish causation and should not be interpreted as clinical evidence.

## Dataset and preparation

The cleaned dataset contains 1,259 responses and 25 analysis-ready fields. Preparation included:

- standardising column names and category labels;
- handling missing values with context-appropriate labels;
- grouping inconsistent gender entries into analysis categories;
- validating age values and creating age bands;
- preserving `no_employees` as text so `1-5` and `6-25` are not converted to dates;
- removing the dashboard's dependency on the original `timestamp` column;
- validating categorical values before building KPIs and charts.

## Repository structure

```text
mental-health-tech-workplace-analysis/
├── main.py
├── cleaned_mental_health_survey.csv
├── country_mental_health_summary.csv
├── employer_support_summary.csv
├── mental_health_kpi_summary.csv
├── treatment_association_results.csv
├── requirements.txt
├── README.md
└── Mental_Health_Tech_Workplace_Report.docx
```

## Technology stack

- Python
- pandas and NumPy
- Plotly
- Streamlit
- SciPy
- Jupyter Notebook

## Run locally

1. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   ```

   Windows: `.venv\Scripts\activate`

   macOS or Linux: `source .venv/bin/activate`

2. Install dependencies and launch the dashboard.

   ```bash
   pip install -r requirements.txt
   streamlit run main.py
   ```

## Recommended actions

1. Clearly communicate mental-health benefits and care pathways.
2. Publish and reinforce anonymity and confidentiality policies.
3. Train managers to respond consistently and without stigma.
4. Prioritise employees reporting frequent work interference.
5. Track treatment access, awareness, and perceived consequences over time.

## Limitations

- Responses are self-reported and do not represent clinical diagnoses.
- The sample is heavily concentrated in the United States and may not represent the global technology workforce.
- Most responses relate to a single survey period, so the analysis is not a current market benchmark.
- Chi-square tests and Cramér's V show association, not causation.
- Some categories were consolidated during cleaning, which improves analysis but reduces detail.

## Author

**Ankan Chowdhury**  
Data Analytics Project


