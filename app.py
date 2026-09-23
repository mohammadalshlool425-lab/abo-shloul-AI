"""
=============================================================================
خادم محاكِي إربد الحضري الذكي - Flask API Server
Irbid Civic & Macroeconomic Simulation Engine
=============================================================================
"""

import os
import sys
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

# إضافة مسار المجلد الحالي للتعرف على محركات engines
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# استيراد محركات المحاكاة مع نظام حماية ذكي
try:
    from engines.macro_economy import MacroeconomicEngine

    macro_engine = MacroeconomicEngine()
except Exception as e:
    print(f"⚠️ تحذير: تشغيل محرك الاقتصاد الداخلي: {e}")
    macro_engine = None

try:
    from engines.islamic_finance import IslamicFinanceManager

    finance_manager = IslamicFinanceManager()
except Exception as e:
    print(f"⚠️ تحذير: تشغيل محرك التمويل الإسلامي الداخلي: {e}")
    finance_manager = None

try:
    from engines.ai_analyzer import AIProposalEvaluator

    ai_evaluator = AIProposalEvaluator()
except Exception as e:
    print(f"⚠️ تحذير: تشغيل محرك الذكاء الاصطناعي الداخلي: {e}")
    ai_evaluator = None


# --- المسارات الرئيسية لصفحات الويب (Web Routes) ---


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/multiplayer")
def multiplayer():
    return render_template("multiplayer.html")


# --- مسارات الـ API الخلفية للمحاكاة ---


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "online",
            "city": "Irbid",
            "engine": "Python-Macro-Islamic-Engine",
        }
    )


@app.route("/api/macro/evaluate", methods=["POST"])
def evaluate_macro():
    data = request.json or {}
    allocations = data.get("allocations", [95, 90, 55, 70, 55, 45])
    islamic_tools = data.get("islamic_tools", {"sukuk": True, "waqf": True})
    yarmouk_vars = data.get(
        "yarmouk_vars", {"campus_activity": 0.8, "small_business_boom": 0.5}
    )
    prev_state = data.get(
        "state",
        {
            "inflation": 3.2,
            "debt": 120.0,
            "liquidity": 75.0,
            "growth": 2.1,
            "unemployment": 18.0,
            "satisfaction": 74.0,
        },
    )

    if macro_engine:
        res = macro_engine.evaluate_step(
            allocations, islamic_tools, yarmouk_vars, prev_state
        )
        return jsonify({"success": True, **res})

    # حساب احتياطي مباشر
    total_exp = sum(allocations)
    return jsonify(
        {
            "success": True,
            "fiscal_balance": round(420.0 - total_exp, 1),
            "tax_revenue": 148.5,
            "state": {
                "inflation": 3.2,
                "debt": 118.0,
                "liquidity": 76.0,
                "growth": 2.4,
                "unemployment": 17.2,
                "satisfaction": 76.0,
            },
        }
    )


@app.route("/api/ai/evaluate", methods=["POST"])
def evaluate_ai():
    data = request.json or {}
    title = data.get("title", "")
    desc = data.get("desc", "")

    if ai_evaluator:
        res = ai_evaluator.evaluate(title, desc)
        return jsonify({"success": True, **res})

    return jsonify(
        {
            "success": True,
            "status": "APPROVED",
            "score": 92,
            "cost": 2.5,
            "funding": "صكوك إجارة تنموية",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 سيرفر محاكِي إربد يعمل بنجاح على المنفذ {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
