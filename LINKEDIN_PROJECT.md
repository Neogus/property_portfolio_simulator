# Property vs Portfolio Simulator — LinkedIn Project Description

## Overview

An open-source financial simulator that answers one of life's biggest financial questions: *Should you buy a home, rent and invest the difference, or become a landlord?*

Built as a full-stack web application using Python, this tool models 40+ financial parameters with month-by-month precision over any time horizon (5–40 years), producing interactive visualizations and exportable reports. The simulator is designed for the Spanish real estate market but is architecture-agnostic — all country-specific parameters (tax brackets, base reference rates, contract regimes) are fully configurable.

## Technical Architecture

### Simulation Engine (`engine.py` — Pure Python, zero dependencies)
- **Loan amortization engine**: Supports French (constant payment) and Linear (constant principal) amortization schedules with full balance tracking and interest/principal decomposition per month
- **Variable & mixed rate modeling**: Year-by-year base rate predictions (Euribor, Fed Funds Rate, SONIA, etc.) with configurable spread. Mixed mortgages support fixed-then-variable or variable-then-fixed with configurable split points. Payments recalculate monthly on remaining balance at current rate
- **Secondary loan support**: Family, private, or government loans with independent rate, term, DTI constraint toggle, and flexible repayment timing (concurrent or deferred after primary loan)
- **Max-affordable property solver**: Binary search algorithm that finds the maximum property value given DTI constraints, LTV, rate, and optional secondary loan interactions
- **Surplus equalization algorithm**: Normalizes monthly cash flows across non-landlord scenarios by investing the cost differential each month, ensuring fair portfolio comparison between strategies with different monthly outlays
- **Landlord IRPF deduction engine**: Implements Spanish rental income tax rules including mortgage interest deduction (not principal), construction depreciation (configurable rate and land ratio), financing+repair cap at gross rental income with 4-year carry-forward of excess deductions, separate uncapped deductions for legal/eviction costs and bad debt
- **Progressive tax calculator**: Configurable bracket-based IRPF computation applied to property capital gains and portfolio liquidation gains independently
- **Bank product bonificaciones**: Aggregates rate discounts and annual costs (% of loan balance + fixed EUR) from activated bank products, applying net discount to effective mortgage rate
- **Rent deposit lifecycle**: Tracks deposit lock from initial portfolio, recalculates delta at contract renewals as rent resets to market, and returns deposit at simulation end
- **Opportunity cost modeling**: Landlord deficits (negative cash flow months) compound at the portfolio return rate, accurately reflecting the opportunity cost of capital subsidizing the property

### Web Application (`app.py` — Streamlit)
- **Multi-scenario tabbed interface**: Add unlimited scenarios of any type (Owner-Occupier, Rent+Invest, Buy-to-Rent Landlord), each with full configuration panels
- **Dynamic data editors**: Editable tables for IRPF tax brackets, base rate year-by-year predictions, and bank product bonificaciones — all supporting add/remove rows
- **Session state management**: Persistent scenario configurations across Streamlit reruns with proper widget key isolation per scenario index
- **Translation layer**: Bidirectional mapping between flat UI state dictionaries and nested engine input format, with DataFrame-to-dict conversion for rate predictions and product aggregation
- **Results dashboard**: Summary comparison table, year-by-year breakdown, 4 interactive Plotly charts (net worth, portfolio, cost trends, stacked final breakdown), and per-scenario month-by-month detail with CSV download

### Internationalization (`i18n.py`)
- **150+ translation keys** covering all UI labels, help texts, glossary entries, and chart titles
- **Full English and Spanish** with natural financial terminology (hipoteca, amortización francesa, Euríbor, plusvalía municipal, IRPF, bonificaciones, inquilino moroso, etc.)
- **Runtime language switching** with session state persistence — no page reload required
- **Graceful fallback chain**: current language → English → raw key

### Analytics & Deployment
- **Google Analytics 4 integration**: Optional GA4 tag injection via environment variable (`GA_MEASUREMENT_ID`)
- **Local view counter**: File-based page view tracking for development
- **Streamlit Community Cloud ready**: Single `requirements.txt`, no database, no secrets required
- **Daemon launcher** (`launch.py`): Double-fork daemonizer for persistent local hosting on WSL/Linux

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Simulation Engine | Python 3.12 (stdlib only — `math`, `typing`) |
| Web Framework | Streamlit 1.63+ |
| Data Processing | Pandas 2.0+ |
| Visualization | Plotly 7.0+ |
| Internationalization | Custom i18n module |
| Hosting | Streamlit Community Cloud (free) |

## Key Financial Parameters Modeled
- Monthly net income & bank DTI limit
- Property value (fixed or max-affordable from DTI)
- Yearly property appreciation (market or capped)
- Mortgage: LTV, rate (fixed/variable/mixed), term, amortization type
- Base rate predictions with spread (Euribor/Fed/SONIA agnostic)
- Bank product bonificaciones (rate discounts + costs)
- Secondary loans (family/private/government) with DTI and timing options
- Transfer tax, registration fees, maintenance (% + fixed), insurance (% + fixed)
- Selling commission, plusvalía (flat or % of appreciation)
- IRPF progressive tax brackets (configurable)
- Rent yield, contract length, in-contract increase type (ITP/custom/market)
- Renter deposit (months of rent, locked from portfolio)
- Landlord: vacancy, agent commission, bad tenant event, IRPF deductions with depreciation and carry-forward
- Portfolio annual return with monthly compounding
- Inflation rate (ITP) for rent indexation

## Links
- **Live app**: https://property-vs-portfolio.streamlit.app
- **Source code**: https://github.com/YOUR_USERNAME/property-vs-portfolio
