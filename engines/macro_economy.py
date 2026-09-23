"""محرك الاقتصاد الكلي والضرائب - بلدية إربد الكبرى"""
import math
import numpy as np

class MacroeconomicEngine:
    def __init__(self, base_budget=420.0):
        self.BASE_BUDGET = base_budget
        self.POPULATION = 1_850_000
        self.STUDENTS = 135_000

    def calculate_tax_revenue(self, state, merchant_satisfaction=65.0, yarmouk_activity=0.8):
        base_tax = 140.0
        merchant_mult = 1.0 + ((merchant_satisfaction - 50) / 100) * 0.25
        yarmouk_bonus = yarmouk_activity * 12.0  # أثر نشاط اليرموك على ضرائب المبيعات
        growth_impact = max(-15, min(25, state.get("growth", 2.0) * 3.2))
        evasion = max(0, (state.get("inflation", 3.0) - 6) * 2.5)
        return float(np.clip((base_tax + yarmouk_bonus + growth_impact - evasion) * merchant_mult, 80, 240))

    def evaluate_step(self, allocations, islamic_tools, yarmouk_vars, prev_state):
        islamic_funding = sum([
            80 if islamic_tools.get("sukuk") else 0,
            35 if islamic_tools.get("waqf") else 0,
            50 if islamic_tools.get("musharakah") else 0
        ])
        effective_budget = self.BASE_BUDGET + islamic_funding
        total_exp = sum(allocations)

        tax = self.calculate_tax_revenue(prev_state, yarmouk_activity=yarmouk_vars.get("campus_activity", 0.8))
        fiscal_balance = (self.BASE_BUDGET * 0.65 + tax + islamic_funding) - total_exp

        # التضخم
        demand_pull = max(0, (total_exp - effective_budget) / effective_budget) * 3.5
        new_inflation = float(np.clip(prev_state.get("inflation", 3.2) + demand_pull - (0.9 if islamic_tools.get("sukuk") else 0), 0.8, 24))

        # السيولة
        infra_drain = max(0, (allocations[1] - 80) / 100) * 12
        new_liquidity = float(np.clip(prev_state.get("liquidity", 75) + fiscal_balance * 0.08 - infra_drain + (8 if islamic_tools.get("waqf") else 0), 8, 95))

        # النمو
        edu_boost = (allocations[3] / effective_budget) * 6.8
        yarmouk_growth = yarmouk_vars.get("small_business_boom", 0.5) * 1.5
        new_growth = float(np.clip(prev_state.get("growth", 2.1) + edu_boost + yarmouk_growth - max(0, new_inflation - 4.5) * 0.4, -3.5, 11))

        # البطالة
        new_unemployment = float(np.clip(prev_state.get("unemployment", 18) - (allocations[3] * 0.05) - (new_growth * 1.2) + 2, 4, 36))

        # الرضا
        new_satisfaction = float(np.clip((allocations[0] + allocations[3] + allocations[4]) / effective_budget * 65 + new_liquidity * 0.2 - max(0, new_inflation - 3) * 2, 10, 98))

        return {
            "fiscal_balance": round(fiscal_balance, 1),
            "tax_revenue": round(tax, 1),
            "effective_budget": round(effective_budget, 1),
            "state": {
                "inflation": round(new_inflation, 2),
                "debt": round(max(0, prev_state.get("debt", 120) + max(0, -fiscal_balance) * 0.5 - islamic_funding * 0.08), 1),
                "liquidity": round(new_liquidity, 1),
                "growth": round(new_growth, 2),
                "unemployment": round(new_unemployment, 1),
                "satisfaction": round(new_satisfaction, 1)
            }
        }
