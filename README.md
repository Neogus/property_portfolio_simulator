# Property vs Portfolio Simulator

🏠📊 A comprehensive financial simulator that compares housing strategies: **buying a home**, **renting & investing**, or **becoming a landlord** — helping you make data-driven decisions about the biggest financial choice of your life.

🌐 **[Try it live →](https://property-vs-portfolio.streamlit.app)**

## Features

### 3 Scenario Types
- **Owner-Occupier** — Buy a property to live in with a mortgage
- **Rent + Invest** — Rent your home and invest the savings
- **Buy-to-Rent (Landlord)** — Buy a property to rent out as an investment

### Deep Financial Modeling
- **Mortgage types**: French & Linear amortization, Fixed / Variable / Mixed rates
- **Base rate predictions**: Year-by-year rate forecasts (Euribor, Fed Rate, SONIA, etc.)
- **Bank product bonificaciones**: Model rate discounts from hiring bank products (nómina, insurance, etc.)
- **Secondary loans**: Family, private, or government loans with flexible timing
- **Spanish IRPF tax**: Progressive capital gains brackets with proper deductions
- **Landlord IRPF deductions**: Mortgage interest, depreciation, bad debt, legal costs — with financing+repair cap and 4-year carry-forward
- **Rent contract regime**: ITP-indexed, custom %, or market value increases with contract renewal resets
- **Deposit tracking**: Renter deposit locked from portfolio, returned at simulation end
- **Surplus equalization**: Fair comparison by investing monthly cost differences
- **Opportunity cost**: Landlord deficits compound at portfolio rate for honest comparison

### Results & Visualization
- Summary comparison table with winner highlight
- Year-by-year breakdown of costs, portfolio, and net worth
- Interactive Plotly charts (net worth, portfolio, cost trends, stacked breakdown)
- Month-by-month detail with CSV export
- Supports unlimited parallel scenarios for A/B comparisons

### Bilingual 🌐
- Full English and Spanish (Español) interface
- Switch languages instantly from the sidebar

## Quick Start

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

## Tech Stack
- **Frontend**: Streamlit
- **Engine**: Pure Python (no dependencies beyond stdlib)
- **Charts**: Plotly
- **i18n**: Custom lightweight translation module

## Screenshots

_Configure scenarios side by side, run simulation, and compare results with interactive charts._

## License

MIT
