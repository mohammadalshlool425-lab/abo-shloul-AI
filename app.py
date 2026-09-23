"""خادم Flask الرئيسي - محاكِي إربد الحضري المتكامل"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from engines.macro_economy import MacroeconomicEngine
from engines.islamic_finance import IslamicFinanceManager
from engines.ai_analyzer import AIProposalEvaluator

app = Flask(__name__)
CORS(app)

macro = MacroeconomicEngine()
finance = IslamicFinanceManager()
ai_eval = AIProposalEvaluator()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/multiplayer")
def multiplayer():
    return render_template("multiplayer.html")

@app.route("/api/macro/evaluate", methods=["POST"])
def evaluate_macro():
    data = request.json or {}
    result = macro.evaluate_step(
        data.get("allocations", [95, 90, 55, 70, 55, 45]),
        data.get("islamic_tools", {}),
        data.get("yarmouk_vars", {"campus_activity": 0.8, "small_business_boom": 0.5}),
        data.get("state", {"inflation": 3.2, "debt": 120, "liquidity": 75, "growth": 2.1, "unemployment": 18, "satisfaction": 74})
    )
    return jsonify({"success": True, **result})

@app.route("/api/finance/impact", methods=["GET"])
def finance_impact():
    return jsonify({"success": True, **finance.get_impact()})

@app.route("/api/ai/evaluate", methods=["POST"])
def ai_evaluate():
    data = request.json or {}
    result = ai_eval.evaluate(data.get("title", ""), data.get("desc", ""))
    return jsonify({"success": True, **result})

if __name__ == "__main__":
    print("🚀 محاكِي إربد الحضري يعمل على http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
