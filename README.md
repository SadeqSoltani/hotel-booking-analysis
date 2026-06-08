# Hotel Booking Demand Analysis

> A complete end-to-end data analytics project analyzing 119,390 hotel bookings to uncover the drivers of cancellation, quantify $16.9M in revenue leakage, and deploy a machine learning model that predicts cancellation risk with 95.29% ROC-AUC.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-ROC--AUC%2095.29%25-FF6600?style=flat)](https://xgboost.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://hotel-booking-cancellation-risk-predictor.streamlit.app)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=powerbi&logoColor=black)]()
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white)]()

---

## Table of Contents

- [Project Overview](#project-overview)
- [Live Demo](#live-demo)
- [Key Metrics](#key-metrics)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Database Design](#database-design)
- [Key Findings](#key-findings)
- [Machine Learning Model](#machine-learning-model)
- [Power BI Dashboard](#power-bi-dashboard)
- [Strategic Recommendations](#strategic-recommendations)
- [Getting Started](#getting-started)
- [Dataset](#dataset)
- [Author](#author)

---

## Project Overview

Hotel cancellations are one of the most damaging and preventable sources of revenue loss in the hospitality industry. This project performs a full-stack data analysis of **119,390 bookings** across two Portuguese hotels — a City Hotel and a Resort Hotel — spanning July 2015 to August 2017.

The project moves through five analytical layers:

- **SQL** — 10 structured business questions answered against a normalized SQLite database
- **ETL & Data Engineering** — raw CSV transformed into a clean 46-column analytical dataset
- **Exploratory Analysis** — statistical profiling, distribution analysis, and correlation mapping
- **Business Intelligence** — deep-dive analysis across booking timeline, hotel performance, market segments, pricing, geography, and cancellation drivers
- **Machine Learning** — XGBoost cancellation predictor deployed as an interactive Streamlit web application

The Power BI dashboard serves as the stakeholder communication layer — translating all findings from SQL and Python into an interactive 6-page visual story for hotel management.

---

## Live Demo

**Cancellation Risk Predictor:** [hotel-booking-cancellation-risk-predictor.streamlit.app](https://hotel-booking-cancellation-risk-predictor.streamlit.app)

Enter booking details and receive an instant cancellation probability score powered by the trained XGBoost model.

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Bookings Analyzed | 119,390 |
| Date Range | July 2015 – August 2017 |
| Hotel Types | City Hotel · Resort Hotel |
| Overall Cancellation Rate | 37.0% |
| City Hotel Cancellation Rate | 41.73% |
| Resort Hotel Cancellation Rate | 27.76% |
| Total Confirmed Revenue | $25,996,306 |
| Revenue Lost to Cancellations | ~$16.9M |
| Average Daily Rate (ADR) | $100 |
| ML Model ROC-AUC | 95.29% |
| Countries Represented | 177 |
| Top Source Market | Portugal (48,590 bookings) |

---

## Project Structure

```
Hotel_Booking/
│
├── screenshots/                        # Power BI dashboard screenshots
│   ├── 01_executive_summary.png
│   ├── 02_booking_timeline.png
│   ├── 03_hotel_segment.png
│   ├── 04_cancellation_deep_dive.png
│   ├── 05_revenue_pricing.png
│   └── 06_geographic_analysis.png
│
├── data/
│   ├── hotel_bookings.csv              # Raw dataset (119,390 rows, 32 columns)
│   ├── hotel_bookings.db               # Normalized SQLite database (3 tables)
│   └── hotel_bookings_clean.csv        # Engineered dataset (46 columns)
│
├── notebooks/
│   ├── 01_database_setup.ipynb         # SQLite schema and data normalization
│   ├── 02_etl_cleaning.ipynb           # ETL pipeline and feature engineering
│   ├── 03_eda_statistics.ipynb         # Exploratory data analysis
│   ├── 04_business_analysis.ipynb      # Business intelligence and insights
│   └── 05_machine_learning.ipynb       # Model training, evaluation, deployment
│
├── sql/
│   ├── queries.sql                     # 10 business SQL queries with context
│   └── results/                        # Query output screenshots
│
├── models/
│   ├── xgb_model.pkl                   # Trained XGBoost classifier
│   ├── cat_mappings.pkl                # Categorical label encodings
│   └── feature_columns.pkl             # Ordered feature list for inference
│
├── dashboard/
│   └── Hotel_booking.pbix              # Power BI Desktop file (6 pages)
│
├── app.py                              # Streamlit web application
├── requirements.txt                    # Python dependencies
└── .gitignore
```

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.9+ |
| Database | SQLite3 |
| Data Processing | Pandas, NumPy |
| Machine Learning | XGBoost, LightGBM, Scikit-learn |
| Model Persistence | Joblib |
| Web Application | Streamlit |
| Business Intelligence | Power BI Desktop |
| Development | Jupyter Notebook, VS Code |

---

## Database Design

The raw CSV was normalized into a SQLite relational database with three tables joined on `booking_id`:

```
bookings (booking_id PK)
├── hotel, is_canceled, lead_time
├── arrival_date_year/month/week/day
├── stays_in_weekend_nights, stays_in_week_nights
├── adr, booking_changes, days_in_waiting_list
├── required_car_parking_spaces, total_of_special_requests
└── reservation_status, reservation_status_date

customers (booking_id FK → bookings)
├── country, is_repeated_guest
├── previous_cancellations, previous_bookings_not_canceled
└── adults, children, babies

reservations (booking_id FK → bookings)
├── meal, market_segment, distribution_channel
├── reserved_room_type, assigned_room_type
├── deposit_type, agent, company
└── customer_type
```

### 10 Business Questions Answered with SQL

| # | Business Question | Key Result |
|---|-------------------|------------|
| Q1 | Which hotel type has the higher cancellation rate? | City Hotel 41.73% vs Resort Hotel 27.76% |
| Q2 | How has ADR changed year over year by hotel type? | City Hotel grew 37% ($85.86→$117.50). Resort spiked in 2017 |
| Q3 | Which market segment loses the most cancellation revenue? | Online TA $10.2M lost. Groups worst rate at 61.06% |
| Q4 | Top countries by bookings — cancellation rate and ADR? | Portugal 56.64% cancellation at $92 ADR — worst quality market |
| Q5 | Which deposit type has the highest cancellation rate? | Non Refund 99.36% — revenue retained despite cancellation flag |
| Q6 | Monthly booking trends across 2015–2017? | August 2017 peak ADR $164.25. Peak months 40–45% cancellation |
| Q7 | Does lead time affect cancellation rate? | Linear: same-day 6.78% → 180+ days 57.01% |
| Q8 | Do repeat guests behave differently from new guests? | Repeat guests 14.49% cancellation vs new guests 37.79% |
| Q9 | Does room mismatch affect cancellation? | Room-changed guests cancel at only 5.38% vs 41.56% for matched |
| Q10 | Do high-value bookings cancel more? | Uniform 34–38% across all tiers. Q4 loss $796 vs Q1 $97 — 8x impact |

---

## Key Findings

All findings are derived from SQL analysis and business intelligence notebooks, then validated through Power BI visualization. Organized by theme.

---

### Cancellation Is a Structural Problem, Not a Seasonal One

The 37% overall cancellation rate remains flat across all 12 months with no meaningful seasonal variation. City Hotel exceeds 37% every single month without exception. This eliminates seasonality as an explanation and confirms a structural problem driven by booking policy, deposit requirements, and channel mix — requiring permanent intervention rather than seasonal adjustments.

SQL confirmed the 14-point gap between City Hotel (41.73%) and Resort Hotel (27.76%), driven by fundamentally different guest profiles. City hotels attract volatile business travelers who book multiple options simultaneously. Resort bookings represent committed leisure trips with longer planning horizons and higher emotional investment.

---

### Lead Time Is the Strongest and Most Actionable Cancellation Driver

A near-perfect linear relationship exists between advance booking window and cancellation probability:

| Lead Time | Bookings | Cancellation Rate |
|-----------|---------|-------------------|
| Same day | 6,345 | 6.78% |
| 1–7 days | 13,401 | 10.98% |
| 8–30 days | 18,960 | 27.86% |
| 31–90 days | 29,553 | 37.70% |
| 91–180 days | 26,439 | 44.71% |
| 180+ days | 24,692 | 57.01% |

Guests who book 180+ days in advance cancel at 57% — more than 8x the rate of same-day bookers. Longer time horizons give guests more opportunity for plans to change. This became the single most important feature in the XGBoost model and directly informs the tiered deposit policy recommendation.

---

### Special Requests Are the Strongest Commitment Signal

Guests with zero special requests cancel at 47.7%. Guests who make 3 or more requests cancel at only 16.8% — a 31-point gap. Guests who communicate specific preferences are emotionally invested in the stay and rarely cancel. This is both one of the top ML predictive features and a highly actionable operational lever: proactively soliciting guest preferences at booking converts passive reservations into committed stays.

---

### The Non-Refundable Deposit Paradox

Non-refundable deposit bookings show a 99.36% cancellation rate — the most counterintuitive finding in the dataset. The explanation: hotels record these as cancelled even when the deposit is retained, meaning revenue is fully protected regardless of the cancellation flag. The true behavioural cancellation risk lies in No Deposit bookings at 28.38%, representing 104,641 bookings. Expanding non-refundable rate options for high-risk segments protects revenue without reducing booking volume.

---

### Resort Hotel Is a Summer-Dependent Business

Resort Hotel ADR reaches $186 in Summer versus $57 in Winter — a 170% seasonal swing that creates serious cash flow vulnerability. City Hotel maintains stable ADR of $85–$118 year-round, driven by consistent business travel demand.

By 2017, City Hotel commands a $9 ADR premium over Resort Hotel ($117.50 vs $108.66) — unusual since resorts typically charge more. This reflects stronger urban demand growth and City Hotel's consistent pricing power.

Despite lower ADR, Resort Hotel generates higher revenue per completed booking ($400.90 vs $311.40) because longer average stays (4.3 vs 3.0 nights) outweigh the rate disadvantage. However, this advantage disappears entirely if summer demand softens. Summer alone generates 45% of annual revenue — a dangerous concentration in a single season.

---

### Online TA Is the Largest Revenue Source and the Largest Single Risk

| Market Segment | Bookings | Cancellation Rate | ADR | Revenue Lost |
|---------------|---------|-------------------|-----|-------------|
| Online TA | 56,477 | 36.72% | $117.20 | $10,227,646 |
| Groups | 19,811 | 61.06% | $79.48 | $2,880,544 |
| Offline TA/TO | 24,219 | 34.32% | $87.35 | $2,492,358 |
| Direct | 12,606 | 15.34% | $115.45 | $993,410 |
| Corporate | 5,295 | 18.73% | $69.36 | $196,383 |

Online TA accounts for 61% of all cancellation revenue loss ($10.2M of $16.9M total). Direct bookings match Online TA ADR ($114 vs $114) with half the cancellation rate (15.3% vs 36.7%) and zero OTA commission — making direct booking conversion the single highest-ROI channel strategy available.

Groups represent the worst risk-return profile in the entire dataset: lowest ADR ($79) combined with the highest cancellation rate (61.06%). Six in ten group bookings cancel.

---

### Portugal Concentration Is a Hidden Revenue Quality Risk

Portugal accounts for 41% of all bookings (48,590) but delivers the worst quality metrics of any major market: the lowest ADR among top countries ($92.04) and the highest cancellation rate (56.64%). Over half of all Portuguese bookings cancel.

Meanwhile the ideal guest markets are being underserved:

| Country | Bookings | Cancellation Rate | ADR |
|---------|---------|-------------------|-----|
| Portugal | 48,590 | 56.64% | $92.04 |
| Germany | 7,287 | 16.71% | $104.40 |
| France | 10,415 | 18.57% | $109.62 |
| USA | 2,097 | 23.90% | $119.00 |
| Switzerland | 1,730 | 24.70% | $117.00 |

International guests consistently cancel at lower rates than domestic Portuguese guests across all segments. Reducing Portugal dependency from 41% to 35% through targeted international marketing would improve both ADR and cancellation rate simultaneously.

---

### Booking Value Does Not Predict Cancellation — But the Financial Stakes Do

Cancellation rates are remarkably uniform across all four booking value quartiles (34.70%–38.46%). Price tier alone does not predict cancellation likelihood. However the financial impact when high-value bookings cancel is dramatically different:

| Booking Tier | Cancellation Rate | Avg Revenue Lost per Cancellation |
|-------------|-------------------|-----------------------------------|
| Q1 Low Value | 34.70% | $97.52 |
| Q2 Mid-Low | 38.36% | $212.20 |
| Q3 Mid-High | 38.46% | $348.65 |
| Q4 High Value | 38.39% | $796.93 |

Q4 cancellations cost 8x more than Q1 cancellations. Deposit policies should therefore target high-value bookings not because they cancel more often, but because the revenue impact when they do is dramatically higher.

---

### Repeat Guests Are Significantly More Reliable

Repeat guests cancel at only 14.49% versus 37.79% for new guests — less than half the rate. However repeat guest ADR is substantially lower ($64.45 vs $103.06), suggesting these are loyalty-driven price-sensitive guests rather than premium bookers. The value of repeat guests comes from their reliability and zero acquisition cost, not from rate premium. Loyalty programs should focus on converting reliable mid-tier guests rather than discounting premium segments.

---

### Room Changes Do Not Cause Cancellations

Guests who received a different room than reserved cancel at only 5.38% versus 41.56% for guests who received their requested room — a counterintuitive finding explained by timing. Room changes are discovered at check-in after arrival, when cancellation is no longer practical. The lower ADR for changed rooms ($83.36 vs $104.47) indicates most changes are downgrades from premium to standard rooms — a guest satisfaction issue that is separate from cancellation risk.

---

## Machine Learning Model

### Objective

Predict cancellation probability for each booking at the moment of reservation, enabling proactive revenue protection before cancellation occurs.

### Models Evaluated

| Model | ROC-AUC | Notes |
|-------|---------|-------|
| Logistic Regression | ~78% | Interpretable baseline — underpowered for this problem |
| Random Forest | ~91% | Strong performance but slower inference |
| LightGBM | ~94% | Fast and accurate |
| **XGBoost** | **95.29%** | **Best overall — selected for production deployment** |

### Top Predictive Features

1. **Lead time** — strongest single predictor; linear relationship confirmed by SQL Q7
2. **Deposit type** — Non Refund bookings flagged as near-certain cancellation
3. **Country of origin** — Portugal significantly elevates risk
4. **Market segment** — Groups and Online TA increase risk; Direct reduces it
5. **Total special requests** — inversely correlated with cancellation
6. **Previous cancellations** — prior behaviour is highly predictive of future behaviour
7. **Required car parking spaces** — guests who need parking rarely cancel
8. **Total nights of stay** — longer stays correlate with lower cancellation probability

### Model Artifacts

```
models/
├── xgb_model.pkl           # Trained XGBoost classifier
├── cat_mappings.pkl         # Label encodings for categorical features
└── feature_columns.pkl      # Ordered feature list for consistent inference
```

---

## Power BI Dashboard

The Power BI dashboard translates all SQL and Python findings into an interactive visual story for hotel management and non-technical stakeholders. Built with 8 custom DAX measures, a custom DateTable, and cross-page slicers for Hotel Type and Year.

### DAX Measures

```dax
Total Bookings     = COUNTROWS(hotel_bookings_clean)

Total Cancelled    = SUM(hotel_bookings_clean[is_canceled])

Cancellation Rate  = DIVIDE([Total Cancelled], [Total Bookings], 0)

Total Revenue      = CALCULATE(SUM(hotel_bookings_clean[total_revenue]),
                               hotel_bookings_clean[is_canceled] = 0)

Average ADR        = CALCULATE(AVERAGE(hotel_bookings_clean[adr]),
                               hotel_bookings_clean[is_canceled] = 0)

Revenue Lost       = CALCULATE(SUM(hotel_bookings_clean[total_revenue]),
                               hotel_bookings_clean[is_canceled] = 1)

Average Lead Time  = AVERAGE(hotel_bookings_clean[lead_time])

Repeat Guest Rate  = DIVIDE(CALCULATE(COUNTROWS(hotel_bookings_clean),
                               hotel_bookings_clean[is_repeated_guest] = 1),
                               COUNTROWS(hotel_bookings_clean), 0)
```

### Dashboard Pages

**Page 1 — Executive Summary**
Five KPI cards, monthly revenue trend by year, cancellation rate by hotel type, and seasonal booking distribution. Designed for a 30-second leadership briefing showing the full scope of the $16.9M revenue leakage problem.

![Executive Summary](screenshots/01_executive_summary.png)

---

**Page 2 — Booking Timeline**
Monthly booking volume by year, seasonal patterns with color-coded bars by season, lead time bucket distribution, and the cancellation rate by lead time curve showing the linear 6.78% to 57.01% progression.

![Booking Timeline](screenshots/02_booking_timeline.png)

---

**Page 3 — Hotel and Segment Performance**
Side-by-side City vs Resort comparison on Revenue, ADR, and Cancellation Rate. Monthly ADR line chart revealing Resort Hotel's dramatic summer spike and winter collapse — the two lines cross in June and September creating a distinctive X pattern. Revenue and cancellation rate by market segment.

![Hotel and Segment Performance](screenshots/03_hotel_segment.png)

---

**Page 4 — Cancellation Deep Dive**
Cancellation rate by deposit type (Non Refund 99.4%), lead time curve, special requests gradient showing the 47.7% to 5.0% decline, and a stacked green/red bar chart showing completed vs cancelled bookings across all 12 months.

![Cancellation Deep Dive](screenshots/04_cancellation_deep_dive.png)

---

**Page 5 — Revenue and Pricing**
ADR by season and hotel type revealing Resort Hotel's summer-only pricing premium. Monthly ADR comparison line chart. Revenue heatmap matrix by month and year with August consistently the darkest cell. Revenue breakdown by market segment.

![Revenue and Pricing](screenshots/05_revenue_pricing.png)

---

**Page 6 — Geographic Analysis**
World map with booking volume bubbles (Portugal cluster dominates Europe), top 15 countries by bookings, top 10 countries by revenue, and a country-level KPI table with bookings, cancellation rate, ADR, and total revenue for all major markets.

![Geographic Analysis](screenshots/06_geographic_analysis.png)

---

## Strategic Recommendations

Ordered by estimated revenue impact, derived directly from quantitative analysis.

**Priority 1 — Direct Booking Conversion**

Direct bookings match Online TA ADR ($114 vs $114) with half the cancellation rate (15.3% vs 36.7%) and zero OTA commission. Shifting 10,000 bookings from OTA to Direct generates approximately $1.5M in saved commission annually — before accounting for the cancellation reduction benefit. Invest in direct booking incentives, best-rate guarantees, and loyalty program enrollment at checkout.

**Priority 2 — Tiered Lead Time Deposit Policy**

Implement deposit requirements scaled to cancellation risk by booking window:
- 0–30 days advance: no deposit required (6.78%–27.86% risk)
- 31–90 days advance: refundable deposit required (37.70% risk)
- 90+ days advance: non-refundable deposit required (44.71%–57.01% risk)

This directly addresses the strongest predictor in the ML model without deterring low-risk short-horizon bookings that are unlikely to cancel anyway.

**Priority 3 — Special Request Engagement at Booking**

Guests with zero special requests cancel at 47.7%. A targeted follow-up sequence asking guests about room preferences, dietary requirements, and transportation — sent within 24 hours of booking — converts passive reservations into committed stays. Low cost, high impact, and immediately deployable.

**Priority 4 — International Market Diversification**

Reducing Portugal dependency from 41% to 35% by investing in targeted marketing toward Germany (16.71% cancellation, $104 ADR), France (18.57%, $110), USA (23.9%, $119), and Switzerland (24.7%, $117) would improve revenue quality across both metrics simultaneously. These markets combine premium rates with reliable behaviour — the ideal guest profile that currently represents less than 20% of total bookings.

**Priority 5 — Resort Hotel Off-Season Revenue Strategy**

Resort Hotel Winter ADR of $57 versus Summer $186 creates a 170% seasonal swing and a dangerous cash flow vulnerability. Develop conference packages, wellness retreats, and shoulder-season promotions targeting the corporate segment to raise Winter ADR toward $80+. The goal is not to match summer revenue, but to reduce the risk of a business that currently generates 45% of its annual revenue in a single season.

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Power BI Desktop (free download from Microsoft) for the .pbix dashboard file

### Installation

```bash
# Clone the repository
git clone https://github.com/SadeqSoltani/hotel-booking-analysis.git
cd hotel-booking-analysis

# Install dependencies
pip install -r requirements.txt
```

### Run the Streamlit App Locally

```bash
streamlit run app.py
```

Or access the live deployment: [hotel-booking-cancellation-risk-predictor.streamlit.app](https://hotel-booking-cancellation-risk-predictor.streamlit.app)

### Open the Power BI Dashboard

Open `dashboard/Hotel_booking.pbix` in Power BI Desktop. All data is embedded — no additional configuration required.

### Run the Analysis Notebooks

Open Jupyter Notebook or VS Code and run notebooks in sequence: `01` → `02` → `03` → `04` → `05`. Each notebook depends on outputs from the previous one.

---

## Dataset

The dataset is the **Hotel Booking Demand** dataset published by Antonio, Almeida, and Nunes (2019).

> Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. *Data in Brief*, 22, 41–49. https://doi.org/10.1016/j.dib.2018.11.126

Available publicly on [Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand). All personally identifying information was removed prior to publication.

---

## Author

**Sadeq Soltani**

📍 Vaughan, Ontario, Canada
🐙 GitHub: [github.com/SadeqSoltani](https://github.com/SadeqSoltani)
🚀 Live App: [hotel-booking-cancellation-risk-predictor.streamlit.app](https://hotel-booking-cancellation-risk-predictor.streamlit.app)

---

*Built as a comprehensive portfolio project demonstrating end-to-end data analytics capability across SQL, Python, machine learning, and business intelligence.*
