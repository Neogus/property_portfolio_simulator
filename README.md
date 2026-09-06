# 🏠 Property vs Portfolio Simulator

A comprehensive financial simulator that compares housing strategies — **buying a home**, **renting & investing**, or **becoming a landlord** — helping you make data-driven decisions about the biggest financial choice of your life.

> 🌐 **[Try it live →] https://property-vs-portfolio.streamlit.app/**
>
> _Replace the URL above with your Streamlit Cloud link after deployment._

---

## Why This Tool?

The "buy vs rent" debate is usually driven by opinions. This simulator replaces guesswork with **math** — modeling 40+ financial parameters with month-by-month precision over any time horizon.

Every situation is different. Your income, local property prices, mortgage rates, rent costs, investment returns, and tax regime all interact in complex ways. This tool lets you plug in **your real numbers** and see which strategy builds more wealth over 5–40 years.

---

## Features

### 3 Scenario Types

| Scenario | What It Models |
|----------|---------------|
| **Owner-Occupier** | Buy a property to live in with a mortgage. Tracks property equity, mortgage payoff, and surplus investing. |
| **Rent + Invest** | Rent your home and invest everything you would have spent on a down payment + the monthly cost difference. |
| **Buy-to-Rent (Landlord)** | Buy a property to rent out. Models rental income, vacancy, expenses, and IRPF deductions on rental earnings. |

Add **unlimited scenarios** side by side — compare a fixed-rate 20-year mortgage vs a variable-rate 25-year, or see how a landlord scenario stacks up against renting + investing.

### Mortgage Modeling
- **Amortization types**: French (constant payment) and Linear (constant principal)
- **Rate types**: Fixed, Variable, or Mixed (fixed period then variable, or vice versa)
- **Base rate predictions**: Enter year-by-year forecasts for your country's reference rate (Euribor, Fed Funds Rate, SONIA, etc.)
- **Bank product bonificaciones**: Model rate discounts from hiring bank products (salary deposit, insurance, credit cards, pension plans) and their associated costs
- **Secondary loans**: Family, private, or government loans with independent rate, term, and flexible repayment timing

### Rental Modeling
- **Rent modes**: Calculate from % of property value or enter a fixed amount
- **Contract regime**: Choose how rent increases within a contract (inflation-indexed, custom %, or market value) and resets at renewal
- **Deposit tracking**: Renter's deposit is locked from the portfolio, increases at renewals, and is returned at simulation end

### Landlord Modeling
- **Vacancy & agent commission**: Configure expected empty months and agent fees
- **Bad tenant scenario**: Model months of unpaid rent, eviction costs, and property repair
- **Spanish IRPF deductions**: Mortgage interest (not principal), construction depreciation, financing+repair cap at gross rent with 4-year carry-forward, legal costs and bad debt as separate uncapped deductions

### Tax & Costs
- **IRPF capital gains brackets**: Fully configurable progressive tax on property sale and portfolio gains
- **Plusvalía municipal**: Flat amount or % of property appreciation
- **Transfer tax, registration, maintenance, insurance**: All configurable as % + fixed amounts
- **Selling commission**: Applied at end of simulation

### Fair Comparison Engine
- **Surplus equalization**: Each month, the cheapest scenario invests the cost difference vs the most expensive
- **Opportunity cost**: Landlord out-of-pocket deficits compound at the portfolio return rate
- **Cash base**: All scenarios start with the same amount of cash

### Results & Visualization
- **Summary table** with winner highlight and advantage metrics
- **Year-by-year comparison** of costs, portfolio, and net worth
- **4 interactive Plotly charts**: Net worth, portfolio growth, final breakdown, monthly costs
- **Month-by-month detail** per scenario with CSV download

### Bilingual 🌐
- Full **English** and **Spanish** interface — switch instantly from the sidebar

---

## Quick Start

### Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/property-vs-portfolio.git
cd property-vs-portfolio
pip install -r requirements.txt
streamlit run app.py
```

Opens at **http://localhost:8501**.

---

## How to Use

### Step 1: Set Global Parameters (Sidebar)
- **Monthly net income** and **DTI limit** → determines mortgage affordability
- **Expected inflation** → used for rent indexation
- **Portfolio annual return** → expected investment return
- **Simulation duration** → how many years to project (5–40)
- **IRPF tax brackets** → editable, defaults to Spanish rates

### Step 2: Configure Scenarios (Tabs)
The app starts with 3 default scenarios. For each:

**Owner-Occupier** — Set property value (auto-calculated from DTI or fixed), mortgage terms, rate type, optional secondary loans and bank product bonificaciones, and all costs (tax, maintenance, insurance, selling fees).

**Rent + Invest** — Choose rent mode (% of property value or fixed amount), set deposit months and contract regime (how rent increases over time).

**Buy-to-Rent (Landlord)** — All owner settings plus rental income config, vacancy, agent commission, bad tenant scenario, and IRPF deduction parameters (depreciation rate, land ratio).

### Step 3: Add More Scenarios (Optional)
Click **➕ Add New Scenario** in the sidebar. Examples:
- Compare 20-year fixed vs 25-year variable mortgage
- Test different property appreciation rates
- See how bank bonificaciones affect the outcome

### Step 4: Run & Analyze
Click **▶️ Run Simulation**. Results include:
1. **Summary table** — Final net worth per scenario with winner highlight
2. **Year-by-year table** — Costs, portfolio, and estimated net worth over time
3. **Interactive charts** — Visual comparison across all scenarios
4. **Month-by-month CSV** — Full granular data for your own analysis

---

## Understanding the Results

**Owner/Landlord Net Worth:**
```
Property Value − Selling Costs − Plusvalía − Remaining Loans − Capital Gains Tax
+ Portfolio Value − Portfolio Tax
```

**Renter Net Worth:**
```
Portfolio Value − Portfolio Tax + Deposit Returned
```

The **winner** is the scenario with the highest net worth after all taxes at the end of the simulation. Small changes in mortgage rate, appreciation, or portfolio return can flip the result — that's why this tool exists.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Simulation Engine | Python (stdlib only — zero external dependencies) |
| Web Framework | Streamlit |
| Data Processing | Pandas |
| Visualization | Plotly |
| Internationalization | Custom i18n module (EN/ES) |

**Architecture:** The simulation engine (`engine.py`) is a standalone Pure Python module with no web dependencies — it can be imported independently into a FastAPI backend, CLI tool, or Jupyter notebook.

---

## Contributing

Suggestions, bug reports, and feature requests welcome! Open an issue or submit a PR.

**Ideas for the future:**
- Additional languages (Portuguese, French, German)
- Country-specific tax presets (UK, US, France)
- PDF report generation
- Sensitivity analysis (sweep a parameter over a range)
- FastAPI backend for monetization (ads, affiliates, premium features)

---

## License

**All Rights Reserved.** This repository is a portfolio showcase. The code is available for viewing only — it may not be copied, modified, or redistributed. See [LICENSE](LICENSE) for details.
