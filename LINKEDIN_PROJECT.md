# Property vs Portfolio Simulator — LinkedIn Project Description

A financial simulator answering: Should you buy a home, rent and invest, or become a landlord?

Built with Python and Streamlit, modeling 40+ financial parameters with month-by-month precision over 5–40 years. Designed for Spanish real estate but fully configurable for any country.

Simulation Engine (Pure Python, zero dependencies):
• French and Linear amortization with interest/principal decomposition
• Fixed, Variable, and Mixed rate mortgages with base rate predictions (Euribor, Fed Rate, SONIA)
• Secondary loans (family/private/government) with DTI constraints and deferred timing
• Max-affordable property solver via binary search on DTI and LTV
• Surplus equalization algorithm normalizing monthly cash flows for fair cross-scenario comparison
• Spanish IRPF deduction engine: mortgage interest, construction depreciation, financing+repair cap at gross rent with 4-year carry-forward, separate uncapped legal/bad debt deductions
• Bank product bonificaciones aggregating rate discounts and costs
• Rent deposit lifecycle tracking with contract renewal deltas
• Landlord opportunity cost — deficits compound at portfolio return rate

Web Application (Streamlit):
• Multi-scenario tabbed interface with unlimited parallel comparisons
• Dynamic data editors for IRPF brackets, base rate predictions, and bank products
• Translation layer mapping flat UI state to nested engine format
• Results: summary table, year-by-year breakdown, 4 Plotly charts, CSV export

Internationalization:
• 150+ translation keys in English and Spanish with runtime switching and graceful fallback chain
• Financial glossary with bilingual explanations of all metrics and concepts

Tech Stack: Python 3.12 (stdlib only) | Streamlit | Pandas | Plotly | Streamlit Community Cloud

Live app: https://propertyvsportfolio.streamlit.app
Source: https://github.com/Neogus/property_portfolio_simulator
