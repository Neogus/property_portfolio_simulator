# Property vs Portfolio Simulator — Context File

## Location
`/mnt/c/Users/grabino/PycharmProjects/pythonProject/Mortgage/calculator/`

## How to Run
```bash
cd /mnt/c/Users/grabino/PycharmProjects/pythonProject/Mortgage/calculator
streamlit run app.py
# Opens at http://localhost:8501
```

## Files
| File | Lines | Purpose |
|------|-------|---------|
| `engine.py` | ~720 | Pure Python simulation engine (zero deps). French/Linear amortization, fixed/variable/mixed rates with base rate predictions, secondary loans (family/private/gov), max-affordable property solver, surplus equalization, landlord IRPF deductions (interest-only, depreciation, financing+repair cap with 4yr carry-forward, bad debt, legal costs), bank product bonificaciones, rent deposit lifecycle, opportunity cost modeling |
| `app.py` | ~1030 | Streamlit GUI. Session state with flat scenario dicts → `_to_engine_scenario()` translates to nested engine format. Multi-tab scenarios, data editors for IRPF brackets / base rate predictions / bank products, Plotly charts, CSV export. Legal disclaimer in EN/ES |
| `i18n.py` | ~620 | 150+ keys in EN/ES. `t(key)` with fallback chain: current lang → 'en' → raw key. `set_lang()`/`get_lang()` with session state persistence |
| `launch.py` | ~25 | Double-fork daemon for persistent local hosting |
| `requirements.txt` | 3 | streamlit, pandas, plotly |
| `README.md` | — | GitHub repo description with usage guide, tech stack, disclaimer |
| `LINKEDIN_PROJECT.md` | — | Technical project description for LinkedIn |
| `LINKEDIN_POST.md` | — | Ready-to-paste LinkedIn post |
| `LICENSE` | — | All Rights Reserved — viewing only, no reuse |
| `CONTEXT.md` | — | This file — project context for AI assistants |
## Engine API
```python
from engine import run_simulation
result = run_simulation(scenarios_list, global_params_dict)
# result['cash_base'] = float
# result['scenarios']['Name'] = {type, upfront, property_value_initial, bank_loan, sec_loan, monthly: [...], final: {...}}
```

All percentages in input dicts are in % form (e.g., 3.0 = 3%). Engine divides by 100 internally.

## 3 Scenario Types

### Owner-Occupier (type='owner')
- Property: max affordable (binary search on DTI) or fixed value
- Bank loan: LTV, rate type (Fixed/Variable/Mixed), amortization (French/Linear)
- Variable rates: `_current_rate()` applies base rate predictions + spread + product discount
- Secondary loan: paid concurrent or deferred after primary, optional DTI constraint
- Bank products: active products reduce effective rate, costs added to monthly expenses
- Costs: transfer tax, registration, maintenance (%+fixed), insurance (%+fixed), selling commission, plusvalía (flat or % of appreciation)
- Portfolios built in `_equalize()` — NOT in `_sim_owner()`

### Rent + Invest (type='rent')
- Rent: % of reference property value (auto-populated from first owner) or fixed
- Contract regime: ITP-indexed / custom % / market value increases, reset at renewal
- Deposit: N months of rent locked from portfolio, delta at renewals, returned at end
- Portfolios built in `_equalize()` — NOT in `_sim_rent()`

### Buy-to-Rent Landlord (type='landlord')
- All owner params + rental income + landlord-specific
- IRPF on rental income with Spanish deduction rules:
  - Financing+repair (interest + maintenance) capped at gross rent, excess carried forward 4yr
  - Depreciation: configurable % of construction value (property × (1 − land_ratio))
  - Legal costs + bad debt: separate uncapped deductions
- Bad tenant event: unpaid months + eviction cost + repair cost at configurable year
- Portfolio grows standalone (NOT in surplus equalization). Negative = opportunity cost compounding at portfolio rate

## Key Design Decisions
1. **Surplus equalization**: `mx = max(all non-landlord costs)` each month; each scenario invests `mx - own_cost`. Ensures fair comparison.
2. **Landlord isolation**: Landlord doesn't participate in equalization — standalone portfolio from after-tax rental income. Contributes to cash_base but doesn't equalize.
3. **Opportunity cost**: Landlord negative portfolio compounds at portfolio return rate (money that could have been invested).
4. **IRPF separation**: Taxable rental income ≠ actual cashflow. Only interest deductible (not principal). Depreciation is deductible but not a cash cost.
5. **Session state**: App uses flat dicts in `st.session_state.scenarios[]`. `_to_engine_scenario()` translates to nested engine format before calling `run_simulation()`.
6. **Language**: `set_lang()` called from session state BEFORE any rendering. Selectbox/radio store English values internally, display translated labels.

## Deployment
- **GitHub repo**: `Neogus/property_portfolio_simulator` on `main` branch
- **Hosting**: Streamlit Community Cloud (free) — auto-deploys on every `git push` to `main`
- **License**: All Rights Reserved — portfolio showcase, code is view-only
- **Disclaimer**: Legal disclaimer displayed in-app (EN/ES) + in README
- **Analytics**: Google Analytics 4 via `GA_MEASUREMENT_ID` env var + local `.views` file counter
- **Bilingual**: Full EN/ES, switchable from sidebar
- **Dependencies**: streamlit, pandas, plotly

## Git Workflow
```bash
# Make changes, then:
cd /mnt/c/Users/grabino/PycharmProjects/pythonProject/Mortgage/calculator
git add <files>
git commit -m "type: description"
git push
# Streamlit auto-redeploys in ~1-2 minutes
```
