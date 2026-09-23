// ربط الواجهة مع Flask API + Firebase + التزامن لحظي
const API_BASE = window.location.origin;
const syncChannel = new BroadcastChannel('irbid_live_sync');

// 1. إرسال تحديث الميزانية لمحرك Python
async function dispatchMacroUpdate() {
    const allocs = [0,1,2,3,4,5].map(i => parseInt(document.getElementById('s'+i)?.value || 70));
    const payload = {
        allocations: allocs,
        islamic_tools: { sukuk: true, waqf: true },
        yarmouk_vars: getYarmoukVars(),
        state: { inflation: 3.2, debt: 120, liquidity: 75, growth: 2.1, unemployment: 18, satisfaction: 74 }
    };

    try {
        const res = await fetch(`${API_BASE}/api/macro/evaluate`, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) applyMacroResults(data);
    } catch(e) {
        console.log('Flask offline - using client engine');
        applyClientSideResults(allocs);
    }

    // بث التزامن لحظي
    syncChannel.postMessage({ type: 'SLIDER_UPDATE', allocs });
}

// 2. متغيرات طبقة جامعة اليرموك
function getYarmoukVars() {
    return {
        campus_activity: document.getElementById('toggleCampus')?.checked ? 0.9 : 0.4,
        small_business_boom: document.getElementById('toggleBiz')?.checked ? 0.8 : 0.3,
        morning_congestion: document.getElementById('toggleMorning')?.checked ? 0.7 : 0.9,
        housing_affordability: document.getElementById('toggleHousing')?.checked ? 0.85 : 0.5
    };
}

function updateYarmoukLayer() {
    const v = getYarmoukVars();
    const congestion = Math.round(95 - (v.campus_activity * 20) - (v.morning_congestion < 0.8 ? 15 : 0));
    const bizBoom = Math.round(40 + v.small_business_boom * 50 + v.campus_activity * 10);
    const housing = Math.round(v.housing_affordability * 100);
    const studentSpend = (120000 * v.campus_activity * 45 / 1000000).toFixed(1);

    const el = (id, val) => { const e = document.getElementById(id); if(e) e.innerText = val; };
    el('yCongestion', congestion + '%');
    el('yBizBoom', bizBoom + '%');
    el('yHousing', housing + '%');
    el('ySpend', studentSpend + 'M د.أ');
}

// 3. تطبيق النتائج
function applyMacroResults(data) {
    const s = data.state;
    const el = (id, val) => { const e = document.getElementById(id); if(e) e.innerText = val; };
    el('valInflation', s.inflation + '%');
    el('valDebt', s.debt + 'M');
    el('valLiquidity', s.liquidity + '%');
    el('valGrowth', s.growth + '%');
    el('valUnemployment', s.unemployment + '%');
    el('valSatisfaction', s.satisfaction + '%');
}

function applyClientSideResults(allocs) {
    const total = allocs.reduce((a,b) => a+b, 0);
    allocs.forEach((v, i) => {
        const e = document.getElementById('v'+i);
        if(e) e.innerText = v + 'M';
    });
}

// 4. التزامن لحظي
syncChannel.onmessage = (e) => {
    if (e.data.type === 'SLIDER_UPDATE') {
        e.data.allocs.forEach((v, i) => {
            const sl = document.getElementById('s'+i);
            if(sl) { sl.value = v; }
            const vl = document.getElementById('v'+i);
            if(vl) vl.innerText = v + 'M';
        });
    }
};

// تهيئة
document.addEventListener('DOMContentLoaded', () => {
    updateYarmoukLayer();
    dispatchMacroUpdate();
});
