# i18n.py
# Internationalization module for Mortgage Calculator Streamlit App
# Supports English ('en') and Spanish ('es')

TRANSLATIONS = {
    'en': {
        # ============================================================
        # APP CHROME
        # ============================================================
        'app_title': '🏠 Property vs Portfolio Simulator',
        'app_desc': 'Simulate and compare housing strategies — buying, renting & investing, or becoming a landlord. See where your money grows more over time with detailed financial projections.',
        'lang_label': 'Language',
        'disclaimer': '⚠️ Disclaimer: This tool is for educational and informational purposes only. It does not constitute financial, tax, or investment advice. Results are based on simplified models and assumptions that may not reflect actual market conditions, tax regulations, or individual circumstances. Always consult a qualified financial advisor, tax professional, or mortgage broker before making real estate or investment decisions. The authors assume no liability for financial decisions made based on this tool\'s output.',

        # ============================================================
        # SIDEBAR - GLOBAL PARAMETERS
        # ============================================================
        'sidebar_header': '⚙️ Global Parameters',
        'monthly_income': 'Monthly Net Income (EUR)',
        'monthly_income_help': 'Your net monthly income after taxes, used to calculate debt-to-income ratio and affordability.',
        'bank_dti': 'Bank DTI Limit (%)',
        'bank_dti_help': 'Maximum percentage of monthly income that can be allocated to debt payments. Typical range: 30-40%.',
        'inflation': 'Expected Inflation / ITP (%)',
        'inflation_help': 'Annual inflation rate used for indexing costs and property appreciation baseline.',
        'portfolio_return': 'Portfolio Annual Return (%)',
        'portfolio_return_help': 'Expected annual return on invested surplus funds (stocks, bonds, index funds, etc.).',
        'sim_years': 'Simulation Duration (years)',

        'irpf_header': '📊 IRPF Capital Gains Brackets',
        'irpf_caption': 'Spanish progressive capital gains tax brackets applied when selling property or liquidating portfolio.',
        'irpf_col_limit': 'Upper Limit (EUR)',
        'irpf_col_rate': 'Rate (%)',

        'run_btn': '▶️ Run Simulation',
        'run_no_scenarios': 'Please add at least one scenario',
        'run_success': '✅ Simulation completed!',
        'run_error': 'Simulation error',
        'running': 'Running simulation…',

        # ============================================================
        # SIDEBAR - ADD SCENARIO
        # ============================================================
        'add_scenario': '➕ Add New Scenario',
        'scenario_type': 'Scenario Type',
        'scenario_name': 'Scenario Name',
        'add_btn': 'Add',

        # ============================================================
        # SCENARIO TYPE NAMES
        # ============================================================
        'type_owner': 'Owner-Occupier',
        'type_rent': 'Rent + Invest',
        'type_landlord': 'Buy-to-Rent (Landlord)',

        # ============================================================
        # SCENARIO TABS
        # ============================================================
        'config_header': '📋 Scenario Configuration',
        'no_scenarios': '👈 Add a scenario from the sidebar to get started',
        'scenario_name_label': 'Scenario Name',
        'delete_btn': '🗑️ Delete',
        'type_label': 'Type',

        # ============================================================
        # OWNER CONFIG - PROPERTY
        # ============================================================
        'property_header': '🏠 Property',
        'prop_mode': 'Property Value Mode',
        'prop_mode_max': 'Max Affordable',
        'prop_mode_fixed': 'Fixed Value',
        'prop_value': 'Property Value (EUR)',
        'yearly_appr': 'Yearly Appreciation (%)',

        # ============================================================
        # OWNER CONFIG - BANK LOAN
        # ============================================================
        'loan_header': '🏦 Bank Loan',
        'ltv': 'LTV (%)',
        'ltv_help': '% of property value financed by bank',
        'rate_type': 'Rate Type',
        'rate_fixed': 'Fixed',
        'rate_variable': 'Variable',
        'rate_mixed': 'Mixed',
        'fixed_rate': 'Fixed Rate (%)',
        'mortgage_term': 'Mortgage Term (years)',
        'amort_type': 'Amortization',
        'amort_french': 'French',
        'amort_linear': 'Linear',

        # ============================================================
        # OWNER CONFIG - VARIABLE/MIXED RATE
        # ============================================================
        'var_config': 'Variable Rate Configuration',
        'base_rate_spread': 'Spread over Base Rate (%)',
        'base_rate_spread_help': 'Additional percentage added on top of the base reference rate (e.g., Euribor in EU, Fed Funds Rate in US, SONIA in UK)',
        'default_base_rate': 'Default Base Rate (%)',
        'default_base_rate_help': 'Base reference rate when no prediction is available for a given year',
        'base_rate_predictions': '📈 Base Rate Predictions by Year',
        'base_rate_col_year': 'Year',
        'base_rate_col_rate': 'Base Rate (%)',
        'fixed_period': 'Fixed Period (years)',
        'var_position': 'Variable Period Position',
        'var_at_end': 'Variable at End',
        'var_at_beginning': 'Variable at Beginning',

        # ============================================================
        # OWNER CONFIG - SECONDARY LOAN
        # ============================================================
        'secondary_loan_header': '🤝 Secondary Loan (Family / Private / Government)',
        'secondary_loan_enable': 'Enable Secondary Loan',
        'secondary_loan_pct': 'Amount (% of property)',
        'secondary_loan_rate': 'Interest Rate (%)',
        'secondary_loan_term': 'Term (years)',
        'secondary_loan_dti': 'Constrained by DTI',
        'secondary_loan_dti_help': 'If ON, bank considers this loan in your DTI calculation',
        'secondary_loan_timing': 'Repayment Timing',
        'secondary_loan_after': 'After Primary Loan',
        'secondary_loan_concurrent': 'Concurrent with Primary',

        'bank_products_header': '🏦 Bank Products & Bonificaciones',
        'bank_products_caption': 'Banks offer interest rate discounts when you hire their products. Enable products to reduce your mortgage rate. The cost of each product is added to your monthly expenses.',

        # ============================================================
        # OWNER CONFIG - COSTS
        # ============================================================
        'costs_header': '💰 Costs',
        'transfer_tax': 'Transfer Tax (%)',
        'registration_fee': 'Registration / Notary (EUR)',
        'maintenance_pct': 'Maintenance (% of property/yr)',
        'maintenance_fixed': 'Fixed Maintenance (EUR/yr)',
        'insurance_pct': 'Insurance (% of property/yr)',

        'selling_costs_header': '🏷️ Selling Costs',
        'selling_commission': 'Selling Commission (%)',
        'plusvalia_mode': 'Plusvalía Mode',
        'plusvalia_flat_mode': 'Flat Amount',
        'plusvalia_pct_mode': '% of Appreciation',
        'plusvalia_flat': 'Plusvalía Flat (EUR)',
        'plusvalia_pct': 'Plusvalía (% of appreciation)',

        # ============================================================
        # RENT CONFIG
        # ============================================================
        'rent_header': '🏘️ Rent',
        'rent_mode': 'Rent Mode',
        'rent_mode_pct': '% of Property Value',
        'rent_mode_fixed': 'Fixed Amount',
        'ref_prop_value': 'Reference Property Value (EUR)',
        'ref_prop_value_help': "Set to 0 to auto-use first owner scenario's property value",
        'ref_appreciation': 'Reference Appreciation (%)',
        'rent_yield': 'Rent Yield (% of value/yr)',
        'rent_yield_help': 'Annual rent as percentage of property value',
        'calc_monthly_rent': 'Calculated Monthly Rent',
        'auto_rent_info': 'Monthly rent will be auto-calculated from first owner scenario.',
        'monthly_rent': 'Monthly Rent (EUR)',

        'contract_regime': '⚙️ Advanced Rent Config — Contract Regime',
        'contract_regime_caption': 'At each contract renewal, rent resets to current market value. Within a contract, rent increases yearly by the selected method.',
        'contract_length': 'Contract Length (years)',
        'in_contract_increase': 'In-Contract Yearly Increase',
        'increase_itp': 'Inflation (ITP)',
        'increase_custom': 'Custom %',
        'increase_market': 'Market Value',
        'custom_increase': 'Custom Increase (%)',
        'deposit_months': 'Deposit (months of rent)',
        'deposit_months_help': 'Number of months rent held as deposit. Locked and not invested. Returned at end of simulation.',

        # ============================================================
        # LANDLORD CONFIG
        # ============================================================
        'rental_income_header': '💵 Rental Income',
        'landlord_expenses': '🏢 Landlord Expenses',
        'vacancy_months': 'Vacancy (months/year)',
        'agent_commission': 'Agent Commission (% of annual rent)',

        'bad_tenant_header': '⚠️ Bad Tenant Scenario',
        'bad_tenant_enable': 'Enable Bad Tenant Scenario',
        'bad_tenant_months': 'Months Unpaid',
        'bad_tenant_year': 'Occurs at Year',
        'bad_tenant_eviction': 'Eviction Cost (EUR)',
        'bad_tenant_repair': 'Repair Cost (EUR)',

        # ============================================================
        # RESULTS
        # ============================================================
        'results_header': '📊 Results',
        'summary_header': '📈 Summary Comparison',
        'col_scenario': 'Scenario',
        'col_type': 'Type',
        'col_initial_prop': 'Initial Property',
        'col_bank_loan': 'Bank Loan',
        'col_upfront': 'Upfront',
        'col_final_prop': 'Final Property',
        'col_net_sale': 'Net from Sale',
        'col_portfolio': 'Portfolio',
        'col_total_irpf': 'Total IRPF',
        'col_net_worth': 'Net Worth',

        'winner_label': '🏆 Winner',
        'advantage_label': 'Advantage over 2nd',
        'cash_base_label': 'Cash Base',

        'yearly_header': '📅 Year-by-Year Comparison',
        'col_year': 'Year',
        'cost_per_mo': 'Cost/mo',
        'portfolio_label': 'Portfolio',
        'net_worth_est': 'Net Worth (est)',

        'charts_header': '📊 Visualisations',
        'chart_nw': 'Estimated Net Worth Over Time',
        'chart_portfolio': 'Portfolio Value Over Time',
        'chart_breakdown': 'Final Net Worth Breakdown',
        'chart_cost': 'Monthly Housing Cost Over Time',
        'prop_after_tax': 'Property (after tax)',
        'port_after_tax': 'Portfolio (after tax)',

        'monthly_detail_header': '🔍 Month-by-Month Detail',
        'download_csv': '📥 Download CSV',
        'no_monthly_data': 'No monthly data.',
        'no_results': 'No scenario results to display.',

        # ============================================================
        # GUIDE / GLOSSARY
        # ============================================================
        'guide_header': '📖 Financial Glossary & Guide',
        'guide_intro': 'This reference explains all financial metrics, terms, and calculation methods used in the mortgage calculator to help you understand your results.',

        'guide_dti_title': 'DTI (Debt-to-Income Ratio)',
        'guide_dti': 'DTI measures the percentage of your monthly income dedicated to debt payments. Lenders use this to assess affordability and lending risk. For example, with a 35% DTI limit and €3,000 monthly income, your maximum monthly debt payment is €1,050. Most banks require DTI below 30-40%.',

        'guide_ltv_title': 'LTV (Loan-to-Value)',
        'guide_ltv': 'LTV is the percentage of the property value that the bank will finance. For example, an 80% LTV on a €300,000 property means the bank lends €240,000, and you provide a €60,000 down payment (20%). Higher LTV means less upfront cash but typically higher interest rates.',

        'guide_french_title': 'French Amortization',
        'guide_french': 'French amortization features constant monthly payments throughout the mortgage term. Each payment contains both principal and interest, but the proportion changes over time: early payments are mostly interest, while later payments are mostly principal. This is the most common mortgage type in Europe.',

        'guide_linear_title': 'Linear Amortization',
        'guide_linear': 'Linear amortization pays a constant amount of principal each month, plus decreasing interest on the remaining balance. Monthly payments start higher but decrease over time. You pay less total interest compared to French amortization, but need higher initial affordability.',

        'guide_base_rate_title': 'Base Reference Rate',
        'guide_base_rate': 'The base reference rate is the interbank lending benchmark rate (Euribor in EU, Fed Funds Rate in US, SONIA in UK, etc.). Variable mortgages charge this rate plus a spread. For example, if Euribor is 3.5% and your spread is 0.8%, your mortgage rate is 4.3%. The calculator lets you predict future base rates for accurate projections.',

        'guide_irpf_title': 'IRPF / Capital Gains Tax',
        'guide_irpf': 'IRPF (Impuesto sobre la Renta de las Personas Físicas) is the Spanish progressive capital gains tax applied to profits from property sales and investment portfolio liquidation. Tax brackets are typically 19% (up to €6,000), 21% (€6,000-€50,000), 23% (€50,000-€200,000), and 26% (above €200,000). The calculator applies these brackets to calculate net proceeds.',

        'guide_plusvalia_title': 'Plusvalía',
        'guide_plusvalia': 'Plusvalía municipal (formally Impuesto sobre el Incremento de Valor de los Terrenos de Naturaleza Urbana) is a Spanish municipal tax on the increase in urban land value when selling property. It can be calculated as a flat amount or percentage of appreciation, varying by municipality. This is separate from capital gains tax.',

        'guide_transfer_tax_title': 'Transfer Tax (ITP)',
        'guide_transfer_tax': 'ITP (Impuesto de Transmisiones Patrimoniales) is the transfer tax paid when buying a resale property in Spain, typically 6-10% depending on the region. For new properties, you pay IVA (VAT) instead, usually 10%. This is a significant upfront cost when purchasing.',

        'guide_rent_yield_title': 'Rent Yield',
        'guide_rent_yield': 'Rent yield is the annual rental income expressed as a percentage of property value. For example, a property worth €300,000 renting for €1,200/month generates €14,400/year, which is a 4.8% yield. Typical yields range from 3-6% depending on location and property type.',

        'guide_surplus_title': 'Surplus Equalization',
        'guide_surplus': 'To fairly compare scenarios with different monthly costs, the calculator invests any monthly surplus (the difference between your DTI limit and actual housing cost) into your investment portfolio. This ensures scenarios are compared on equal financial footing, as lower monthly costs allow more investment.',

        'guide_net_worth_title': 'Net Worth',
        'guide_net_worth': 'Final net worth is calculated as: (property equity after selling costs and capital gains tax) + (investment portfolio value after capital gains tax). This represents your total liquid wealth at the end of the simulation period, allowing direct comparison between ownership, renting, and landlord strategies.',

        'guide_portfolio_title': 'Investment Portfolio',
        'guide_portfolio': 'The investment portfolio represents surplus funds invested monthly in stocks, bonds, index funds, or other assets. It grows according to your specified annual return rate. For rent scenarios, the down payment that would have been used to buy is also invested. Portfolio gains are taxed at IRPF rates when liquidated.',

        'guide_vacancy_title': 'Vacancy Rate',
        'guide_vacancy': 'Vacancy represents the expected number of months per year when a rental property has no tenant and generates no income. Typical vacancy rates are 0.5-2 months per year. During vacancy, you still pay mortgage, maintenance, and other costs without rental income to offset them.',

        'guide_contract_title': 'Rent Contract Regime',
        'guide_contract': 'The contract regime determines how rent evolves. At each contract renewal (e.g., every 3 or 5 years), rent resets to current market value based on appreciation. During a contract, rent increases yearly by inflation, a custom percentage, or market value, depending on your setting. This models real-world rental dynamics accurately.',

        'guide_amortization_title': 'Amortization',
        'guide_amortization': 'Amortization is how a mortgage is repaid over time. The two main types are French (constant total payment) and Linear (constant principal payment). The type of amortization affects your monthly payment amount and total interest paid over the life of the loan.',

        'guide_fixed_rate_title': 'Fixed Rate Mortgage',
        'guide_fixed_rate': 'A fixed rate mortgage has the same interest rate for the entire loan term. Your monthly payment never changes, making budgeting predictable. However, fixed rates are typically higher than initial variable rates since the bank assumes the risk of future rate changes.',

        'guide_variable_rate_title': 'Variable Rate Mortgage',
        'guide_variable_rate': 'A variable rate mortgage has an interest rate that changes periodically based on a base reference rate (e.g., Euribor) plus a fixed spread. Monthly payments can go up or down. Lower initial rates but carries the risk of future rate increases.',

        'guide_mixed_rate_title': 'Mixed Rate Mortgage',
        'guide_mixed_rate': 'A mixed rate mortgage combines fixed and variable periods. Typically, you pay a fixed rate for an initial period (e.g., 5-10 years) and then switch to a variable rate for the remaining term, or vice versa. This balances payment predictability with potential savings.',

        'guide_bad_tenant_title': 'Bad Tenant Scenario',
        'guide_bad_tenant': 'The bad tenant scenario models a worst-case event where a tenant stops paying rent. It includes months of unpaid rent, legal eviction costs, and property repair/damage costs. This is a common risk for landlords, especially in jurisdictions with strong tenant protections where eviction can take 6-12+ months.',
    },

    'es': {
        # ============================================================
        # APP CHROME
        # ============================================================
        'app_title': '🏠 Simulador Propiedad vs Cartera',
        'app_desc': 'Simula y compara estrategias de vivienda — comprar, alquilar e invertir, o ser casero. Descubre dónde crece más tu dinero con proyecciones financieras detalladas.',
        'lang_label': 'Idioma',
        'disclaimer': '⚠️ Aviso legal: Esta herramienta es solo para fines educativos e informativos. No constituye asesoramiento financiero, fiscal ni de inversión. Los resultados se basan en modelos y supuestos simplificados que pueden no reflejar las condiciones reales del mercado, la normativa fiscal o las circunstancias individuales. Consulte siempre a un asesor financiero cualificado, un profesional fiscal o un intermediario hipotecario antes de tomar decisiones inmobiliarias o de inversión. Los autores no asumen responsabilidad por decisiones financieras basadas en los resultados de esta herramienta.',

        # ============================================================
        # SIDEBAR - GLOBAL PARAMETERS
        # ============================================================
        'sidebar_header': '⚙️ Parámetros Globales',
        'monthly_income': 'Ingresos Netos Mensuales (EUR)',
        'monthly_income_help': 'Tus ingresos mensuales netos después de impuestos, usados para calcular el ratio de endeudamiento y la capacidad de pago.',
        'bank_dti': 'Límite DTI del Banco (%)',
        'bank_dti_help': 'Porcentaje máximo de ingresos mensuales que se puede destinar al pago de deudas. Rango típico: 30-40%.',
        'inflation': 'Inflación Esperada / ITP (%)',
        'inflation_help': 'Tasa de inflación anual utilizada para indexar costes y revalorización base de la propiedad.',
        'portfolio_return': 'Rentabilidad Anual de Cartera (%)',
        'portfolio_return_help': 'Rentabilidad anual esperada de los fondos excedentes invertidos (acciones, bonos, fondos indexados, etc.).',
        'sim_years': 'Duración de Simulación (años)',

        'irpf_header': '📊 Tramos IRPF Ganancias Patrimoniales',
        'irpf_caption': 'Tramos progresivos de IRPF aplicados al vender una propiedad o liquidar la cartera de inversión.',
        'irpf_col_limit': 'Límite Superior (EUR)',
        'irpf_col_rate': 'Tipo (%)',

        'run_btn': '▶️ Ejecutar Simulación',
        'run_no_scenarios': 'Por favor, añade al menos un escenario',
        'run_success': '✅ ¡Simulación completada!',
        'run_error': 'Error en la simulación',
        'running': 'Ejecutando simulación…',

        # ============================================================
        # SIDEBAR - ADD SCENARIO
        # ============================================================
        'add_scenario': '➕ Añadir Nuevo Escenario',
        'scenario_type': 'Tipo de Escenario',
        'scenario_name': 'Nombre del Escenario',
        'add_btn': 'Añadir',

        # ============================================================
        # SCENARIO TYPE NAMES
        # ============================================================
        'type_owner': 'Propietario-Residente',
        'type_rent': 'Alquiler + Inversión',
        'type_landlord': 'Comprar para Alquilar (Casero)',

        # ============================================================
        # SCENARIO TABS
        # ============================================================
        'config_header': '📋 Configuración de Escenarios',
        'no_scenarios': '👈 Añade un escenario desde la barra lateral para empezar',
        'scenario_name_label': 'Nombre del Escenario',
        'delete_btn': '🗑️ Eliminar',
        'type_label': 'Tipo',

        # ============================================================
        # OWNER CONFIG - PROPERTY
        # ============================================================
        'property_header': '🏠 Propiedad',
        'prop_mode': 'Modo de Valor de Propiedad',
        'prop_mode_max': 'Máximo Asequible',
        'prop_mode_fixed': 'Valor Fijo',
        'prop_value': 'Valor de Propiedad (EUR)',
        'yearly_appr': 'Revalorización Anual (%)',

        # ============================================================
        # OWNER CONFIG - BANK LOAN
        # ============================================================
        'loan_header': '🏦 Préstamo Bancario',
        'ltv': 'LTV (%)',
        'ltv_help': '% del valor de la propiedad financiado por el banco',
        'rate_type': 'Tipo de Interés',
        'rate_fixed': 'Fijo',
        'rate_variable': 'Variable',
        'rate_mixed': 'Mixto',
        'fixed_rate': 'Tipo Fijo (%)',
        'mortgage_term': 'Plazo de Hipoteca (años)',
        'amort_type': 'Amortización',
        'amort_french': 'Francesa',
        'amort_linear': 'Lineal',

        # ============================================================
        # OWNER CONFIG - VARIABLE/MIXED RATE
        # ============================================================
        'var_config': 'Configuración de Tipo Variable',
        'base_rate_spread': 'Diferencial sobre Tipo Base (%)',
        'base_rate_spread_help': 'Porcentaje adicional sobre el tipo de referencia base (por ejemplo, Euríbor en UE, Fed Funds Rate en EE.UU., SONIA en Reino Unido)',
        'default_base_rate': 'Tipo Base por Defecto (%)',
        'default_base_rate_help': 'Tipo de referencia base cuando no hay predicción disponible para un año dado',
        'base_rate_predictions': '📈 Predicciones de Tipo Base por Año',
        'base_rate_col_year': 'Año',
        'base_rate_col_rate': 'Tipo Base (%)',
        'fixed_period': 'Período Fijo (años)',
        'var_position': 'Posición del Período Variable',
        'var_at_end': 'Variable al Final',
        'var_at_beginning': 'Variable al Principio',

        # ============================================================
        # OWNER CONFIG - SECONDARY LOAN
        # ============================================================
        'secondary_loan_header': '🤝 Préstamo Secundario (Familiar / Privado / Público)',
        'secondary_loan_enable': 'Activar Préstamo Secundario',
        'secondary_loan_pct': 'Importe (% de la propiedad)',
        'secondary_loan_rate': 'Tipo de Interés (%)',
        'secondary_loan_term': 'Plazo (años)',
        'secondary_loan_dti': 'Limitado por DTI',
        'secondary_loan_dti_help': 'Si está ACTIVADO, el banco considera este préstamo en el cálculo de tu DTI',
        'secondary_loan_timing': 'Calendario de Amortización',
        'secondary_loan_after': 'Después del Préstamo Principal',
        'secondary_loan_concurrent': 'Simultáneo con Principal',

        'bank_products_header': '🏦 Productos Bancarios y Bonificaciones',
        'bank_products_caption': 'Los bancos ofrecen descuentos en el tipo de interés cuando contratas sus productos. Activa productos para reducir tu tipo hipotecario. El coste de cada producto se añade a tus gastos mensuales.',

        # ============================================================
        # OWNER CONFIG - COSTS
        # ============================================================
        'costs_header': '💰 Costes',
        'transfer_tax': 'ITP (%)',
        'registration_fee': 'Registro / Notaría (EUR)',
        'maintenance_pct': 'Mantenimiento (% propiedad/año)',
        'maintenance_fixed': 'Mantenimiento Fijo (EUR/año)',
        'insurance_pct': 'Seguro (% propiedad/año)',

        'selling_costs_header': '🏷️ Costes de Venta',
        'selling_commission': 'Comisión de Venta (%)',
        'plusvalia_mode': 'Modo de Plusvalía',
        'plusvalia_flat_mode': 'Importe Fijo',
        'plusvalia_pct_mode': '% de la Revalorización',
        'plusvalia_flat': 'Plusvalía Fija (EUR)',
        'plusvalia_pct': 'Plusvalía (% de revalorización)',

        # ============================================================
        # RENT CONFIG
        # ============================================================
        'rent_header': '🏘️ Alquiler',
        'rent_mode': 'Modo de Alquiler',
        'rent_mode_pct': '% del Valor de Propiedad',
        'rent_mode_fixed': 'Importe Fijo',
        'ref_prop_value': 'Valor de Propiedad de Referencia (EUR)',
        'ref_prop_value_help': 'Pon 0 para usar automáticamente el valor de la propiedad del primer escenario de propietario',
        'ref_appreciation': 'Revalorización de Referencia (%)',
        'rent_yield': 'Rentabilidad de Alquiler (% valor/año)',
        'rent_yield_help': 'Alquiler anual como porcentaje del valor de la propiedad',
        'calc_monthly_rent': 'Alquiler Mensual Calculado',
        'auto_rent_info': 'El alquiler mensual se calculará automáticamente desde el primer escenario de propietario.',
        'monthly_rent': 'Alquiler Mensual (EUR)',

        'contract_regime': '⚙️ Config. Avanzada Alquiler — Régimen de Contrato',
        'contract_regime_caption': 'En cada renovación de contrato, el alquiler se ajusta al valor de mercado actual. Dentro de un contrato, el alquiler aumenta anualmente según el método seleccionado.',
        'contract_length': 'Duración de Contrato (años)',
        'in_contract_increase': 'Aumento Anual Intra-Contrato',
        'increase_itp': 'Inflación (ITP)',
        'increase_custom': '% Personalizado',
        'increase_market': 'Valor de Mercado',
        'custom_increase': 'Aumento Personalizado (%)',
        'deposit_months': 'Depósito (meses de alquiler)',
        'deposit_months_help': 'Número de meses de alquiler retenidos como fianza. No se invierte. Se devuelve al final de la simulación.',

        # ============================================================
        # LANDLORD CONFIG
        # ============================================================
        'rental_income_header': '💵 Ingresos por Alquiler',
        'landlord_expenses': '🏢 Gastos del Casero',
        'vacancy_months': 'Vacante (meses/año)',
        'agent_commission': 'Comisión de Agencia (% alquiler anual)',

        'bad_tenant_header': '⚠️ Escenario de Inquilino Moroso',
        'bad_tenant_enable': 'Activar Escenario de Inquilino Moroso',
        'bad_tenant_months': 'Meses Impagados',
        'bad_tenant_year': 'Ocurre en el Año',
        'bad_tenant_eviction': 'Coste de Desahucio (EUR)',
        'bad_tenant_repair': 'Coste de Reparación (EUR)',

        # ============================================================
        # RESULTS
        # ============================================================
        'results_header': '📊 Resultados',
        'summary_header': '📈 Comparativa Resumen',
        'col_scenario': 'Escenario',
        'col_type': 'Tipo',
        'col_initial_prop': 'Propiedad Inicial',
        'col_bank_loan': 'Préstamo Bancario',
        'col_upfront': 'Desembolso Inicial',
        'col_final_prop': 'Propiedad Final',
        'col_net_sale': 'Neto de Venta',
        'col_portfolio': 'Cartera',
        'col_total_irpf': 'IRPF Total',
        'col_net_worth': 'Patrimonio Neto',

        'winner_label': '🏆 Ganador',
        'advantage_label': 'Ventaja sobre el 2º',
        'cash_base_label': 'Base Líquida',

        'yearly_header': '📅 Comparativa Año a Año',
        'col_year': 'Año',
        'cost_per_mo': 'Coste/mes',
        'portfolio_label': 'Cartera',
        'net_worth_est': 'Patrimonio (est)',

        'charts_header': '📊 Visualizaciones',
        'chart_nw': 'Patrimonio Neto Estimado a lo Largo del Tiempo',
        'chart_portfolio': 'Valor de la Cartera a lo Largo del Tiempo',
        'chart_breakdown': 'Desglose del Patrimonio Neto Final',
        'chart_cost': 'Coste Mensual de Vivienda a lo Largo del Tiempo',
        'prop_after_tax': 'Propiedad (tras impuestos)',
        'port_after_tax': 'Cartera (tras impuestos)',

        'monthly_detail_header': '🔍 Detalle Mes a Mes',
        'download_csv': '📥 Descargar CSV',
        'no_monthly_data': 'Sin datos mensuales.',
        'no_results': 'No hay resultados de escenarios para mostrar.',

        # ============================================================
        # GUIDE / GLOSSARY
        # ============================================================
        'guide_header': '📖 Glosario Financiero y Guía',
        'guide_intro': 'Esta referencia explica todas las métricas financieras, términos y métodos de cálculo utilizados en la calculadora de hipotecas para ayudarte a entender tus resultados.',

        'guide_dti_title': 'DTI (Ratio de Endeudamiento)',
        'guide_dti': 'El DTI mide el porcentaje de tus ingresos mensuales dedicado al pago de deudas. Los bancos lo utilizan para evaluar la capacidad de pago y el riesgo crediticio. Por ejemplo, con un límite DTI del 35% e ingresos de 3.000€ al mes, tu pago mensual máximo de deuda es 1.050€. La mayoría de bancos exigen un DTI inferior al 30-40%.',

        'guide_ltv_title': 'LTV (Loan-to-Value)',
        'guide_ltv': 'El LTV es el porcentaje del valor de la propiedad que el banco financiará. Por ejemplo, un LTV del 80% sobre una propiedad de 300.000€ significa que el banco presta 240.000€ y tú aportas 60.000€ de entrada (20%). Un LTV mayor significa menos efectivo inicial pero normalmente tipos de interés más altos.',

        'guide_french_title': 'Amortización Francesa',
        'guide_french': 'La amortización francesa se caracteriza por cuotas mensuales constantes durante todo el plazo de la hipoteca. Cada cuota contiene capital e intereses, pero la proporción cambia con el tiempo: las primeras cuotas son mayormente intereses, mientras que las últimas son mayormente capital. Es el tipo de hipoteca más común en Europa.',

        'guide_linear_title': 'Amortización Lineal',
        'guide_linear': 'La amortización lineal paga una cantidad constante de capital cada mes, más intereses decrecientes sobre el saldo restante. Las cuotas mensuales empiezan más altas pero disminuyen con el tiempo. Pagas menos intereses totales comparado con la francesa, pero necesitas mayor capacidad de pago inicial.',

        'guide_base_rate_title': 'Tipo de Referencia Base',
        'guide_base_rate': 'El tipo de referencia base es el índice de préstamos interbancarios (Euríbor en UE, Fed Funds Rate en EE.UU., SONIA en Reino Unido, etc.). Las hipotecas variables cobran este tipo más un diferencial. Por ejemplo, si el Euríbor está al 3,5% y tu diferencial es 0,8%, tu tipo hipotecario es 4,3%. La calculadora te permite predecir tipos base futuros para proyecciones precisas.',

        'guide_irpf_title': 'IRPF / Impuesto Ganancias Patrimoniales',
        'guide_irpf': 'El IRPF (Impuesto sobre la Renta de las Personas Físicas) es el impuesto progresivo español sobre ganancias patrimoniales aplicado a beneficios de ventas de propiedades y liquidación de cartera de inversión. Los tramos típicos son 19% (hasta 6.000€), 21% (6.000€-50.000€), 23% (50.000€-200.000€) y 26% (más de 200.000€). La calculadora aplica estos tramos para calcular el beneficio neto.',

        'guide_plusvalia_title': 'Plusvalía',
        'guide_plusvalia': 'La plusvalía municipal (formalmente Impuesto sobre el Incremento de Valor de los Terrenos de Naturaleza Urbana) es un impuesto municipal español sobre el incremento de valor del suelo urbano al vender una propiedad. Puede calcularse como importe fijo o porcentaje de la revalorización, variando según el municipio. Es independiente del IRPF sobre ganancias patrimoniales.',

        'guide_transfer_tax_title': 'ITP (Impuesto Transmisiones Patrimoniales)',
        'guide_transfer_tax': 'El ITP es el impuesto que se paga al comprar una vivienda de segunda mano en España, típicamente 6-10% según la comunidad autónoma. Para viviendas nuevas, se paga IVA en su lugar, normalmente un 10%. Es un coste inicial significativo en la compra.',

        'guide_rent_yield_title': 'Rentabilidad de Alquiler',
        'guide_rent_yield': 'La rentabilidad de alquiler es el ingreso anual por alquiler expresado como porcentaje del valor de la propiedad. Por ejemplo, una propiedad de 300.000€ que se alquila por 1.200€/mes genera 14.400€/año, lo que es una rentabilidad del 4,8%. Las rentabilidades típicas oscilan entre 3-6% según ubicación y tipo de propiedad.',

        'guide_surplus_title': 'Equalización de Excedente',
        'guide_surplus': 'Para comparar escenarios con distintos costes mensuales de forma justa, la calculadora invierte cualquier excedente mensual (la diferencia entre tu límite DTI y el coste real de vivienda) en tu cartera de inversión. Esto asegura que los escenarios se comparen en igualdad de condiciones financieras, ya que costes mensuales más bajos permiten más inversión.',

        'guide_net_worth_title': 'Patrimonio Neto',
        'guide_net_worth': 'El patrimonio neto final se calcula como: (plusvalía de la propiedad tras costes de venta e IRPF) + (valor de cartera de inversión tras IRPF). Representa tu riqueza líquida total al final del período de simulación, permitiendo comparar directamente entre estrategias de propiedad, alquiler y casero.',

        'guide_portfolio_title': 'Cartera de Inversión',
        'guide_portfolio': 'La cartera de inversión representa los fondos excedentes invertidos mensualmente en acciones, bonos, fondos indexados u otros activos. Crece según el tipo de rentabilidad anual que especifiques. En escenarios de alquiler, la entrada que se habría usado para comprar también se invierte. Las ganancias de la cartera tributan al IRPF al liquidarse.',

        'guide_vacancy_title': 'Tasa de Vacante',
        'guide_vacancy': 'La vacante representa el número esperado de meses al año en que una propiedad de alquiler no tiene inquilino y no genera ingresos. Las tasas de vacante típicas son 0,5-2 meses al año. Durante la vacante, sigues pagando hipoteca, mantenimiento y otros costes sin ingresos por alquiler que los compensen.',

        'guide_contract_title': 'Régimen de Contrato de Alquiler',
        'guide_contract': 'El régimen de contrato determina cómo evoluciona el alquiler. En cada renovación de contrato (por ejemplo, cada 3 o 5 años), el alquiler se ajusta al valor de mercado actual basándose en la revalorización. Durante un contrato, el alquiler aumenta anualmente por inflación, un porcentaje personalizado o valor de mercado, según tu configuración. Esto modela con precisión la dinámica real de alquileres.',

        'guide_amortization_title': 'Amortización',
        'guide_amortization': 'La amortización es cómo se devuelve una hipoteca a lo largo del tiempo. Los dos tipos principales son Francesa (cuota total constante) y Lineal (amortización de capital constante). El tipo de amortización afecta tu cuota mensual y el total de intereses pagados durante la vida del préstamo.',

        'guide_fixed_rate_title': 'Hipoteca a Tipo Fijo',
        'guide_fixed_rate': 'Una hipoteca a tipo fijo tiene el mismo tipo de interés durante todo el plazo del préstamo. Tu cuota mensual nunca cambia, lo que hace el presupuesto predecible. Sin embargo, los tipos fijos suelen ser más altos que los variables iniciales ya que el banco asume el riesgo de cambios futuros en los tipos.',

        'guide_variable_rate_title': 'Hipoteca a Tipo Variable',
        'guide_variable_rate': 'Una hipoteca a tipo variable tiene un tipo de interés que cambia periódicamente basado en un tipo de referencia base (por ejemplo, Euríbor) más un diferencial fijo. Las cuotas mensuales pueden subir o bajar. Tipos iniciales más bajos pero con el riesgo de subidas futuras.',

        'guide_mixed_rate_title': 'Hipoteca a Tipo Mixto',
        'guide_mixed_rate': 'Una hipoteca a tipo mixto combina períodos fijos y variables. Normalmente, pagas un tipo fijo durante un período inicial (por ejemplo, 5-10 años) y luego cambias a tipo variable por el plazo restante, o viceversa. Esto equilibra la previsibilidad de las cuotas con el ahorro potencial.',

        'guide_bad_tenant_title': 'Escenario de Inquilino Moroso',
        'guide_bad_tenant': 'El escenario de inquilino moroso modela un evento adverso donde un inquilino deja de pagar el alquiler. Incluye meses de impago, costes legales de desahucio y costes de reparación/daños a la propiedad. Es un riesgo común para propietarios, especialmente en jurisdicciones con fuertes protecciones al inquilino donde el desahucio puede tardar 6-12+ meses.',
    }
}

# Current language setting
_current_lang = 'en'


def set_lang(lang: str) -> None:
    """
    Set the current language for translations.

    Args:
        lang: Language code ('en' or 'es')
    """
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang
    else:
        # Fall back to English if invalid language
        _current_lang = 'en'


def get_lang() -> str:
    """
    Get the current language setting.

    Returns:
        Current language code ('en' or 'es')
    """
    return _current_lang


def t(key: str) -> str:
    """
    Translate a key to the current language.

    Falls back to English if key not found in current language,
    then falls back to the key itself if not found in English either.

    Args:
        key: Translation key to look up

    Returns:
        Translated string
    """
    # Try current language
    if key in TRANSLATIONS.get(_current_lang, {}):
        return TRANSLATIONS[_current_lang][key]

    # Fall back to English
    if key in TRANSLATIONS.get('en', {}):
        return TRANSLATIONS['en'][key]

    # Fall back to key itself if not found anywhere
    return key
