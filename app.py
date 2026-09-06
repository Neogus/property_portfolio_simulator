"""
Mortgage / Rent / Invest Calculator — Streamlit Application
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
import plotly.graph_objects as go
from engine import run_simulation
from i18n import t, set_lang, get_lang


def inject_ga(ga_id):
    """Inject Google Analytics 4 tag."""
    if ga_id:
        components.html(f"""
            <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){{dataLayer.push(arguments);}}
                gtag('js', new Date());
                gtag('config', '{ga_id}');
            </script>
        """, height=0)

def increment_views():
    views_file = os.path.join(os.path.dirname(__file__), '.views')
    try:
        count = int(open(views_file).read().strip()) if os.path.exists(views_file) else 0
    except:
        count = 0
    count += 1
    with open(views_file, 'w') as f:
        f.write(str(count))
    return count

st.set_page_config(page_title='Property vs Portfolio Simulator', layout='wide',
                   initial_sidebar_state='expanded')

GA_ID = os.environ.get('GA_MEASUREMENT_ID', '')  # Set your GA4 ID here or via env var
inject_ga(GA_ID)
views = increment_views()

# ============================================================================
# DEFAULT SCENARIO FACTORIES
# ============================================================================

def create_default_owner_scenario(name):
    return {
        'name': name, 'type': 'Owner-Occupier',
        'bank_products': pd.DataFrame({
            'Product': ['Direct deposit (nómina)', 'Home insurance', 'Life / mortgage protection insurance',
                        'Payment protection insurance', 'Credit card', 'Pension plan / investment funds',
                        'Other insurance (car, health)', 'Alarm / security service'],
            'Active': [False, False, False, False, False, False, False, False],
            'Rate Discount (%)': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'Annual Cost (% of loan)': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'Annual Cost (EUR)': [0, 0, 0, 0, 0, 0, 0, 0],
        }),
        'property_value_mode': 'Max Affordable',
        'property_value': 237000,
        'yearly_appreciation': 4.5,
        'ltv': 80, 'rate_type': 'Fixed', 'fixed_rate': 3.0,
        'mortgage_term': 20, 'amortization_type': 'French',
        'euribor_spread': 1.0, 'default_euribor': 2.5,
        'euribor_predictions': pd.DataFrame({
            'Year': [1, 5, 10, 15, 20],
            'Base Rate (%)': [2.5, 2.8, 3.0, 3.2, 3.5]
        }),
        'fixed_period': 10,
        'variable_period_position': 'Variable at End',
        'secondary_loan_enabled': False,
        'secondary_loan_amount_pct': 20,
        'secondary_loan_rate': 0.0,
        'secondary_loan_term': 5,
        'secondary_loan_dti_constrained': False,
        'secondary_loan_timing': 'After Primary Loan',
        'transfer_tax': 10.0, 'registration_fee': 2000,
        'maintenance_pct': 1.0, 'maintenance_fixed': 0.0,
        'insurance_pct': 0.0, 'selling_commission': 6.0,
        'plusvalia_mode': 'Flat Amount',
        'plusvalia_flat': 4000, 'plusvalia_pct': 5.0,
    }

def create_default_rent_scenario(name):
    return {
        'name': name, 'type': 'Rent + Invest',
        'rent_mode': '% of Property Value',
        'reference_property_value': 0,
        'reference_appreciation': 4.5,
        'rent_yield': 5.0, 'monthly_rent_fixed': 1000,
        'contract_length': 5,
        'in_contract_increase': 'Inflation (ITP)',
        'custom_increase': 2.5,
        'deposit_months': 1,
    }

def create_default_landlord_scenario(name):
    sc = create_default_owner_scenario(name)
    sc.update({
        'type': 'Buy-to-Rent (Landlord)',
        'rent_mode': '% of Property Value',
        'reference_property_value': 0,
        'reference_appreciation': 4.5,
        'rent_yield': 5.0, 'monthly_rent_fixed': 1000,
        'contract_length': 5,
        'in_contract_increase': 'Inflation (ITP)',
        'custom_increase': 2.5,
        'insurance_pct': 0.3,
        'vacancy_months': 1.0,
        'agent_commission_pct': 8.0,
        'bad_tenant_enabled': False,
        'bad_tenant_months_unpaid': 6,
        'bad_tenant_eviction_cost': 3000,
        'bad_tenant_repair_cost': 5000,
        'bad_tenant_year': 10,
    })
    return sc

# ============================================================================
# APP → ENGINE TRANSLATION
# ============================================================================

def _euribor_df_to_dict(df):
    if df is None or not hasattr(df, 'iterrows'):
        return {}
    out = {}
    rate_col = 'Base Rate (%)' if 'Base Rate (%)' in df.columns else 'Euribor (%)'
    for _, row in df.iterrows():
        try:
            out[str(int(row[t('base_rate_col_year')]))] = float(row[rate_col])
        except Exception:
            try:
                out[str(int(row['Year']))] = float(row[rate_col])
            except Exception:
                pass
    return out

def _to_engine_scenario(app):
    """Convert flat app-format scenario dict → nested engine format."""
    t = app['type']
    if t == 'Owner-Occupier':
        etype = 'owner'
    elif t == 'Rent + Invest':
        etype = 'rent'
    else:
        etype = 'landlord'

    if etype == 'rent':
        return {
            'name': app['name'], 'type': 'rent',
            'rent': {
                'mode': 'pct_of_value' if app.get('rent_mode') == '% of Property Value' else 'fixed',
                'rent_yield_pct': app.get('rent_yield', 5.0),
                'reference_property_value': app.get('reference_property_value', 0),
                'reference_appreciation': app.get('reference_appreciation', 4.5),
                'fixed_monthly_rent': app.get('monthly_rent_fixed', 1000),
                'contract_years': app.get('contract_length', 5),
                'increase_type': app.get('in_contract_increase', 'Inflation (ITP)'),
                'custom_increase_pct': app.get('custom_increase', 2.5),
                'deposit_months': app.get('deposit_months', 1),
                'deposit_months': app.get('deposit_months', 1),
            }
        }

    # owner / landlord share property+loan+costs structure
    base = {
        'name': app['name'], 'type': etype,
        'property_value_mode': app.get('property_value_mode', 'Max Affordable'),
        'property_value': app.get('property_value', 237000),
        'yearly_appreciation': app.get('yearly_appreciation', 4.5),
        'loan': {
            'ltv_pct': app.get('ltv', 85),
            'rate_type': app.get('rate_type', 'Fixed'),
            'fixed_rate': app.get('fixed_rate', 3.0),
            'term_years': app.get('mortgage_term', 20),
            'amortization': app.get('amortization_type', 'French'),
            'euribor_spread': app.get('euribor_spread', 1.0),
            'euribor_predictions': _euribor_df_to_dict(app.get('euribor_predictions')),
            'default_euribor': app.get('default_euribor', 2.5),
            'fixed_years': app.get('fixed_period', 10),
            'variable_at_end': app.get('variable_period_position', 'Variable at End') == 'Variable at End',
        },
        'secondary_loan': {
            'enabled': app.get('secondary_loan_enabled', False),
            'amount_pct': app.get('secondary_loan_amount_pct', 20),
            'interest_rate': app.get('secondary_loan_rate', 0.0),
            'term_years': app.get('secondary_loan_term', 5),
            'constrained_by_dti': app.get('secondary_loan_dti_constrained', False),
            'paid_after_primary': app.get('secondary_loan_timing', 'After Primary Loan') == 'After Primary Loan',
        },
        'costs': {
            'transfer_tax_pct': app.get('transfer_tax', 10.0),
            'registration_fee': app.get('registration_fee', 2000),
            'maintenance_pct': app.get('maintenance_pct', 1.0),
            'maintenance_fixed': app.get('maintenance_fixed', 0.0),
            'insurance_pct': app.get('insurance_pct', 0.0),
            'insurance_fixed': app.get('insurance_fixed', 0.0),
            'selling_fee_pct': app.get('selling_commission', 6.0),
            'plusvalia_mode': app.get('plusvalia_mode', 'Flat Amount'),
            'plusvalia_flat': app.get('plusvalia_flat', 4000),
            'plusvalia_pct': app.get('plusvalia_pct', 5.0),
        },
    }

    if etype == 'landlord':
        base['rent_config'] = {
            'mode': 'pct_of_value' if app.get('rent_mode') == '% of Property Value' else 'fixed',
            'rent_yield_pct': app.get('rent_yield', 5.0),
            'reference_property_value': app.get('reference_property_value', 0),
            'reference_appreciation': app.get('reference_appreciation', 4.5),
            'fixed_monthly_rent': app.get('monthly_rent_fixed', 1000),
            'contract_years': app.get('contract_length', 5),
            'increase_type': app.get('in_contract_increase', 'Inflation (ITP)'),
            'custom_increase_pct': app.get('custom_increase', 2.5),
        }
        base['landlord'] = {
            'vacancy_months_per_year': app.get('vacancy_months', 1.0),
            'agent_commission_pct': app.get('agent_commission_pct', 8.0),
            'bad_tenant_enabled': app.get('bad_tenant_enabled', False),
            'bad_tenant_unpaid_months': app.get('bad_tenant_months_unpaid', 6),
            'bad_tenant_eviction_cost': app.get('bad_tenant_eviction_cost', 3000),
            'bad_tenant_repair_cost': app.get('bad_tenant_repair_cost', 5000),
            'bad_tenant_occurs_at_year': app.get('bad_tenant_year', 10),
            'depreciation_rate': app.get('depreciation_rate', 3.0),
            'land_ratio': app.get('land_ratio', 20.0),
        }


    # Aggregate bank products for owner/landlord
    products_df = app.get('bank_products')
    if products_df is not None and hasattr(products_df, 'iterrows'):
        active = products_df[products_df.get('Active', False) == True]
        base['loan']['product_rate_discount'] = float(active['Rate Discount (%)'].sum())
        base['costs']['product_cost_pct_loan'] = float(active['Annual Cost (% of loan)'].sum())
        base['costs']['product_cost_fixed'] = float(active['Annual Cost (EUR)'].sum())
    else:
        base['loan']['product_rate_discount'] = 0
        base['costs']['product_cost_pct_loan'] = 0
        base['costs']['product_cost_fixed'] = 0

    return base

# ============================================================================
# SESSION STATE
# ============================================================================

if 'scenarios' not in st.session_state:
    st.session_state.scenarios = [
        create_default_owner_scenario('Traditional Buy'),
        create_default_rent_scenario('Rent + Invest'),
        create_default_landlord_scenario('Buy-to-Rent'),
    ]
if 'results' not in st.session_state:
    st.session_state.results = None

# Set language from session state BEFORE any rendering
if 'app_lang' not in st.session_state:
    st.session_state.app_lang = 'en'
set_lang(st.session_state.app_lang)

# ============================================================================
# TITLE
# ============================================================================

st.title(t('app_title'))
st.markdown(t('app_desc'))
st.caption(t('disclaimer'))
st.divider()

# ============================================================================
# FINANCIAL GUIDE / GLOSSARY
# ============================================================================

with st.expander(t('guide_header')):
    st.markdown(t('guide_intro'))
    st.markdown(f"\n**{t('guide_dti_title')}**")
    st.markdown(t('guide_dti'))
    st.markdown(f"\n**{t('guide_ltv_title')}**")
    st.markdown(t('guide_ltv'))
    st.markdown(f"\n**{t('guide_amortization_title')}**")
    st.markdown(t('guide_amortization'))
    st.markdown(f"\n**{t('guide_french_title')}**")
    st.markdown(t('guide_french'))
    st.markdown(f"\n**{t('guide_linear_title')}**")
    st.markdown(t('guide_linear'))
    st.markdown(f"\n**{t('guide_base_rate_title')}**")
    st.markdown(t('guide_base_rate'))
    st.markdown(f"\n**{t('guide_fixed_rate_title')}**")
    st.markdown(t('guide_fixed_rate'))
    st.markdown(f"\n**{t('guide_variable_rate_title')}**")
    st.markdown(t('guide_variable_rate'))
    st.markdown(f"\n**{t('guide_mixed_rate_title')}**")
    st.markdown(t('guide_mixed_rate'))
    st.markdown(f"\n**{t('guide_transfer_tax_title')}**")
    st.markdown(t('guide_transfer_tax'))
    st.markdown(f"\n**{t('guide_plusvalia_title')}**")
    st.markdown(t('guide_plusvalia'))
    st.markdown(f"\n**{t('guide_irpf_title')}**")
    st.markdown(t('guide_irpf'))
    st.markdown(f"\n**{t('guide_rent_yield_title')}**")
    st.markdown(t('guide_rent_yield'))
    st.markdown(f"\n**{t('guide_surplus_title')}**")
    st.markdown(t('guide_surplus'))
    st.markdown(f"\n**{t('guide_net_worth_title')}**")
    st.markdown(t('guide_net_worth'))
    st.markdown(f"\n**{t('guide_portfolio_title')}**")
    st.markdown(t('guide_portfolio'))
    st.markdown(f"\n**{t('guide_contract_title')}**")
    st.markdown(t('guide_contract'))
    st.markdown(f"\n**{t('guide_vacancy_title')}**")
    st.markdown(t('guide_vacancy'))
    st.markdown(f"\n**{t('guide_bad_tenant_title')}**")
    st.markdown(t('guide_bad_tenant'))

st.divider()

# ============================================================================
# SIDEBAR — GLOBAL PARAMETERS
# ============================================================================

with st.sidebar:
    # Language selector at the very top
    lang_options = ['English', 'Español']
    lang_idx = 0 if st.session_state.app_lang == 'en' else 1
    lang = st.selectbox(t('lang_label'), lang_options, index=lang_idx, key='lang_sel')
    new_lang = 'es' if lang == 'Español' else 'en'
    if new_lang != st.session_state.app_lang:
        st.session_state.app_lang = new_lang
        set_lang(new_lang)
        st.rerun()
    st.divider()

    st.header(t('sidebar_header'))

    monthly_income = st.number_input(t('monthly_income'), min_value=0,
                                     value=2500, step=100, format='%d',
                                     help=t('monthly_income_help'))

    bank_dti = st.number_input(t('bank_dti'), min_value=10, max_value=60,
                               value=35, step=1, format='%d',
                               help=t('bank_dti_help'))

    inflation = st.number_input(t('inflation'), min_value=0.0,
                                value=3.0, step=0.1, format='%.1f',
                                help=t('inflation_help'))

    portfolio_return = st.number_input(t('portfolio_return'), min_value=0.0,
                                      value=11.0, step=0.1, format='%.1f',
                                      help=t('portfolio_return_help'))

    sim_years = st.number_input(t('sim_years'), min_value=5,
                                max_value=40, value=20, step=1, format='%d')

    with st.expander(t('irpf_header')):
        st.caption(t('irpf_caption'))
        default_irpf = pd.DataFrame({
            t('irpf_col_limit'): [6000, 50000, 200000, 300000, 999999999],
            t('irpf_col_rate'): [19.0, 21.0, 23.0, 27.0, 28.0],
        })
        if 'irpf_df' not in st.session_state:
            st.session_state.irpf_df = default_irpf
        irpf_df = st.data_editor(st.session_state.irpf_df, num_rows='dynamic',
                                 use_container_width=True, hide_index=True)
        st.session_state.irpf_df = irpf_df

    st.divider()

    # ── Run simulation ────────────────────────────────────────────
    if st.button(t('run_btn'), type='primary', use_container_width=True):
        if not st.session_state.scenarios:
            st.error(t('run_no_scenarios'))
        else:
            with st.spinner(t('running')):
                try:
                    # Extract IRPF brackets handling both old and new column names
                    irpf_brackets = []
                    limit_col = t('irpf_col_limit') if t('irpf_col_limit') in irpf_df.columns else 'Upper Limit (EUR)'
                    rate_col = t('irpf_col_rate') if t('irpf_col_rate') in irpf_df.columns else 'Rate (%)'
                    for _, r in irpf_df.iterrows():
                        irpf_brackets.append({
                            'limit': int(r[limit_col]),
                            'rate': float(r[rate_col])
                        })

                    gp = {
                        'monthly_net_income': float(monthly_income),
                        'bank_dti_pct': float(bank_dti),
                        'inflation_rate': float(inflation),
                        'portfolio_return': float(portfolio_return),
                        'simulation_years': int(sim_years),
                        'irpf_brackets': irpf_brackets,
                    }
                    engine_sc = [_to_engine_scenario(s) for s in st.session_state.scenarios]
                    st.session_state.results = run_simulation(engine_sc, gp)
                    st.success(t('run_success'))
                    st.rerun()
                except Exception as e:
                    st.error(f"{t('run_error')}: {e}")

    st.divider()

    # ── Add scenario ──────────────────────────────────────────────
    with st.expander(t('add_scenario')):
        type_options = [t('type_owner'), t('type_rent'), t('type_landlord')]
        type_values = ['Owner-Occupier', 'Rent + Invest', 'Buy-to-Rent (Landlord)']
        new_type = st.selectbox(t('scenario_type'), type_options, key='new_sc_type')
        new_name = st.text_input(t('scenario_name'),
                                 value=f'Scenario {len(st.session_state.scenarios)+1}',
                                 key='new_sc_name')
        if st.button(t('add_btn'), key='add_sc'):
            selected_type = type_values[type_options.index(new_type)]
            factory = {'Owner-Occupier': create_default_owner_scenario,
                       'Rent + Invest': create_default_rent_scenario,
                       'Buy-to-Rent (Landlord)': create_default_landlord_scenario}
            st.session_state.scenarios.append(factory[selected_type](new_name))
            st.session_state.results = None
            st.rerun()


    # View counter at bottom of sidebar
    st.sidebar.caption(f'👁️ {views} views')
    st.sidebar.caption('☕ [Support this project](https://github.com/sponsors/Neogus) · [Ko-fi](https://ko-fi.com/neogus43222)')

# ============================================================================
# SCENARIO RENDER FUNCTIONS
# ============================================================================

def render_owner_occupier_config(scenario, idx):
    st.subheader(t('property_header'))
    col1, col2 = st.columns(2)
    with col1:
        mode_options = [t('prop_mode_max'), t('prop_mode_fixed')]
        mode_values = ['Max Affordable', 'Fixed Value']
        mode_idx = mode_values.index(scenario['property_value_mode'])
        mode_sel = st.radio(t('prop_mode'), mode_options, index=mode_idx, key=f'prop_mode_{idx}')
        scenario['property_value_mode'] = mode_values[mode_options.index(mode_sel)]
    with col2:
        if scenario['property_value_mode'] == 'Fixed Value':
            scenario['property_value'] = st.number_input(
                t('prop_value'), min_value=0,
                value=scenario['property_value'], step=1000, format='%d',
                key=f'prop_val_{idx}')
    scenario['yearly_appreciation'] = st.number_input(
        t('yearly_appr'), min_value=0.0,
        value=float(scenario['yearly_appreciation']),
        step=0.1, format='%.2f', key=f'appr_{idx}')

    st.divider()
    st.subheader(t('loan_header'))
    c1, c2 = st.columns(2)
    with c1:
        scenario['ltv'] = st.number_input(t('ltv'), min_value=0, max_value=100,
                                          value=scenario['ltv'], step=1, format='%d',
                                          key=f'ltv_{idx}',
                                          help=t('ltv_help'))
    with c2:
        rate_options = [t('rate_fixed'), t('rate_variable'), t('rate_mixed')]
        rate_values = ['Fixed', 'Variable', 'Mixed']
        rate_idx = rate_values.index(scenario['rate_type'])
        rate_sel = st.selectbox(t('rate_type'), rate_options, index=rate_idx, key=f'rt_{idx}')
        scenario['rate_type'] = rate_values[rate_options.index(rate_sel)]
    c1, c2 = st.columns(2)
    with c1:
        if scenario['rate_type'] in ('Fixed', 'Mixed'):
            scenario['fixed_rate'] = st.number_input(
                t('fixed_rate'), min_value=0.0,
                value=float(scenario['fixed_rate']),
                step=0.1, format='%.2f', key=f'fr_{idx}')
    with c2:
        scenario['mortgage_term'] = st.number_input(
            t('mortgage_term'), min_value=1, max_value=40,
            value=scenario['mortgage_term'], step=1, format='%d',
            key=f'mt_{idx}')
    amort_options = [t('amort_french'), t('amort_linear')]
    amort_values = ['French', 'Linear']
    amort_idx = amort_values.index(scenario['amortization_type'])
    amort_sel = st.selectbox(t('amort_type'), amort_options, index=amort_idx, key=f'am_{idx}')
    scenario['amortization_type'] = amort_values[amort_options.index(amort_sel)]

    if scenario['rate_type'] in ('Variable', 'Mixed'):
        st.markdown(f"**{t('var_config')}**")
        c1, c2 = st.columns(2)
        with c1:
            scenario['euribor_spread'] = st.number_input(
                t('base_rate_spread'), min_value=0.0,
                value=float(scenario['euribor_spread']),
                step=0.1, format='%.2f', key=f'es_{idx}',
                help=t('base_rate_spread_help'))
        with c2:
            scenario['default_euribor'] = st.number_input(
                t('default_base_rate'), min_value=0.0,
                value=float(scenario['default_euribor']),
                step=0.1, format='%.2f', key=f'de_{idx}',
                help=t('default_base_rate_help'))
        with st.expander(t('base_rate_predictions')):
            scenario['euribor_predictions'] = st.data_editor(
                scenario['euribor_predictions'],
                num_rows='dynamic', use_container_width=True, hide_index=True,
                key=f'ep_{idx}')

    if scenario['rate_type'] == 'Mixed':
        c1, c2 = st.columns(2)
        with c1:
            scenario['fixed_period'] = st.number_input(
                t('fixed_period'), min_value=1,
                max_value=scenario['mortgage_term'],
                value=min(scenario['fixed_period'], scenario['mortgage_term']),
                step=1, format='%d', key=f'fp_{idx}')
        with c2:
            var_pos_options = [t('var_at_end'), t('var_at_beginning')]
            var_pos_values = ['Variable at End', 'Variable at Beginning']
            var_pos_idx = var_pos_values.index(scenario['variable_period_position'])
            var_pos_sel = st.radio(t('var_position'), var_pos_options, index=var_pos_idx, key=f'vp_{idx}')
            scenario['variable_period_position'] = var_pos_values[var_pos_options.index(var_pos_sel)]

    st.divider()
    with st.expander(t('secondary_loan_header')):
        scenario['secondary_loan_enabled'] = st.toggle(
            t('secondary_loan_enable'), value=scenario['secondary_loan_enabled'],
            key=f'sl_en_{idx}')
        if scenario['secondary_loan_enabled']:
            c1, c2 = st.columns(2)
            with c1:
                scenario['secondary_loan_amount_pct'] = st.number_input(
                    t('secondary_loan_pct'), min_value=0.0, max_value=100.0,
                    value=float(scenario['secondary_loan_amount_pct']),
                    step=1.0, format='%.1f', key=f'sl_pct_{idx}')
            with c2:
                scenario['secondary_loan_rate'] = st.number_input(
                    t('secondary_loan_rate'), min_value=0.0,
                    value=float(scenario['secondary_loan_rate']),
                    step=0.1, format='%.2f', key=f'sl_r_{idx}')
            c1, c2 = st.columns(2)
            with c1:
                scenario['secondary_loan_term'] = st.number_input(
                    t('secondary_loan_term'), min_value=1, max_value=40,
                    value=scenario['secondary_loan_term'], step=1, format='%d',
                    key=f'sl_t_{idx}')
            with c2:
                scenario['secondary_loan_dti_constrained'] = st.toggle(
                    t('secondary_loan_dti'), value=scenario['secondary_loan_dti_constrained'],
                    key=f'sl_dti_{idx}',
                    help=t('secondary_loan_dti_help'))
            timing_options = [t('secondary_loan_after'), t('secondary_loan_concurrent')]
            timing_values = ['After Primary Loan', 'Concurrent with Primary']
            timing_idx = timing_values.index(scenario['secondary_loan_timing'])
            timing_sel = st.radio(t('secondary_loan_timing'), timing_options, index=timing_idx, key=f'sl_tm_{idx}')
            scenario['secondary_loan_timing'] = timing_values[timing_options.index(timing_sel)]

    st.divider()
    with st.expander(t('bank_products_header')):
        st.caption(t('bank_products_caption'))
        if 'bank_products' not in scenario or scenario['bank_products'] is None:
            scenario['bank_products'] = create_default_owner_scenario('tmp')['bank_products']
        scenario['bank_products'] = st.data_editor(
            scenario['bank_products'],
            num_rows='dynamic',
            use_container_width=True,
            hide_index=True,
            key=f'bp_{idx}',
            column_config={
                'Active': st.column_config.CheckboxColumn(default=False),
                'Rate Discount (%)': st.column_config.NumberColumn(format='%.2f', min_value=0),
                'Annual Cost (% of loan)': st.column_config.NumberColumn(format='%.2f', min_value=0),
                'Annual Cost (EUR)': st.column_config.NumberColumn(format='%.0f', min_value=0),
            }
        )
        # Show summary
        active = scenario['bank_products'][scenario['bank_products']['Active'] == True]
        total_discount = active['Rate Discount (%)'].sum()
        total_cost_fixed = active['Annual Cost (EUR)'].sum()
        total_cost_pct = active['Annual Cost (% of loan)'].sum()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric('Total Rate Discount', f'-{total_discount:.2f}%')
        with c2:
            st.metric('Fixed Product Costs', f'€{total_cost_fixed:,.0f}/yr')
        with c3:
            st.metric('Variable Product Costs', f'{total_cost_pct:.2f}% of loan/yr')

    st.divider()
    st.subheader(t('costs_header'))
    c1, c2 = st.columns(2)
    with c1:
        scenario['transfer_tax'] = st.number_input(
            t('transfer_tax'), min_value=0.0,
            value=float(scenario['transfer_tax']),
            step=0.5, format='%.1f', key=f'tt_{idx}')
    with c2:
        scenario['registration_fee'] = st.number_input(
            t('registration_fee'), min_value=0,
            value=scenario['registration_fee'], step=100, format='%d',
            key=f'rf_{idx}')
    c1, c2 = st.columns(2)
    with c1:
        scenario['maintenance_pct'] = st.number_input(
            t('maintenance_pct'), min_value=0.0,
            value=float(scenario['maintenance_pct']),
            step=0.1, format='%.2f', key=f'mp_{idx}')
    with c2:
        scenario['maintenance_fixed'] = st.number_input(
            t('maintenance_fixed'), min_value=0.0,
            value=float(scenario['maintenance_fixed']),
            step=100.0, format='%.0f', key=f'mf_{idx}')
    c1, c2 = st.columns(2)
    with c1:
        scenario['insurance_pct'] = st.number_input(
            t('insurance_pct'), min_value=0.0,
            value=float(scenario.get('insurance_pct', 0.0)),
            step=0.05, format='%.2f', key=f'ip_{idx}')
    with c2:
        scenario['insurance_fixed'] = st.number_input(
            'Fixed Insurance (EUR/yr)', min_value=0.0,
            value=float(scenario.get('insurance_fixed', 0.0)),
            step=50.0, format='%.0f', key=f'if_{idx}')

    with st.expander(t('selling_costs_header')):
        scenario['selling_commission'] = st.number_input(
            t('selling_commission'), min_value=0.0,
            value=float(scenario['selling_commission']),
            step=0.5, format='%.1f', key=f'sc_{idx}')
        plusv_options = [t('plusvalia_flat_mode'), t('plusvalia_pct_mode')]
        plusv_values = ['Flat Amount', '% of Appreciation']
        plusv_idx = plusv_values.index(scenario['plusvalia_mode'])
        plusv_sel = st.radio(t('plusvalia_mode'), plusv_options, index=plusv_idx, key=f'pm_{idx}')
        scenario['plusvalia_mode'] = plusv_values[plusv_options.index(plusv_sel)]
        if scenario['plusvalia_mode'] == 'Flat Amount':
            scenario['plusvalia_flat'] = st.number_input(
                t('plusvalia_flat'), min_value=0,
                value=scenario['plusvalia_flat'], step=500, format='%d',
                key=f'pf_{idx}')
        else:
            scenario['plusvalia_pct'] = st.number_input(
                t('plusvalia_pct'), min_value=0.0,
                value=float(scenario['plusvalia_pct']),
                step=0.5, format='%.1f', key=f'pp_{idx}')


def render_rent_invest_config(scenario, idx):
    st.subheader(t('rent_header'))
    mode_options = [t('rent_mode_pct'), t('rent_mode_fixed')]
    mode_values = ['% of Property Value', 'Fixed Amount']
    mode_idx = mode_values.index(scenario['rent_mode'])
    mode_sel = st.radio(t('rent_mode'), mode_options, index=mode_idx, key=f'rm_{idx}')
    scenario['rent_mode'] = mode_values[mode_options.index(mode_sel)]

    if scenario['rent_mode'] == '% of Property Value':
        c1, c2 = st.columns(2)
        with c1:
            scenario['reference_property_value'] = st.number_input(
                t('ref_prop_value'), min_value=0,
                value=int(scenario.get('reference_property_value', 237000)),
                step=1000, format='%d', key=f'rpv_{idx}',
                help=t('ref_prop_value_help'))
        with c2:
            scenario['reference_appreciation'] = st.number_input(
                t('ref_appreciation'), min_value=0.0,
                value=float(scenario.get('reference_appreciation', 4.5)),
                step=0.1, format='%.2f', key=f'ra_{idx}')
        scenario['rent_yield'] = st.number_input(
            t('rent_yield'), min_value=0.0,
            value=float(scenario.get('rent_yield', 5.0)),
            step=0.1, format='%.2f', key=f'ry_{idx}',
            help=t('rent_yield_help'))
        ref_pv = scenario['reference_property_value']
        if ref_pv > 0:
            st.metric(t('calc_monthly_rent'),
                      f"€{ref_pv * scenario['rent_yield'] / 100 / 12:,.2f}")
        else:
            st.info(t('auto_rent_info'))
    else:
        scenario['monthly_rent_fixed'] = st.number_input(
            t('monthly_rent'), min_value=0,
            value=int(scenario.get('monthly_rent_fixed', 1000)),
            step=50, format='%d', key=f'mrf_{idx}')


    scenario['deposit_months'] = st.number_input(
        t('deposit_months'), min_value=0, max_value=6,
        value=int(scenario.get('deposit_months', 1)),
        step=1, format='%d', key=f'dm_{idx}',
        help=t('deposit_months_help'))

    with st.expander(t('contract_regime')):
        st.caption(t('contract_regime_caption'))
        scenario['contract_length'] = st.number_input(
            t('contract_length'), min_value=1, max_value=20,
            value=scenario.get('contract_length', 5),
            step=1, format='%d', key=f'cl_{idx}')
        inc_options = [t('increase_itp'), t('increase_custom'), t('increase_market')]
        inc_values = ['Inflation (ITP)', 'Custom %', 'Market Value']
        inc_idx = inc_values.index(scenario.get('in_contract_increase', 'Inflation (ITP)'))
        inc_sel = st.selectbox(t('in_contract_increase'), inc_options, index=inc_idx, key=f'ici_{idx}')
        scenario['in_contract_increase'] = inc_values[inc_options.index(inc_sel)]
        if scenario['in_contract_increase'] == 'Custom %':
            scenario['custom_increase'] = st.number_input(
                t('custom_increase'), min_value=0.0,
                value=float(scenario.get('custom_increase', 2.5)),
                step=0.1, format='%.2f', key=f'ci_{idx}')


def render_landlord_config(scenario, idx):
    # Property + loan + costs (reuse owner renderer)
    render_owner_occupier_config(scenario, idx)

    st.divider()
    st.subheader(t('rental_income_header'))
    mode_options = [t('rent_mode_pct'), t('rent_mode_fixed')]
    mode_values = ['% of Property Value', 'Fixed Amount']
    mode_idx = mode_values.index(scenario['rent_mode'])
    mode_sel = st.radio(t('rent_mode'), mode_options, index=mode_idx, key=f'll_rm_{idx}')
    scenario['rent_mode'] = mode_values[mode_options.index(mode_sel)]

    if scenario['rent_mode'] == '% of Property Value':
        c1, c2 = st.columns(2)
        with c1:
            scenario['reference_property_value'] = st.number_input(
                t('ref_prop_value'), min_value=0,
                value=int(scenario.get('reference_property_value',
                                       scenario.get('property_value', 237000))),
                step=1000, format='%d', key=f'll_rpv_{idx}')
        with c2:
            scenario['reference_appreciation'] = st.number_input(
                t('ref_appreciation'), min_value=0.0,
                value=float(scenario.get('reference_appreciation',
                                         scenario.get('yearly_appreciation', 4.5))),
                step=0.1, format='%.2f', key=f'll_ra_{idx}')
        scenario['rent_yield'] = st.number_input(
            t('rent_yield'), min_value=0.0,
            value=float(scenario.get('rent_yield', 5.0)),
            step=0.1, format='%.2f', key=f'll_ry_{idx}')
        ref = scenario['reference_property_value']
        if ref > 0:
            st.metric(t('calc_monthly_rent'),
                      f"€{ref * scenario['rent_yield'] / 100 / 12:,.2f}")
    else:
        scenario['monthly_rent_fixed'] = st.number_input(
            t('monthly_rent'), min_value=0,
            value=int(scenario.get('monthly_rent_fixed', 1000)),
            step=50, format='%d', key=f'll_mrf_{idx}')

    with st.expander(t('contract_regime')):
        scenario['contract_length'] = st.number_input(
            t('contract_length'), min_value=1, max_value=20,
            value=scenario.get('contract_length', 5),
            step=1, format='%d', key=f'll_cl_{idx}')
        inc_options = [t('increase_itp'), t('increase_custom'), t('increase_market')]
        inc_values = ['Inflation (ITP)', 'Custom %', 'Market Value']
        inc_idx = inc_values.index(scenario.get('in_contract_increase', 'Inflation (ITP)'))
        inc_sel = st.selectbox(t('in_contract_increase'), inc_options, index=inc_idx, key=f'll_ici_{idx}')
        scenario['in_contract_increase'] = inc_values[inc_options.index(inc_sel)]
        if scenario['in_contract_increase'] == 'Custom %':
            scenario['custom_increase'] = st.number_input(
                t('custom_increase'), min_value=0.0,
                value=float(scenario.get('custom_increase', 2.5)),
                step=0.1, format='%.2f', key=f'll_ci_{idx}')

    with st.expander(t('landlord_expenses')):
        c1, c2 = st.columns(2)
        with c1:
            scenario['vacancy_months'] = st.number_input(
                t('vacancy_months'), min_value=0.0, max_value=12.0,
                value=float(scenario.get('vacancy_months', 1.0)),
                step=0.5, format='%.1f', key=f'll_vm_{idx}')
        with c2:
            scenario['agent_commission_pct'] = st.number_input(
                t('agent_commission'), min_value=0.0,
                value=float(scenario.get('agent_commission_pct', 8.0)),
                step=0.5, format='%.1f', key=f'll_ac_{idx}')

    with st.expander(t('bad_tenant_header')):
        scenario['bad_tenant_enabled'] = st.toggle(
            t('bad_tenant_enable'),
            value=scenario.get('bad_tenant_enabled', False),
            key=f'll_bt_{idx}')
        if scenario['bad_tenant_enabled']:
            c1, c2 = st.columns(2)
            with c1:
                scenario['bad_tenant_months_unpaid'] = st.number_input(
                    t('bad_tenant_months'), min_value=1, max_value=24,
                    value=scenario.get('bad_tenant_months_unpaid', 6),
                    step=1, format='%d', key=f'll_btm_{idx}')
            with c2:
                scenario['bad_tenant_year'] = st.number_input(
                    t('bad_tenant_year'), min_value=1, max_value=40,
                    value=scenario.get('bad_tenant_year', 10),
                    step=1, format='%d', key=f'll_bty_{idx}')
            c1, c2 = st.columns(2)
            with c1:
                scenario['bad_tenant_eviction_cost'] = st.number_input(
                    t('bad_tenant_eviction'), min_value=0,
                    value=scenario.get('bad_tenant_eviction_cost', 3000),
                    step=100, format='%d', key=f'll_bte_{idx}')
            with c2:
                scenario['bad_tenant_repair_cost'] = st.number_input(
                    t('bad_tenant_repair'), min_value=0,
                    value=scenario.get('bad_tenant_repair_cost', 5000),
                    step=100, format='%d', key=f'll_btr_{idx}')


    with st.expander('🏠 IRPF Deductions (Depreciation & Land Ratio)'):
        st.caption('Depreciation of construction value is deductible from rental income. '
                   'Land is not depreciable, so only the construction portion qualifies.')
        c1, c2 = st.columns(2)
        with c1:
            scenario['depreciation_rate'] = st.number_input(
                'Depreciation Rate (% of construction/yr)', min_value=0.0,
                value=float(scenario.get('depreciation_rate', 3.0)),
                step=0.5, format='%.1f', key=f'll_depr_{idx}',
                help='Annual depreciation of construction value (typically 3% in Spain)')
        with c2:
            scenario['land_ratio'] = st.number_input(
                'Land Ratio (% of property value)', min_value=0.0, max_value=100.0,
                value=float(scenario.get('land_ratio', 20.0)),
                step=5.0, format='%.0f', key=f'll_land_{idx}',
                help='Portion of property value that is land (not depreciable). Typically 20-30%.')
        # Show calculated depreciation
        prop_val = scenario.get('property_value', 237000)
        constr = prop_val * (1 - scenario.get('land_ratio', 20) / 100)
        annual_depr = constr * scenario.get('depreciation_rate', 3.0) / 100
        st.metric('Annual Depreciation Deduction', f'€{annual_depr:,.0f}')

# ============================================================================
# SCENARIO TABS
# ============================================================================

if not st.session_state.scenarios:
    st.info(t('no_scenarios'))
else:
    st.header(t('config_header'))
    tabs = st.tabs([s['name'] for s in st.session_state.scenarios])

    for idx, tab in enumerate(tabs):
        with tab:
            sc = st.session_state.scenarios[idx]
            c1, c2 = st.columns([3, 1])
            with c1:
                sc['name'] = st.text_input(t('scenario_name_label'), value=sc['name'],
                                           key=f'nm_{idx}')
            with c2:
                st.markdown('<br>', unsafe_allow_html=True)
                if st.button(t('delete_btn'), key=f'del_{idx}', type='secondary'):
                    st.session_state.scenarios.pop(idx)
                    st.session_state.results = None
                    st.rerun()
            st.caption(f"**{t('type_label')}:** {sc['type']}")
            st.divider()

            if sc['type'] == 'Owner-Occupier':
                render_owner_occupier_config(sc, idx)
            elif sc['type'] == 'Rent + Invest':
                render_rent_invest_config(sc, idx)
            else:
                render_landlord_config(sc, idx)

# ============================================================================
# RESULTS
# ============================================================================

if st.session_state.results is not None:
    res = st.session_state.results
    scenarios = res.get('scenarios', {})

    if not scenarios:
        st.warning(t('no_results'))
    else:
        st.divider()
        st.header(t('results_header'))

        # ── Summary table ─────────────────────────────────────────
        st.subheader(t('summary_header'))
        rows = []
        for name, d in scenarios.items():
            f = d.get('final', {})
            rows.append({
                t('col_scenario'): name,
                t('col_type'): d['type'].title(),
                t('col_initial_prop'): f.get('property_value', d.get('property_value_initial')) or 0,
                t('col_bank_loan'): d.get('bank_loan') or 0,
                t('col_upfront'): d.get('upfront', 0),
                t('col_final_prop'): f.get('property_value') or 0,
                t('col_net_sale'): f.get('net_from_sale', 0),
                t('col_portfolio'): f.get('portfolio_value', 0),
                t('col_total_irpf'): f.get('property_irpf', 0) + f.get('portfolio_irpf', 0),
                t('col_net_worth'): f.get('total_net_worth', 0),
            })
        df = pd.DataFrame(rows)

        for c in [c for c in df.columns if c != t('col_scenario') and c != t('col_type')]:
            df[c] = df[c].apply(lambda x: f'€{x:,.0f}')
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Winner highlight
        if rows:
            winner = max(rows, key=lambda r: r[t('col_net_worth')])
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric(t('winner_label'), winner[t('col_scenario')],
                          f"€{winner[t('col_net_worth')]:,.0f}")
            with c2:
                others = [r for r in rows if r[t('col_scenario')] != winner[t('col_scenario')]]
                if others:
                    second = max(others, key=lambda r: r[t('col_net_worth')])
                    delta = winner[t('col_net_worth')] - second[t('col_net_worth')]
                    st.metric(t('advantage_label'),
                              f"€{delta:,.0f}",
                              f"{delta / max(1, abs(second[t('col_net_worth')])) * 100:.1f}%")
            with c3:
                st.metric(t('cash_base_label'), f"€{res.get('cash_base', 0):,.0f}")

        st.divider()

        # ── Year-by-year comparison ───────────────────────────────
        st.subheader(t('yearly_header'))
        yearly_rows = []
        for yr in range(1, sim_years + 1):
            row = {t('col_year'): yr}
            for name, d in scenarios.items():
                mo_data = d.get('monthly', [])
                mi = yr * 12 - 1
                if mi < len(mo_data):
                    m = mo_data[mi]
                    row[f'{name} {t("cost_per_mo")}'] = m['total_housing_cost']
                    row[f'{name} {t("portfolio_label")}'] = m['portfolio']
                    pv_cur = m.get('property_value')
                    prop_equity = (pv_cur or 0) - m.get('bank_balance', 0) - m.get('sec_balance', 0)
                    row[f'{name} {t("net_worth_est")}'] = prop_equity + m['portfolio']
            yearly_rows.append(row)
        ydf = pd.DataFrame(yearly_rows)
        for c in [c for c in ydf.columns if c != t('col_year')]:
            ydf[c] = ydf[c].apply(lambda x: f'€{x:,.0f}')
        st.dataframe(ydf, use_container_width=True,
                     hide_index=True, height=min(400, 40 + 35 * len(ydf)))

        st.divider()

        # ── Charts ────────────────────────────────────────────────
        st.subheader(t('charts_header'))

        # Net worth over time
        fig_nw = go.Figure()
        for name, d in scenarios.items():
            years, nws = [], []
            for yr in range(1, sim_years + 1):
                mi = yr * 12 - 1
                if mi < len(d.get('monthly', [])):
                    m = d['monthly'][mi]
                    pv_cur = m.get('property_value') or 0
                    equity = pv_cur - m.get('bank_balance', 0) - m.get('sec_balance', 0)
                    years.append(yr)
                    nws.append(equity + m['portfolio'])
            fig_nw.add_trace(go.Scatter(x=years, y=nws, mode='lines+markers',
                                        name=name, line=dict(width=3)))
        fig_nw.update_layout(title=t('chart_nw'),
                             xaxis_title=t('col_year'), yaxis_title='EUR',
                             hovermode='x unified', height=500)
        st.plotly_chart(fig_nw, use_container_width=True)

        # Portfolio over time
        fig_port = go.Figure()
        for name, d in scenarios.items():
            years, ports = [], []
            for yr in range(1, sim_years + 1):
                mi = yr * 12 - 1
                if mi < len(d.get('monthly', [])):
                    years.append(yr)
                    ports.append(d['monthly'][mi]['portfolio'])
            fig_port.add_trace(go.Scatter(x=years, y=ports, mode='lines+markers',
                                          name=name, line=dict(width=3)))
        fig_port.update_layout(title=t('chart_portfolio'),
                               xaxis_title=t('col_year'), yaxis_title='EUR',
                               hovermode='x unified', height=500)
        st.plotly_chart(fig_port, use_container_width=True)

        # Final breakdown bar chart
        names_list = list(scenarios.keys())
        prop_equities, port_values = [], []
        for name in names_list:
            f = scenarios[name].get('final', {})
            prop_equities.append(f.get('net_from_sale', 0) - f.get('property_irpf', 0))
            port_values.append(f.get('portfolio_value', 0) - f.get('portfolio_irpf', 0))
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=names_list, y=prop_equities, name=t('prop_after_tax'),
                                 marker_color='lightblue'))
        fig_bar.add_trace(go.Bar(x=names_list, y=port_values, name=t('port_after_tax'),
                                 marker_color='lightgreen'))
        fig_bar.update_layout(title=t('chart_breakdown'),
                              yaxis_title='EUR', barmode='stack', height=500)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Monthly cost over time
        fig_cost = go.Figure()
        for name, d in scenarios.items():
            years, costs = [], []
            for yr in range(1, sim_years + 1):
                mi = yr * 12 - 1
                if mi < len(d.get('monthly', [])):
                    years.append(yr)
                    costs.append(d['monthly'][mi]['total_housing_cost'])
            fig_cost.add_trace(go.Scatter(x=years, y=costs, mode='lines+markers',
                                          name=name, line=dict(width=3)))
        fig_cost.update_layout(title=t('chart_cost'),
                               xaxis_title=t('col_year'), yaxis_title='EUR/month',
                               hovermode='x unified', height=500)
        st.plotly_chart(fig_cost, use_container_width=True)

        st.divider()

        # ── Month-by-month detail ────────────────────────────────
        st.subheader(t('monthly_detail_header'))
        for name, d in scenarios.items():
            with st.expander(f'📋 {name}'):
                mdata = d.get('monthly', [])
                if mdata:
                    mdf = pd.DataFrame(mdata)
                    display_cols = ['month', 'year', 'property_value',
                                    'bank_payment', 'secondary_payment',
                                    'maintenance', 'insurance',
                                    'rent_paid', 'rent_received',
                                    'total_housing_cost', 'surplus_invested',
                                    'portfolio', 'bank_balance', 'sec_balance']
                    display_cols = [c for c in display_cols if c in mdf.columns]
                    mdf_show = mdf[display_cols]
                    st.dataframe(mdf_show, use_container_width=True,
                                 hide_index=True, height=400)
                    csv = mdf_show.to_csv(index=False)
                    st.download_button(t('download_csv'), csv,
                                       file_name=f'{name}_monthly.csv',
                                       mime='text/csv')
                else:
                    st.info(t('no_monthly_data'))
