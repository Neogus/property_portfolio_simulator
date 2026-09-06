"""
Mortgage Calculator — Simulation Engine
Pure Python (no Streamlit). All percentage inputs are in % form (e.g. 3.0 = 3%).
"""
from typing import List, Dict, Any
import math


# ════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ════════════════════════════════════════════════════════════════════

def run_simulation(scenarios: List[Dict[str, Any]],
                   global_params: Dict[str, Any]) -> Dict[str, Any]:
    monthly_net_income = global_params['monthly_net_income']
    bank_dti_pct = global_params['bank_dti_pct']
    inflation_rate = global_params['inflation_rate'] / 100
    portfolio_return = global_params['portfolio_return'] / 100
    simulation_years = global_params['simulation_years']
    irpf_brackets = global_params['irpf_brackets']
    port_m = (1 + portfolio_return) ** (1 / 12) - 1

    # ── Step 1: resolve "Max Affordable" property values ──────────
    for sc in scenarios:
        if sc['type'] in ('owner', 'landlord'):
            if sc.get('property_value_mode') == 'Max Affordable':
                sc['property_value'] = _max_affordable(sc, monthly_net_income, bank_dti_pct)

    # ── Step 1.5: propagate property value to rent/landlord-rent refs ─
    first_prop_val = None
    first_appr = 4.5
    for sc in scenarios:
        if sc['type'] in ('owner', 'landlord') and sc.get('property_value', 0) > 0:
            first_prop_val = sc['property_value']
            first_appr = sc.get('yearly_appreciation', 4.5)
            break
    if first_prop_val:
        for sc in scenarios:
            if sc['type'] == 'rent':
                rc = sc.get('rent', {})
                if rc.get('mode') == 'pct_of_value' and rc.get('reference_property_value', 0) <= 0:
                    rc['reference_property_value'] = first_prop_val
                    rc.setdefault('reference_appreciation', first_appr)
            if sc['type'] == 'landlord':
                rc = sc.get('rent_config', {})
                if rc.get('mode') == 'pct_of_value' and rc.get('reference_property_value', 0) <= 0:
                    rc['reference_property_value'] = first_prop_val
                    rc.setdefault('reference_appreciation', first_appr)

    # ── Step 2: CASH base = max upfront across owner/landlord ─────
    cash_base = 0.0
    for sc in scenarios:
        if sc['type'] in ('owner', 'landlord'):
            cash_base = max(cash_base, _upfront(sc))

    # ── Step 3: simulate each scenario (costs only for non-landlord)
    results: Dict[str, Any] = {}
    sc_map: Dict[str, Dict] = {}
    for sc in scenarios:
        name = sc['name']
        sc_map[name] = sc
        if sc['type'] == 'owner':
            results[name] = _sim_owner(sc, global_params, cash_base, simulation_years)
        elif sc['type'] == 'rent':
            results[name] = _sim_rent(sc, global_params, cash_base, simulation_years)
        elif sc['type'] == 'landlord':
            results[name] = _sim_landlord(sc, global_params, cash_base, port_m,
                                          simulation_years, irpf_brackets)

    # ── Step 4: surplus-equalize non-landlord, build portfolios ───
    _equalize(results, cash_base, port_m, simulation_years)

    # ── Step 5: final net worth ───────────────────────────────────
    for name, res in results.items():
        _final_net_worth(res, sc_map[name], irpf_brackets)

    return {'cash_base': cash_base, 'scenarios': results}


# ════════════════════════════════════════════════════════════════════
#  MAX-AFFORDABLE PROPERTY
# ════════════════════════════════════════════════════════════════════

def _max_affordable(sc, income, dti_pct):
    dti = dti_pct / 100
    max_pmt = income * dti
    loan = sc['loan']
    rate = loan['fixed_rate'] / 100  # use fixed for qualification
    term = loan['term_years']
    ltv = loan['ltv_pct'] / 100

    sec = sc.get('secondary_loan', {})
    if sec.get('enabled') and not sec.get('paid_after_primary') and sec.get('constrained_by_dti'):
        # Both loans count against DTI, paid concurrently
        sec_rate = sec.get('interest_rate', 0) / 100
        sec_term = sec.get('term_years', 5)
        sec_pct = sec.get('amount_pct', 20) / 100
        # Iterative: find property where bank_pmt + sec_pmt <= max_pmt
        lo, hi = 0, income * 1000
        for _ in range(80):
            mid = (lo + hi) / 2
            bp = _french_pmt(mid * ltv, rate, term)
            sp = _french_pmt(mid * sec_pct, sec_rate, sec_term)
            if bp + sp <= max_pmt:
                lo = mid
            else:
                hi = mid
        return round(lo, 2)

    # Standard: only bank payment limited by DTI
    max_loan = _max_principal(max_pmt, rate, term)
    return round(max_loan / ltv, 2)


# ════════════════════════════════════════════════════════════════════
#  LOAN HELPERS
# ════════════════════════════════════════════════════════════════════

def _french_pmt(principal, annual_rate, years):
    if principal <= 0:
        return 0.0
    if annual_rate <= 0:
        return principal / (years * 12)
    r = annual_rate / 12
    n = years * 12
    return principal * r * (1 + r)**n / ((1 + r)**n - 1)


def _max_principal(max_payment, annual_rate, years):
    if max_payment <= 0:
        return 0
    if annual_rate <= 0:
        return max_payment * years * 12
    r = annual_rate / 12
    n = years * 12
    return max_payment * ((1 + r)**n - 1) / (r * (1 + r)**n)


def _current_rate(loan, year_in_loan):
    """Annual interest rate for the given year of the loan."""
    rt = loan['rate_type']
    if rt == 'Fixed':
        discount = loan.get('product_rate_discount', 0) / 100
        return max(0, loan['fixed_rate'] / 100 - discount)
    if rt == 'Variable':
        return _variable_rate(loan, year_in_loan)
    # Mixed
    fy = loan.get('fixed_years', 10)
    if loan.get('variable_at_end', True):
        discount = loan.get('product_rate_discount', 0) / 100
        return max(0, loan['fixed_rate'] / 100 - discount) if year_in_loan <= fy else _variable_rate(loan, year_in_loan)
    else:
        variable_years = loan['term_years'] - fy
        discount = loan.get('product_rate_discount', 0) / 100
        return _variable_rate(loan, year_in_loan) if year_in_loan <= variable_years else max(0, loan['fixed_rate'] / 100 - discount)


def _variable_rate(loan, year):
    preds = loan.get('euribor_predictions', {})
    default = loan.get('default_euribor', 2.5)
    spread = loan.get('euribor_spread', 1.0)
    euribor = default
    for y in sorted(int(k) for k in preds):
        if y <= year:
            euribor = preds[str(y)]
        else:
            break
    discount = loan.get('product_rate_discount', 0) / 100
    return max(0, (euribor + spread) / 100 - discount)


def _loan_payment(loan, balance, month_in_loan, total_months):
    """Monthly payment for primary loan at a given month."""
    if balance <= 0 or month_in_loan < 1 or month_in_loan > total_months:
        return 0.0
    year = (month_in_loan - 1) // 12 + 1
    annual_rate = _current_rate(loan, year)
    r = annual_rate / 12
    remaining = total_months - month_in_loan + 1
    if loan.get('amortization', 'French') == 'French':
        if r <= 0:
            return balance / remaining
        f = (1 + r) ** remaining
        return balance * r * f / (f - 1)
    else:  # Linear
        return balance / remaining + balance * r


def _update_balance(balance, payment, annual_rate):
    """Return (new_balance, interest_portion)."""
    if balance <= 0:
        return 0.0, 0.0
    interest = balance * annual_rate / 12
    principal = payment - interest
    return max(0.0, balance - principal), interest


def _sec_payment(sec, balance, month_in_sec, total_sec_months):
    """Monthly payment for secondary loan."""
    if balance <= 0 or month_in_sec < 1 or month_in_sec > total_sec_months:
        return 0.0
    rate = sec.get('interest_rate', 0) / 100
    r = rate / 12
    remaining = total_sec_months - month_in_sec + 1
    if r <= 0:
        return balance / remaining
    f = (1 + r) ** remaining
    return balance * r * f / (f - 1)


# ════════════════════════════════════════════════════════════════════
#  UPFRONT COST
# ════════════════════════════════════════════════════════════════════

def _upfront(sc):
    pv = sc.get('property_value', 0)
    loan = sc['loan']
    costs = sc.get('costs', {})
    sec = sc.get('secondary_loan', {})

    ltv = loan['ltv_pct'] / 100
    sec_pct = sec.get('amount_pct', 0) / 100 if sec.get('enabled') else 0
    down_pct = max(0, 1 - ltv - sec_pct)
    down = pv * down_pct
    tax = pv * costs.get('transfer_tax_pct', 10) / 100
    reg = costs.get('registration_fee', 2000)
    return down + tax + reg


# ════════════════════════════════════════════════════════════════════
#  RENT HELPERS
# ════════════════════════════════════════════════════════════════════

def _initial_rent(rc):
    if rc.get('mode') == 'pct_of_value':
        return rc.get('reference_property_value', 0) * rc.get('rent_yield_pct', 5) / 100 / 12
    return rc.get('fixed_monthly_rent', 1000)


def _rent_for_year(rc, prev_rent, year, inflation):
    """Return monthly rent for the given year (year >= 1)."""
    clen = rc.get('contract_years', 5)
    inc = rc.get('increase_type', 'Inflation (ITP)')

    # Contract renewal → reset to market
    if year > 1 and (year - 1) % clen == 0:
        ref = rc.get('reference_property_value', 0)
        appr = rc.get('reference_appreciation', 4.5) / 100
        yld = rc.get('rent_yield_pct', 5) / 100
        return ref * (1 + appr) ** (year - 1) * yld / 12

    if year == 1:
        return _initial_rent(rc)

    # Within contract
    if inc == 'Inflation (ITP)':
        return prev_rent * (1 + inflation)
    elif inc == 'Custom %':
        return prev_rent * (1 + rc.get('custom_increase_pct', 2.5) / 100)
    elif inc == 'Market Value':
        ref = rc.get('reference_property_value', 0)
        appr = rc.get('reference_appreciation', 4.5) / 100
        yld = rc.get('rent_yield_pct', 5) / 100
        return ref * (1 + appr) ** (year - 1) * yld / 12
    return prev_rent


# ════════════════════════════════════════════════════════════════════
#  SCENARIO SIMULATORS  (costs only — portfolios built in equalize)
# ════════════════════════════════════════════════════════════════════

def _sim_owner(sc, gp, cash_base, sim_years):
    pv = sc['property_value']
    loan = sc['loan']
    costs = sc.get('costs', {})
    sec = sc.get('secondary_loan', {})
    appr = sc.get('yearly_appreciation', 0) / 100
    inflation = gp['inflation_rate'] / 100
    upfront = _upfront(sc)

    bank_loan_amt = pv * loan['ltv_pct'] / 100
    bank_term_mo = loan['term_years'] * 12
    sec_enabled = sec.get('enabled', False)
    sec_loan_amt = pv * sec.get('amount_pct', 0) / 100 if sec_enabled else 0
    sec_term_mo = sec.get('term_years', 5) * 12 if sec_enabled else 0
    sec_after = sec.get('paid_after_primary', True)

    bank_bal = bank_loan_amt
    sec_bal = sec_loan_amt
    monthly = []

    for month in range(1, sim_years * 12 + 1):
        year = (month - 1) // 12 + 1
        cur_pv = pv * (1 + appr) ** (year - 1)

        # ── bank payment ──
        bp = _loan_payment(loan, bank_bal, month, bank_term_mo)
        yr_in_loan = (month - 1) // 12 + 1
        ann_rate = _current_rate(loan, yr_in_loan) if month <= bank_term_mo else 0
        bank_bal, _ = _update_balance(bank_bal, bp, ann_rate) if month <= bank_term_mo else (bank_bal, 0)

        # ── secondary payment ──
        sp = 0.0
        if sec_enabled and sec_bal > 0:
            if sec_after:
                sec_mo = month - bank_term_mo  # month within secondary
                sp = _sec_payment(sec, sec_bal, sec_mo, sec_term_mo)
                if sec_mo >= 1:
                    sec_rate = sec.get('interest_rate', 0) / 100
                    sec_bal, _ = _update_balance(sec_bal, sp, sec_rate)
            else:
                sp = _sec_payment(sec, sec_bal, month, sec_term_mo)
                if month <= sec_term_mo:
                    sec_rate = sec.get('interest_rate', 0) / 100
                    sec_bal, _ = _update_balance(sec_bal, sp, sec_rate)

        maint = cur_pv * costs.get('maintenance_pct', 1) / 100 / 12 + costs.get('maintenance_fixed', 0) / 12
        ins = cur_pv * costs.get('insurance_pct', 0) / 100 / 12 + costs.get('insurance_fixed', 0) / 12
        # Product costs (bank bonificaciones)
        prod_cost_pct = costs.get('product_cost_pct_loan', 0) / 100
        prod_cost_fixed = costs.get('product_cost_fixed', 0)
        prod_cost_mo = bank_bal * prod_cost_pct / 12 + prod_cost_fixed / 12
        total = bp + sp + maint + ins + prod_cost_mo

        monthly.append({
            'month': month, 'year': year,
            'property_value': cur_pv,
            'bank_payment': bp, 'secondary_payment': sp,
            'maintenance': maint, 'insurance': ins,
            'rent_paid': 0, 'rent_received': 0,
            'total_housing_cost': total,
            'surplus_invested': 0, 'portfolio': 0,
            'cumulative_invested': 0,
            'bank_balance': bank_bal, 'sec_balance': sec_bal,
            'net_rental_income': 0,
            'product_costs': prod_cost_mo,
        })

    return {
        'type': 'owner', 'upfront': upfront,
        'property_value_initial': pv,
        'bank_loan': bank_loan_amt, 'sec_loan': sec_loan_amt,
        'monthly': monthly, 'final': {},
    }


def _sim_rent(sc, gp, cash_base, sim_years):
    rc = sc.get('rent', {})
    inflation = gp['inflation_rate'] / 100
    deposit_months = rc.get('deposit_months', 1)
    rent = _initial_rent(rc)
    initial_deposit = deposit_months * rent
    deposit_held = initial_deposit
    monthly = []
    for month in range(1, sim_years * 12 + 1):
        year = (month - 1) // 12 + 1
        mo_in_yr = (month - 1) % 12 + 1
        
        # At contract renewal (start of year after first contract), recalculate deposit
        contract_len = rc.get('contract_years', 5)
        deposit_delta = 0
        if year > 1 and (year - 1) % contract_len == 0:
            # Contract renewal - rent resets to market
            rent = _rent_for_year(rc, rent, year, inflation)
            new_deposit = deposit_months * rent
            deposit_delta = new_deposit - deposit_held
            deposit_held = new_deposit
        elif mo_in_yr == 1:
            rent = _rent_for_year(rc, rent, year, inflation)
        monthly.append({
            'month': month, 'year': year,
            'property_value': None,
            'bank_payment': 0, 'secondary_payment': 0,
            'maintenance': 0, 'insurance': 0,
            'rent_paid': rent, 'rent_received': 0,
            'total_housing_cost': rent + deposit_delta,
            'surplus_invested': 0, 'portfolio': 0,
            'cumulative_invested': 0,
            'bank_balance': 0, 'sec_balance': 0,
            'net_rental_income': 0,
            'deposit_held': deposit_held,
        })

    return {
        'type': 'rent', 'upfront': 0,
        'property_value_initial': None,
        'bank_loan': None, 'sec_loan': None,
        'monthly': monthly, 'final': {},
        'deposit': initial_deposit,
    }


# ────────────────────────────────────────────────────────────────────
#  LANDLORD — standalone portfolio (not in equalization)
# ────────────────────────────────────────────────────────────────────

def _sim_landlord(sc, gp, cash_base, port_m, sim_years, irpf_brackets):
    pv = sc['property_value']
    loan = sc['loan']
    costs = sc.get('costs', {})
    sec = sc.get('secondary_loan', {})
    rc = sc.get('rent_config', {})
    ll = sc.get('landlord', {})
    appr = sc.get('yearly_appreciation', 0) / 100
    inflation = gp['inflation_rate'] / 100

    upfront = _upfront(sc)
    bank_loan_amt = pv * loan['ltv_pct'] / 100
    bank_term_mo = loan['term_years'] * 12
    sec_enabled = sec.get('enabled', False)
    sec_loan_amt = pv * sec.get('amount_pct', 0) / 100 if sec_enabled else 0
    sec_term_mo = sec.get('term_years', 5) * 12 if sec_enabled else 0
    sec_after = sec.get('paid_after_primary', True)

    vacancy = ll.get('vacancy_months_per_year', 1)
    vac_factor = (12 - vacancy) / 12
    agent_pct = ll.get('agent_commission_pct', 8) / 100
    contract_yrs = rc.get('contract_years', 5)
    bad_enabled = ll.get('bad_tenant_enabled', False)
    bad_year = ll.get('bad_tenant_occurs_at_year', 10)

    # IRPF deduction params
    depreciation_rate = ll.get('depreciation_rate', 3.0) / 100
    land_ratio = ll.get('land_ratio', 20.0) / 100
    construction_value = pv * (1 - land_ratio)
    annual_depreciation = construction_value * depreciation_rate

    bank_bal = bank_loan_amt
    sec_bal = sec_loan_amt
    portfolio = max(0, cash_base - upfront)
    cum_inv = portfolio
    rent = _initial_rent(rc)
    monthly = []

    # Yearly accumulators for IRPF
    yr_gross_rent = 0.0
    yr_mortgage_interest = 0.0
    yr_sec_interest = 0.0
    yr_maintenance = 0.0
    yr_insurance = 0.0
    yr_agent = 0.0
    yr_legal_costs = 0.0       # eviction = separate deductible category
    yr_bad_debt = 0.0          # unpaid rent = deductible after 6mo
    yr_repair_from_tenant = 0.0  # bad tenant repair goes to maintenance
    yr_actual_cashflow = 0.0

    # Carry-forward: list of (excess_amount, year_created)
    carry_forward = []

    for month in range(1, sim_years * 12 + 1):
        year = (month - 1) // 12 + 1
        mo_in_yr = (month - 1) % 12 + 1
        cur_pv = pv * (1 + appr) ** (year - 1)

        # Reset yearly accumulators at start of year
        if mo_in_yr == 1:
            yr_gross_rent = 0.0
            yr_mortgage_interest = 0.0
            yr_sec_interest = 0.0
            yr_maintenance = 0.0
            yr_insurance = 0.0
            yr_agent = 0.0
            yr_legal_costs = 0.0
            yr_bad_debt = 0.0
            yr_repair_from_tenant = 0.0
            yr_actual_cashflow = 0.0
            rent = _rent_for_year(rc, rent, year, inflation)

        # ── bank payment (split interest vs principal) ──
        bp = _loan_payment(loan, bank_bal, month, bank_term_mo)
        yr_in_loan = (month - 1) // 12 + 1
        ann_rate = _current_rate(loan, yr_in_loan) if month <= bank_term_mo else 0
        if month <= bank_term_mo:
            bank_bal, interest_paid = _update_balance(bank_bal, bp, ann_rate)
            yr_mortgage_interest += interest_paid
        else:
            interest_paid = 0

        # ── secondary loan (split interest) ──
        sp = 0.0
        sec_interest = 0.0
        if sec_enabled and sec_bal > 0:
            if sec_after:
                sec_mo = month - bank_term_mo
                sp = _sec_payment(sec, sec_bal, sec_mo, sec_term_mo)
                if sec_mo >= 1:
                    sec_rate_val = sec.get('interest_rate', 0) / 100
                    sec_bal, sec_interest = _update_balance(sec_bal, sp, sec_rate_val)
            else:
                sp = _sec_payment(sec, sec_bal, month, sec_term_mo)
                if month <= sec_term_mo:
                    sec_rate_val = sec.get('interest_rate', 0) / 100
                    sec_bal, sec_interest = _update_balance(sec_bal, sp, sec_rate_val)
        yr_sec_interest += sec_interest

        maint = cur_pv * costs.get('maintenance_pct', 1) / 100 / 12 + costs.get('maintenance_fixed', 0) / 12
        ins = cur_pv * costs.get('insurance_pct', 0.3) / 100 / 12 + costs.get('insurance_fixed', 0) / 12
        yr_maintenance += maint
        yr_insurance += ins

        # ── rental income ──
        rent_recv = rent * vac_factor
        agent_mo = (rent * 12 * agent_pct) / (contract_yrs * 12)
        yr_gross_rent += rent_recv
        yr_agent += agent_mo

        # ── bad tenant event ──
        bad_cash_cost = 0
        if bad_enabled and year == bad_year and mo_in_yr == 1:
            unpaid_months = ll.get('bad_tenant_unpaid_months', 6)
            eviction_cost = ll.get('bad_tenant_eviction_cost', 3000)
            repair_cost = ll.get('bad_tenant_repair_cost', 5000)
            bad_cash_cost = unpaid_months * rent + eviction_cost + repair_cost
            # For IRPF deductions:
            yr_bad_debt += unpaid_months * rent           # bad debt (separate deduction)
            yr_legal_costs += eviction_cost               # legal defense (separate deduction)
            yr_repair_from_tenant += repair_cost          # goes to maintenance (financing+repair cap)

        # Product costs (bank bonificaciones)
        prod_cost_pct = costs.get('product_cost_pct_loan', 0) / 100
        prod_cost_fixed = costs.get('product_cost_fixed', 0)
        prod_cost_mo = bank_bal * prod_cost_pct / 12 + prod_cost_fixed / 12
        # Actual monthly cashflow (what the landlord really pays/receives)
        net_mo = rent_recv - bp - sp - maint - ins - agent_mo - bad_cash_cost - prod_cost_mo
        yr_actual_cashflow += net_mo

        # ── yearly IRPF with Spanish deduction rules ──
        if mo_in_yr == 12:
            # 1) Financing + repair/conservation (CAPPED at gross rent, excess carried fwd 4yr)
            financing_repair = (yr_mortgage_interest + yr_sec_interest
                                + yr_maintenance + yr_repair_from_tenant)
            # Add carry-forward from previous years (drop expired > 4yr)
            carry_forward = [(amt, yr_created) for amt, yr_created in carry_forward
                             if year - yr_created <= 4]
            total_cf = sum(amt for amt, _ in carry_forward)
            available_fr = financing_repair + total_cf
            deductible_fr = min(available_fr, yr_gross_rent)
            excess = available_fr - deductible_fr
            # Update carry-forward: consume oldest first, add new excess
            remaining_to_consume = deductible_fr - financing_repair  # how much CF we used
            new_cf = []
            for amt, yr_created in carry_forward:
                if remaining_to_consume > 0:
                    consumed = min(amt, remaining_to_consume)
                    remaining_to_consume -= consumed
                    leftover = amt - consumed
                    if leftover > 0:
                        new_cf.append((leftover, yr_created))
                else:
                    new_cf.append((amt, yr_created))
            if excess > 0 and excess > total_cf:  # new excess from this year
                new_cf.append((excess - total_cf, year))
            elif excess > 0 and excess <= total_cf:  # all excess is old CF
                pass  # already in new_cf
            carry_forward = new_cf

            # 2) Other deductions (NO cap)
            other_deductions = (yr_insurance + yr_agent + annual_depreciation
                                + yr_legal_costs + yr_bad_debt)

            # 3) Taxable rental income
            taxable_rental = yr_gross_rent - deductible_fr - other_deductions
            r_irpf = _calc_irpf(max(0, taxable_rental), irpf_brackets)

            # 4) After-tax actual cashflow invested
            after_tax = yr_actual_cashflow - r_irpf
            portfolio += after_tax
            cum_inv += max(0, after_tax)

        # Compound portfolio (negative = opportunity cost)
        portfolio = portfolio * (1 + port_m)

        total_cost = bp + sp + maint + ins + prod_cost_mo
        monthly.append({
            'month': month, 'year': year,
            'property_value': cur_pv,
            'bank_payment': bp, 'secondary_payment': sp,
            'maintenance': maint, 'insurance': ins,
            'rent_paid': 0, 'rent_received': rent_recv,
            'total_housing_cost': total_cost,
            'surplus_invested': 0, 'portfolio': portfolio,
            'cumulative_invested': cum_inv,
            'bank_balance': bank_bal, 'sec_balance': sec_bal,
            'net_rental_income': net_mo,
        })

    return {
        'type': 'landlord', 'upfront': upfront,
        'property_value_initial': pv,
        'bank_loan': bank_loan_amt, 'sec_loan': sec_loan_amt,
        'monthly': monthly, 'final': {},
    }


# ════════════════════════════════════════════════════════════════════
#  SURPLUS EQUALIZATION  (non-landlord only)
# ════════════════════════════════════════════════════════════════════

def _equalize(results, cash_base, port_m, sim_years):
    """Build portfolios for owner/rent scenarios with monthly surplus investing."""
    non_ll = {n: d for n, d in results.items() if d['type'] != 'landlord'}
    if not non_ll:
        return

    total_months = sim_years * 12

    # Initial portfolio for each scenario
    portfolios = {}
    cum_invested = {}
    for name, data in non_ll.items():
        if data['type'] == 'owner':
            init = max(0, cash_base - data['upfront'])
        else:  # rent
            init = cash_base - data.get('deposit', 0)
        portfolios[name] = init
        cum_invested[name] = init

    for mi in range(total_months):
        # Collect costs
        costs = {}
        for name, data in non_ll.items():
            costs[name] = data['monthly'][mi]['total_housing_cost']
        mx = max(costs.values()) if costs else 0

        for name, data in non_ll.items():
            surplus = mx - costs[name]
            # Grow then add surplus
            portfolios[name] = portfolios[name] * (1 + port_m) + surplus
            cum_invested[name] += surplus

            md = data['monthly'][mi]
            md['surplus_invested'] = surplus
            md['portfolio'] = portfolios[name]
            md['cumulative_invested'] = cum_invested[name]


# ════════════════════════════════════════════════════════════════════
#  FINAL NET WORTH
# ════════════════════════════════════════════════════════════════════

def _final_net_worth(res, sc, brackets):
    md = res['monthly']
    if not md:
        return
    last = md[-1]

    if res['type'] == 'rent':
        pv = last['portfolio'] + last.get('deposit_held', 0)
        ci = last['cumulative_invested']
        pg = max(0, pv - ci)
        pt = _calc_irpf(pg, brackets)
        res['final'] = {
            'property_value': None, 'sell_fee': 0, 'plusvalia': 0,
            'remaining_bank': 0, 'remaining_sec': 0, 'net_from_sale': 0,
            'property_gain': 0, 'property_irpf': 0,
            'portfolio_value': pv, 'portfolio_gain': pg, 'portfolio_irpf': pt,
            'total_net_worth': pv - pt,
        }
        return

    # owner or landlord
    pv_init = res['property_value_initial']
    pv_final = last['property_value']
    costs = sc.get('costs', {})

    sell_fee = pv_final * costs.get('selling_fee_pct', 6) / 100
    appr_amt = max(0, pv_final - pv_init)
    if costs.get('plusvalia_mode') == 'Flat Amount':
        plusvalia = costs.get('plusvalia_flat', 0)
    else:
        plusvalia = appr_amt * costs.get('plusvalia_pct', 5) / 100

    rem_bank = last['bank_balance']
    rem_sec = last['sec_balance']
    net_sale = pv_final - sell_fee - plusvalia - rem_bank - rem_sec
    prop_gain = max(0, pv_final - pv_init)
    prop_irpf = _calc_irpf(prop_gain, brackets)

    port_val = last['portfolio']
    cum_inv = last['cumulative_invested']
    port_gain = max(0, port_val - cum_inv)
    port_irpf = _calc_irpf(port_gain, brackets)

    nw = (net_sale - prop_irpf) + (port_val - port_irpf)
    res['final'] = {
        'property_value': pv_final, 'sell_fee': sell_fee,
        'plusvalia': plusvalia,
        'remaining_bank': rem_bank, 'remaining_sec': rem_sec,
        'net_from_sale': net_sale,
        'property_gain': prop_gain, 'property_irpf': prop_irpf,
        'portfolio_value': port_val, 'portfolio_gain': port_gain,
        'portfolio_irpf': port_irpf, 'total_net_worth': nw,
    }


# ════════════════════════════════════════════════════════════════════
#  IRPF
# ════════════════════════════════════════════════════════════════════

def _calc_irpf(gain, brackets):
    if gain <= 0:
        return 0.0
    tax = 0.0
    remaining = gain
    prev = 0
    for b in brackets:
        lim = b['limit']
        rate = b['rate'] / 100
        width = lim - prev
        t = min(remaining, width)
        tax += t * rate
        remaining -= t
        prev = lim
        if remaining <= 0:
            break
    if remaining > 0:
        tax += remaining * (brackets[-1]['rate'] / 100)
    return tax
