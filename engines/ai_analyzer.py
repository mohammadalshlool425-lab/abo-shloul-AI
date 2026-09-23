"""محرك الذكاء الاصطناعي لتقييم المقترحات"""
import os, json
from typing import Dict, Any

try:
    import google.generativeai as genai
    GEMINI_OK = True
except ImportError:
    GEMINI_OK = False

class AIProposalEvaluator:
    def __init__(self, budget=420.0):
        self.budget = budget
        key = os.getenv("GEMINI_API_KEY")
        if GEMINI_OK and key:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def evaluate(self, title: str, desc: str) -> Dict[str, Any]:
        text = (title + " " + desc).lower()
        if len(title) < 5 or len(desc) < 15:
            return {"status": "REJECTED", "reason": "مقترح قصير وغير مكتمل.", "score": 10, "cost": 0}

        absurd = ["قمر", "فضاء", "صاروخ", "برج إيفل", "ذهب خالص", "سيارات مجانية", "طائرات"]
        if any(w in text for w in absurd):
            return {"status": "REJECTED", "reason": "مقترح غير منطقي ومستحيل هندسياً.", "score": 6, "cost": 0}

        cat, cost, score, funding = "traffic", 2.5, 88, "صكوك إجارة"
        if any(w in text for w in ["طالب", "جامع", "يرموك", "تكنو"]):
            cat, cost, score, funding = "student", 2.8, 95, "وقف تعليمي"
        elif any(w in text for w in ["حديق", "بيئ", "شجر", "طاق"]):
            cat, cost, score, funding = "green", 1.6, 92, "وقف أخضر"

        return {
            "status": "APPROVED", "reason": None, "category": cat,
            "cost": cost, "score": score, "funding": funding,
            "budget_impact": round((cost / self.budget) * 100, 2)
        }
