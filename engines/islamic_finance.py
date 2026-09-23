"""محرك المصارف الإسلامية والوقف الرقمي"""
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class SukukIssue:
    id: str
    title: str
    structure: str  # Ijarah, Musharakah, Istisna
    target_million: float
    raised_million: float = 0.0
    annual_yield_pct: float = 0.0
    subscribers: int = 0

@dataclass
class WaqfAsset:
    id: str
    name: str
    waqf_type: str  # RealEstate, CashWaqf
    valuation_million: float
    annual_revenue_million: float
    beneficiary: str  # Students, Parks, Health
    donors: int = 0

class IslamicFinanceManager:
    def __init__(self):
        self.sukuk_portfolio: Dict[str, SukukIssue] = {}
        self.waqf_registry: Dict[str, WaqfAsset] = {}
        self._init_defaults()

    def _init_defaults(self):
        self.sukuk_portfolio["sukuk_transit"] = SukukIssue("sukuk_transit", "صكوك نفق ومواقف شارع الجامعة", "Ijarah", 18.0, 14.5, 6.8, 1380)
        self.sukuk_portfolio["sukuk_solar"] = SukukIssue("sukuk_solar", "صكوك محطة الطاقة الشمسية", "Musharakah", 12.0, 9.8, 7.5, 890)
        self.waqf_registry["waqf_students"] = WaqfAsset("waqf_students", "مجمع الوقف السكني لطلبة اليرموك", "RealEstate", 8.5, 0.72, "Students", 2950)
        self.waqf_registry["waqf_green"] = WaqfAsset("waqf_green", "سهم الوقف الأخضر لمتنزهات برقش", "CashWaqf", 4.0, 0.38, "Parks", 1820)

    def get_impact(self) -> Dict:
        total_sukuk = sum(s.raised_million for s in self.sukuk_portfolio.values())
        total_waqf_rev = sum(w.annual_revenue_million for w in self.waqf_registry.values())
        return {
            "total_sukuk_raised": round(total_sukuk, 2),
            "debt_avoided": round(total_sukuk, 2),
            "interest_saved_annual": round(total_sukuk * 0.065, 2),
            "waqf_annual_revenue": round(total_waqf_rev, 2),
            "sharia_compliance": 100.0
        }
