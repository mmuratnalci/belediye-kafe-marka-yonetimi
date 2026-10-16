from __future__ import annotations

from typing import Any

import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Kent Kafe | Marka Stratejisi Simülatörü",
    page_icon="☕",
    layout="wide",
)

# Simülasyon verileri eğitim amacıyla varsayımsaldır.
STRATEGIES = {
    "Sosyal ve Ekonomik": {
        "key": "sosyal",
        "accessibility": 80,
        "brand": 70,
        "audience": "Öğrenciler, emekliler ve aileler",
        "value": "Ulaşılabilir fiyatlarla herkes için sıcak ve kapsayıcı bir buluşma noktası.",
        "slogan": "Herkesin Kafesi",
        "short": "Sosyal",
    },
    "Yerel ve Özgün": {
        "key": "yerel",
        "accessibility": 66,
        "brand": 86,
        "audience": "Yerel ürünleri ve şehir kültürünü önemseyen kent sakinleri",
        "value": "Yerel lezzetleri ve üreticileri buluşturan, şehrin hikâyesini taşıyan kafe.",
        "slogan": "Şehrin Tadı, Mahallenin Buluşması",
        "short": "Yerel",
    },
    "Modern ve Kaliteli": {
        "key": "modern",
        "accessibility": 58,
        "brand": 75,
        "audience": "Nitelikli hizmet ve çağdaş kafe deneyimi arayan genç yetişkinler ve çalışanlar",
        "value": "Özenli hizmeti, çağdaş atmosferi ve tutarlı kaliteyi bir araya getiren deneyim.",
        "slogan": "Şehrin Yeni Buluşma Noktası",
        "short": "Modern",
    },
}

PRICE_POLICIES = ["Çok uygun", "Uygun", "Dengeli", "Yüksek", "Premium"]
PRICE_INDEX = {policy: index for index, policy in enumerate(PRICE_POLICIES)}
DEFAULTS = {
    "strategy": "Sosyal ve Ekonomik",
    "price_policy": "Çok uygun",
    "quality": 3,
    "budget": 20_000,
}
MAX_SIMULATION_MONTHS = 6
BASE_MONTHLY_CUSTOMERS = 2_700
BASE_AVERAGE_SPEND = 100
PRODUCT_COST_RATE = 0.32
PRICE_COST_RATE = 0.015
BASE_STAFF_COST = 100_000
QUALITY_STAFF_COST = 10_000
BASE_OPERATING_COST = 30_000
OPERATING_COST_PER_CUSTOMER = 5
NAVIGATION = [
    "Yönetim Paneli",
    "Marka Kimliği",
    "Stratejik Kararlar",
    "Aylık Simülasyon",
    "Performans Analizi",
    "Strateji Danışmanı",
]
STRATEGY_THEMES = {
    "Sosyal ve Ekonomik": {
        "name": "Sosyal Kafe",
        "accent": "#2E6248",
        "tint": "#E6F0E7",
        "description": "Erişilebilir ve kapsayıcı",
    },
    "Yerel ve Özgün": {
        "name": "Yerel Kafe",
        "accent": "#8C4F32",
        "tint": "#F4E8DE",
        "description": "Yerel üretim ve kent kültürü",
    },
    "Modern ve Kaliteli": {
        "name": "Modern Kafe",
        "accent": "#28636A",
        "tint": "#E3F0F1",
        "description": "Çağdaş deneyim ve özenli hizmet",
    },
}


def clamp_score(value: float) -> float:
    """Bir performans puanını 0-100 aralığında tutar."""
    return max(0.0, min(100.0, value))


def calculate_performance(
    strategy_name: str, price_index: int, quality: int, budget: int
) -> dict[str, float]:
    """Belirlenen varsayımsal formüllerle üç performans puanını hesaplar."""
    strategy = STRATEGIES[strategy_name]
    accessibility = strategy["accessibility"] - (price_index * 9) - (quality * 2)
    financial_balance = 55 + (price_index * 11) - (quality * 5) + (budget / 10_000 * 3)
    brand_strength = strategy["brand"] + (quality * 4) + (budget / 10_000 * 2)

    return {
        "Marka Gücü": clamp_score(brand_strength),
        "Finansal Denge": clamp_score(financial_balance),
        "Toplumsal Erişilebilirlik": clamp_score(accessibility),
    }


def calculate_financials(
    price_index: int,
    quality: int,
    budget: int,
    scores: dict[str, float],
) -> dict[str, float]:
    """Aylık finans tahminini açık, sentetik maliyet varsayımlarıyla hesaplar."""
    customer_change = (
        (scores["Marka Gücü"] - 86) * 18
        + (scores["Toplumsal Erişilebilirlik"] - 74) * 10
        + ((budget - 20_000) / 5_000) * 40
    )
    customers = max(0, round(BASE_MONTHLY_CUSTOMERS + customer_change))
    average_spend = BASE_AVERAGE_SPEND + (price_index * 18) + (quality * 2)
    revenue = customers * average_spend
    product_cost = revenue * (PRODUCT_COST_RATE + price_index * PRICE_COST_RATE)
    staff_cost = BASE_STAFF_COST + (quality * QUALITY_STAFF_COST)
    operating_cost = BASE_OPERATING_COST + (customers * OPERATING_COST_PER_CUSTOMER)
    total_expenses = product_cost + staff_cost + operating_cost + budget

    return {
        "Aylık Müşteri": customers,
        "Ortalama Harcama": average_spend,
        "Ciro": revenue,
        "Ürün Maliyeti": product_cost,
        "Personel Gideri": staff_cost,
        "İşletme Gideri": operating_cost,
        "Tanıtım Gideri": budget,
        "Toplam Gider": total_expenses,
        "Faaliyet Sonucu": revenue - total_expenses,
    }


def format_tl(value: float) -> str:
    """Türkçe sayı biçimiyle TL değerini gösterir."""
    return f"{value:,.0f}".replace(",", ".") + " TL"


def evaluate_month(record: dict[str, Any]) -> list[str]:
    """Kaydedilmiş ay için üç kısa ve kararlarla ilişkili değerlendirme üretir."""
    strategy_name = record["strategy"]
    price_index = record["price_index"]
    quality = record["quality"]
    financials = record["financials"]
    scores = record["scores"]

    if strategy_name == "Sosyal ve Ekonomik" and price_index >= 3:
        positioning_note = "Sosyal konumlandırma ile yüksek fiyat arasında belirgin bir tutarsızlık var."
    elif quality >= 4 and price_index <= 1 and financials["Faaliyet Sonucu"] < 0:
        positioning_note = "Yüksek hizmet yatırımı ve uygun fiyat birlikte faaliyet sonucunu baskılıyor."
    elif strategy_name == "Modern ve Kaliteli" and quality <= 2:
        positioning_note = "Modern kalite vaadi, düşük hizmet yatırımıyla yeterince desteklenmiyor."
    else:
        positioning_note = f"{strategy_name} konumlandırması seçili fiyat ve hizmet kararlarıyla genel olarak uyumlu."

    result = financials["Faaliyet Sonucu"]
    if result < 0:
        financial_note = f"Faaliyet sonucu {format_tl(result)}; giderler bu ay cironun üzerinde."
    else:
        financial_note = f"Faaliyet sonucu {format_tl(result)}; bu varsayımlarda ciro giderleri karşılıyor."

    if scores["Toplumsal Erişilebilirlik"] < 55:
        access_note = "Erişilebilirlik puanı 55'in altında; fiyat ve hizmet maliyeti dengesini gözden geçirin."
    elif scores["Marka Gücü"] > scores["Toplumsal Erişilebilirlik"] + 20:
        access_note = "Marka gücü erişilebilirlikten belirgin biçimde yüksek; toplumsal erişimi korumayı değerlendirin."
    else:
        access_note = "Marka gücü ve toplumsal erişilebilirlik arasındaki denge bu ay korunuyor."

    return [positioning_note, financial_note, access_note]


def advance_simulation() -> None:
    """Mevcut widget kararlarını callback sırasında bir aylık kayıt olarak saklar."""
    history = st.session_state.simulation_history
    if len(history) >= MAX_SIMULATION_MONTHS:
        return

    strategy_name = st.session_state["strategy"]
    price_policy = st.session_state["price_policy"]
    price_index = PRICE_INDEX[price_policy]
    quality = st.session_state["quality"]
    budget = st.session_state["budget"]
    scores = calculate_performance(strategy_name, price_index, quality, budget)
    financials = calculate_financials(price_index, quality, budget, scores)
    month_record = {
        "month": len(history) + 1,
        "strategy": strategy_name,
        "price_policy": price_policy,
        "price_index": price_index,
        "quality": quality,
        "budget": budget,
        "scores": scores,
        "financials": financials,
    }
    month_record["evaluations"] = evaluate_month(month_record)
    st.session_state.simulation_history = [*history, month_record]
    st.session_state.last_advanced_month = month_record["month"]


def get_recommendations(
    strategy_name: str, price_index: int, quality: int, budget: int
) -> list[str]:
    """Seçimlere göre açıklanabilir, kural tabanlı öneriler oluşturur."""
    recommendations = []
    strategy = STRATEGIES[strategy_name]

    if strategy_name == "Sosyal ve Ekonomik" and price_index >= 3:
        recommendations.append(
            "Sosyal ve ekonomik konumlandırma ile yüksek fiyat arasında tutarsızlık oluşabilir. "
            "Fiyat politikasını marka vaadiyle birlikte gözden geçirin."
        )
    if quality >= 4 and price_index <= 1:
        recommendations.append(
            "Yüksek kalite yatırımı ve uygun fiyat birlikte finansal sürdürülebilirlik riski yaratabilir. "
            "Maliyetleri ve uzun vadeli kaynakları izleyin."
        )
    if budget < 10_000:
        recommendations.append(
            "Tanıtım bütçesi düşük. Yerel etkinlikler, ağızdan ağıza iletişim ve belediye kanallarıyla "
            "marka bilinirliğini geliştirmeyi değerlendirin."
        )
    if strategy_name == "Yerel ve Özgün":
        recommendations.append(
            "Yerel üreticilerle iş birlikleri kurun; menüde ürünlerin ve üreticilerin hikâyelerine yer verin."
        )
    if strategy_name == "Modern ve Kaliteli":
        recommendations.append(
            "Hizmet kalitesi ve deneyim odaklı farklılaşmayı güçlendirin; ekip eğitimini ve kafe atmosferini birlikte ele alın."
        )
    if not recommendations:
        recommendations.append(
            f"{strategy['short']} konumlandırmanızla tutarlı bir deneyim sunmak için fiyat, hizmet ve iletişim kararlarını birlikte yönetin."
        )

    return recommendations


def build_report(
    strategy_name: str,
    price_policy: str,
    quality: int,
    budget: int,
    scores: dict[str, float],
    recommendations: list[str],
) -> str:
    """Öğrenci kararlarını, sonuçları ve model varsayımlarını TXT olarak hazırlar."""
    strategy = STRATEGIES[strategy_name]
    recommendation_lines = "\n".join(f"- {item}" for item in recommendations)
    return f"""KENT KAFE - STRATEJİ RAPORU
Eğitim amacıyla hazırlanmış varsayımsal simülasyon

MARKA KİMLİĞİ
Marka: Kent Kafe
Strateji: {strategy_name}
Hedef kitle: {strategy['audience']}
Değer önerisi: {strategy['value']}
Marka vaadi / slogan: {strategy['slogan']}

STRATEJİK KARARLAR
Fiyat politikası: {price_policy} (indeks {PRICE_INDEX[price_policy]})
Hizmet kalitesi yatırımı: {quality}/5
Aylık tanıtım bütçesi: {budget:,.0f} TL

PERFORMANS SONUÇLARI
Marka Gücü: {scores['Marka Gücü']:.1f}/100
Finansal Denge: {scores['Finansal Denge']:.1f}/100
Toplumsal Erişilebilirlik: {scores['Toplumsal Erişilebilirlik']:.1f}/100

MODELİN KISA AÇIKLAMASI
Tanıtım bütçesi hesaplamalarda kesirli değerlerle kullanılır. Puanlar 0-100 aralığında sınırlandırılır.
Erişilebilirlik = strateji temel puanı - (fiyat indeksi x 9) - (kalite yatırımı x 2)
Finansal Denge = 55 + (fiyat indeksi x 11) - (kalite yatırımı x 5) + (bütçe / 10.000 x 3)
Marka Gücü = strateji temel puanı + (kalite yatırımı x 4) + (bütçe / 10.000 x 2)
Bu formüller bilimsel tahmin değildir; karar ilişkilerini öğretmek için tasarlanmış varsayımsal bir simülasyondur.

KURAL TABANLI STRATEJİ DANIŞMANI
{recommendation_lines}
"""


def reset_settings() -> None:
    """Başlangıç senaryosunu widget durumuna geri yükler."""
    for key, value in DEFAULTS.items():
        st.session_state[key] = value


def reset_simulation() -> None:
    """Kaydedilmiş aylık sonuçları temizler."""
    st.session_state.simulation_history = []


def select_strategy(strategy_name: str) -> None:
    """Görsel konumlandırma kartından seçilen stratejiyi uygular."""
    st.session_state.strategy = strategy_name


def build_history_rows(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Kaydedilmiş simülasyon aylarını grafiklerin kullanacağı satırlara çevirir."""
    return [
        {
            "Ay": f"Ay {record['month']}",
            "Ciro": record["financials"]["Ciro"],
            "Toplam Gider": record["financials"]["Toplam Gider"],
            "Faaliyet Sonucu": record["financials"]["Faaliyet Sonucu"],
            "Sonuç Türü": "Pozitif" if record["financials"]["Faaliyet Sonucu"] >= 0 else "Negatif",
            "Marka Gücü": record["scores"]["Marka Gücü"],
            "Toplumsal Erişilebilirlik": record["scores"]["Toplumsal Erişilebilirlik"],
        }
        for record in history
    ]


def render_history_charts(history: list[dict[str, Any]]) -> None:
    """Aylık ciro/gider, faaliyet sonucu ve marka göstergesi grafiklerini gösterir."""
    if not history:
        st.info("Aylık eğilimleri görmek için Stratejik Kararlar bölümünde ilk ayı kaydedin.")
        return

    rows = build_history_rows(history)
    revenue_column, result_column = st.columns(2)
    with revenue_column:
        revenue_chart = px.bar(
            rows,
            x="Ay",
            y=["Ciro", "Toplam Gider"],
            barmode="group",
            color_discrete_sequence=["#526b4b", "#b48b62"],
            labels={"value": "Tutar (TL)", "variable": "Kalem"},
        )
        revenue_chart.update_layout(
            title="Aylık ciro ve giderler",
            height=340,
            margin=dict(l=12, r=12, t=50, b=12),
            plot_bgcolor="#fffdf8",
            paper_bgcolor="#f7f5ef",
            legend_title=None,
        )
        st.plotly_chart(revenue_chart, width="stretch", config={"displayModeBar": False, "responsive": True})
    with result_column:
        result_chart = px.bar(
            rows,
            x="Ay",
            y="Faaliyet Sonucu",
            color="Sonuç Türü",
            color_discrete_map={"Pozitif": "#526b4b", "Negatif": "#a4473d"},
            labels={"Faaliyet Sonucu": "Sonuç (TL)"},
        )
        result_chart.add_hline(y=0, line_dash="dot", line_color="#654735")
        result_chart.update_layout(
            title="Aylık faaliyet sonucu",
            height=340,
            margin=dict(l=12, r=12, t=50, b=12),
            plot_bgcolor="#fffdf8",
            paper_bgcolor="#f7f5ef",
            showlegend=False,
        )
        st.plotly_chart(result_chart, width="stretch", config={"displayModeBar": False, "responsive": True})

    brand_chart = px.line(
        rows,
        x="Ay",
        y=["Marka Gücü", "Toplumsal Erişilebilirlik"],
        markers=True,
        range_y=[0, 100],
        color_discrete_sequence=["#7c5942", "#526b4b"],
        labels={"value": "Puan (0-100)", "variable": "Gösterge"},
    )
    brand_chart.update_layout(
        title="Marka ve toplum göstergeleri",
        height=330,
        margin=dict(l=12, r=12, t=50, b=12),
        plot_bgcolor="#fffdf8",
        paper_bgcolor="#f7f5ef",
        legend_title=None,
    )
    st.plotly_chart(brand_chart, width="stretch", config={"displayModeBar": False, "responsive": True})


# Sıfırlama geri çağrısı widget'lar oluşturulmadan önce çalışır.
for state_key, default_value in DEFAULTS.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value
if "simulation_history" not in st.session_state:
    st.session_state.simulation_history = []
if "active_view" not in st.session_state:
    st.session_state.active_view = "Yönetim Paneli"

selected_strategy = st.session_state.strategy
selected_theme = STRATEGY_THEMES[selected_strategy]
st.markdown(
    f"<style>:root {{ --accent: {selected_theme['accent']}; --accent-tint: {selected_theme['tint']}; }}</style>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    :root {
        --coffee: #654735;
        --coffee-dark: #3e3027;
        --cream: #f7f3e9;
        --leaf: #526b4b;
        --ink: #282a25;
        --muted: #676b61;
    }
    .stApp { background: #f7f5ef; color: var(--ink); }
    .block-container { max-width: 1500px; padding: 1.25rem 2.3rem 3rem; }
    h1, h2, h3 { color: var(--coffee-dark); }
    [data-testid="stSidebar"] { background: #eee8dc; border-right: 1px solid #ded4c6; }
    [data-testid="stSidebar"] * { color: #302820; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 7px; padding: .45rem .6rem; color: #302820 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: var(--accent) !important; color: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) * { color: #ffffff !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:not(:has(input:checked)):hover { background: #e1d8ca; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label * { color: inherit !important; }
    [data-testid="stWidgetLabel"] p, [data-testid="stMarkdown"] p, label, small { color: #302820; }
    [data-testid="stSlider"] [data-baseweb="slider"] { color: var(--accent); }
    [data-testid="stSelectSlider"] [role="slider"] { background: var(--accent); }
    [data-testid="stSelectbox"] label, [data-testid="stSlider"] label { color: #302820 !important; }
    [data-testid="stSlider"] [data-testid="stTickBar"] div,
    [data-testid="stSelectSlider"] [data-testid="stTickBar"] div { color: #302820 !important; }
    [data-testid="stButton"] button {
        border-radius: 7px; font-weight: 650; min-height: 2.7rem;
        border: 1px solid #cfc4b4; color: #302820; background: #fffdf8;
    }
    [data-testid="stBaseButton-primary"] { background: var(--accent) !important; border-color: var(--accent) !important; color: #ffffff !important; }
    [data-testid="stBaseButton-primary"] * { color: #ffffff !important; }
    [data-testid="stBaseButton-secondary"] { background: #fffdf8 !important; color: #302820 !important; }
    [data-testid="stButton"] button[kind="primary"] {
        background: var(--accent); border-color: var(--accent); color: #ffffff !important;
    }
    [data-testid="stButton"] button[kind="secondary"] { background: #fffdf8; color: #302820 !important; }
    [data-testid="stButton"] button:disabled { color: #68645e !important; background: #e7e2d9; }
    .page-heading { display:flex; justify-content:space-between; align-items:center; gap:1rem; margin:.2rem 0 1.25rem; }
    .page-heading h1 { margin:0; font-size:2rem; }
    .eyebrow { color:var(--accent); font-size:.78rem; font-weight:750; letter-spacing:.08em; text-transform:uppercase; }
    .tagline { color:#5d5b54; margin-top:.3rem; font-size:1rem; }
    .period-badge { background:var(--accent-tint); border:1px solid var(--accent); border-radius:8px; padding:.65rem 1rem; min-width:180px; text-align:right; }
    .period-badge span { display:block; color:#514b43; font-size:.72rem; font-weight:700; text-transform:uppercase; }
    .period-badge strong { color:var(--accent); font-size:1.05rem; }
    .section-heading { margin:.4rem 0 .2rem; }
    .section-caption { color:#625f58; margin-bottom:1rem; }
    .identity-box {
        background: #fffdf8; border: 1px solid #e7dfd0; border-radius: 8px;
        padding: 1rem 1.1rem; min-height: 122px; margin-bottom: .5rem;
    }
    .identity-label { color: var(--leaf); font-weight: 700; font-size: .82rem; text-transform: uppercase; }
    .identity-value { color: var(--coffee-dark); margin-top: .35rem; }
    .strategy-card { background:#fffdf8; border:2px solid #ded4c6; border-radius:9px; padding:1.1rem; min-height:205px; }
    .strategy-card.selected { border-color:var(--card-accent); background:var(--card-tint); box-shadow:0 4px 16px #34291d18; }
    .strategy-card h3 { color:#302820; margin:.6rem 0 .3rem; font-size:1.2rem; }
    .strategy-card p { color:#514c44; min-height:2.8rem; margin-bottom:.5rem; }
    .strategy-card .strategy-check { color:var(--card-accent); font-weight:800; }
    [data-testid="stMetric"] { background:#fffdf8; border:1px solid #dfd6ca; border-top:4px solid var(--accent); border-radius:8px; padding:1rem; min-height:125px; }
    [data-testid="stMetricValue"] { color:#302820; font-size:1.55rem; }
    [data-testid="stMetricLabel"] { color:#3c5643; font-weight:650; }
    div[data-testid="stExpander"] { background:#fffdf8; border:1px solid #ded4c6; border-radius:7px; }
    [data-testid="stDataFrame"] { border:1px solid #ded4c6; border-radius:7px; }
    div[data-testid="stProgress"] > div > div { background-color: var(--leaf); }
    .note { color:#5f5a52; font-size:.92rem; }
    @media (max-width: 640px) {
        .block-container { padding:1rem .8rem 2rem; }
        .page-heading { align-items:flex-start; flex-direction:column; }
        .page-heading h1 { font-size:1.65rem; }
        .period-badge { text-align:left; }
        .identity-box { min-height: 0; }
        .strategy-card { min-height:0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## KENT KAFE")
    st.caption("MARKA YÖNETİMİ SİMÜLATÖRÜ")
    active_view = st.radio(
        "Gezinme",
        options=NAVIGATION,
        key="active_view",
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(f"Dönem: {min(len(st.session_state.simulation_history) + 1, MAX_SIMULATION_MONTHS)} / {MAX_SIMULATION_MONTHS}")
    st.progress(min(len(st.session_state.simulation_history) / MAX_SIMULATION_MONTHS, 1.0))

strategy_name = st.session_state.strategy
price_policy = st.session_state.price_policy
price_index = PRICE_INDEX[price_policy]
quality = st.session_state.quality
budget = st.session_state.budget
scores = calculate_performance(strategy_name, price_index, quality, budget)
recommendations = get_recommendations(strategy_name, price_index, quality, budget)
financials = calculate_financials(price_index, quality, budget, scores)
history = st.session_state.simulation_history
current_period = "Simülasyon tamamlandı" if len(history) >= MAX_SIMULATION_MONTHS else f"Ay {len(history) + 1} / {MAX_SIMULATION_MONTHS}"
selected_theme = STRATEGY_THEMES[strategy_name]

st.markdown(
    f"""
    <div class="page-heading">
      <div><div class="eyebrow">KENT KAFE · MARKA YÖNETİMİ</div>
      <h1>Kent Kafe</h1><div class="tagline">{STRATEGIES[strategy_name]['slogan']}</div></div>
      <div class="period-badge"><span>{current_period}</span><strong>{selected_theme['name']}</strong></div>
    </div>
    """,
    unsafe_allow_html=True,
)

if active_view == "Yönetim Paneli":
    st.markdown('<div class="section-heading"><h2>Yönetim Paneli</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Güncel kararların tahmini etkisi ve simülasyonun genel görünümü.</div>', unsafe_allow_html=True)
    kpi_columns = st.columns(4)
    kpi_columns[0].metric("Aylık müşteri", f"{financials['Aylık Müşteri']:,}".replace(",", "."))
    kpi_columns[1].metric("Tahmini ciro", format_tl(financials["Ciro"]))
    kpi_columns[2].metric(
        "Faaliyet sonucu",
        format_tl(financials["Faaliyet Sonucu"]),
        help="Ciro eksi ürün, personel, işletme ve tanıtım giderleri. Negatif değer zarar anlamına gelir.",
    )
    kpi_columns[3].metric("Marka gücü", f"{scores['Marka Gücü']:.1f} / 100")

    st.subheader("Marka sağlığı")
    gauge_columns = st.columns(3)
    gauge_values = [
        ("Marka Gücü", scores["Marka Gücü"], "Tanınma ve tercih edilme potansiyeli"),
        ("Toplumsal Erişilebilirlik", scores["Toplumsal Erişilebilirlik"], "Hizmetin farklı gruplara erişimi"),
        ("Finansal Denge", scores["Finansal Denge"], "Fiyat, kalite ve tanıtım dengesi"),
    ]
    for column, (label, value, description) in zip(gauge_columns, gauge_values):
        with column:
            st.markdown(f"**{label}** · {value:.1f} / 100")
            st.progress(int(round(value)))
            st.caption(description)

    overview_left, overview_right = st.columns([1.25, 1])
    with overview_left:
        st.subheader("Seçili marka yönü")
        st.markdown(
            f"""
            <div class="strategy-card selected" style="--card-accent:{selected_theme['accent']};--card-tint:{selected_theme['tint']};">
              <div class="eyebrow">{selected_theme['name']} · {selected_theme['description']}</div>
              <h3>{STRATEGIES[strategy_name]['slogan']}</h3>
              <p>{STRATEGIES[strategy_name]['value']}</p>
              <span class="strategy-check">HEDEF KİTLE</span><br>{STRATEGIES[strategy_name]['audience']}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with overview_right:
        st.subheader("Mevcut ayın finans görünümü")
        current_finance_rows = [
            {"Kalem": "Ciro", "Tutar": financials["Ciro"]},
            {"Kalem": "Toplam gider", "Tutar": financials["Toplam Gider"]},
        ]
        overview_chart = px.bar(
            current_finance_rows,
            x="Kalem",
            y="Tutar",
            color="Kalem",
            color_discrete_map={"Ciro": selected_theme["accent"], "Toplam gider": "#b48b62"},
            labels={"Tutar": "Tutar (TL)"},
        )
        overview_chart.update_layout(
            height=270,
            margin=dict(l=8, r=8, t=12, b=8),
            showlegend=False,
            plot_bgcolor="#fffdf8",
            paper_bgcolor="#f7f5ef",
        )
        st.plotly_chart(overview_chart, width="stretch", config={"displayModeBar": False, "responsive": True})

    st.divider()
    st.subheader("Aylık eğilim")
    render_history_charts(history)
    with st.expander("Öğrenciler için tartışma soruları"):
        st.markdown(
            """
1. Belediye kafesi kârlılığı mı yoksa toplumsal erişilebilirliği mi öncelemelidir?
2. Çok uygun fiyat politikası güçlü bir marka oluşturmak için yeterli midir?
3. Tanıtım bütçesi artırılmadan marka gücü nasıl geliştirilebilir?
"""
        )
    st.caption("Tüm veriler eğitim amacıyla kullanılan varsayımsal verilerdir; gerçek belediye verisi kullanılmamaktadır.")

if active_view == "Marka Kimliği":
    st.subheader("Marka konumlandırması")
    st.caption("Kafenin hangi temel değerle sesleneceğini üç konumlandırma kartından seçin.")
    strategy_columns = st.columns(3)
    for column, (name, data) in zip(strategy_columns, STRATEGIES.items()):
        theme = STRATEGY_THEMES[name]
        is_selected = name == strategy_name
        selection_label = "✓ SEÇİLİ" if is_selected else "STRATEJİ KARTI"
        with column:
            st.markdown(
                f"""
                <div class="strategy-card {'selected' if is_selected else ''}" style="--card-accent:{theme['accent']};--card-tint:{theme['tint']};">
                  <div class="strategy-check">{selection_label}</div>
                  <h3>{theme['name']}</h3>
                  <p>{theme['description']}</p>
                  <strong>{data['slogan']}</strong><br><small>{data['value']}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.button(
                "Seçili konumlandırma" if is_selected else "Bu stratejiyi seç",
                key=f"select_{data['key']}",
                type="primary" if is_selected else "secondary",
                disabled=is_selected,
                on_click=select_strategy,
                args=(name,),
                width="stretch",
            )

    selected_strategy = STRATEGIES[strategy_name]
    st.divider()
    st.subheader(f"{selected_theme['name']} marka kimliği")
    identity_columns = st.columns(3)
    for column, label, value in zip(
        identity_columns,
        ["Temel hedef kitle", "Değer önerisi", "Marka vaadi"],
        [selected_strategy["audience"], selected_strategy["value"], selected_strategy["slogan"]],
    ):
        column.markdown(
            f'<div class="identity-box"><div class="identity-label">{label}</div>'
            f'<div class="identity-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

if active_view == "Stratejik Kararlar":
    st.subheader("Stratejik kararlar")
    st.caption("Bir ayarı değiştirdiğinizde mevcut ay tahmini güncellenir. Ay sonu kararınızı kaydetmek için ilerleyin.")
    history = st.session_state.simulation_history
    st.progress(len(history) / MAX_SIMULATION_MONTHS)
    st.caption(f"Simülasyon ilerlemesi: {len(history)} / {MAX_SIMULATION_MONTHS} ay")
    decision_left, decision_right = st.columns(2)
    with decision_left:
        price_policy = st.select_slider(
            "Fiyat politikası",
            options=PRICE_POLICIES,
            key="price_policy",
            help="Fiyat indeksi çok uygun için 0, Premium için 4'tür; artan fiyat erişilebilirliği azaltır.",
        )
        st.caption("Daha düşük fiyatlar erişimi destekler; yüksek fiyatlar finansal denge puanını artırır.")
        quality = st.slider(
            "Hizmet kalitesine yatırım (1-5)",
            min_value=1,
            max_value=5,
            key="quality",
            help="Yatırım marka gücünü destekler; bu basit modelde finansal denge puanından düşülür.",
        )
        st.caption("Hizmet eğitimi ve süreç iyileştirmesi gibi kalite yatırımlarını temsil eder.")
    with decision_right:
        budget = st.slider(
            "Aylık tanıtım bütçesi (TL)",
            min_value=0,
            max_value=50_000,
            step=5_000,
            key="budget",
            help="Bütçe, formüllerde 10.000 TL birimlerine dönüştürülür; ara değerler korunur.",
        )
        st.caption("Yerel etkinlik, basılı/dijital iletişim ve kampanya harcamalarını düşünün.")
        st.info(f"Seçili marka stratejisi: **{strategy_name}**. Stratejiyi A. Marka Kimliği bölümünden değiştirebilirsiniz.")
    advance_column, clear_column, defaults_column = st.columns([1.35, 1.15, 1.45])
    with advance_column:
        st.button(
            "Bir Ay İlerle",
            type="primary",
            disabled=len(history) >= MAX_SIMULATION_MONTHS,
            on_click=advance_simulation,
            help="Mevcut kararları ay sonu sonucu olarak kaydeder.",
            width="stretch",
        )
    with clear_column:
        st.button(
            "Simülasyonu Sıfırla",
            on_click=reset_simulation,
            disabled=not history,
            help="Kaydedilen ayları temizler; seçili stratejik kararlar korunur.",
            width="stretch",
        )
    with defaults_column:
        st.button(
            "Başlangıç Ayarlarına Dön",
            on_click=reset_settings,
            help="Strateji, fiyat, kalite ve bütçeyi başlangıç değerlerine döndürür.",
            type="secondary",
            width="stretch",
        )

    newly_advanced_month = st.session_state.pop("last_advanced_month", None)
    if newly_advanced_month is not None:
        st.success(f"Ay {newly_advanced_month} kaydedildi. Kararlarınız ay sonu sonuçlarına işlendi.")
    history = st.session_state.simulation_history
    if history:
        latest_month = history[-1]
        with st.expander(
            f"Ay {latest_month['month']} yönetici değerlendirmesi",
            expanded=newly_advanced_month is not None,
        ):
            for evaluation in latest_month["evaluations"]:
                st.markdown(f"- {evaluation}")

price_index = PRICE_INDEX[price_policy]
scores = calculate_performance(strategy_name, price_index, quality, budget)
recommendations = get_recommendations(strategy_name, price_index, quality, budget)
financials = calculate_financials(price_index, quality, budget, scores)

if active_view == "Aylık Simülasyon":
    st.subheader("Aylık Simülasyon")
    st.caption("Her ayın kararlarını, finans sonuçlarını ve marka göstergelerini karşılaştırın.")
    st.progress(len(history) / MAX_SIMULATION_MONTHS)
    st.caption(f"Kaydedilen dönem: {len(history)} / {MAX_SIMULATION_MONTHS} ay")
    if history:
        month_columns = st.columns(min(len(history), 3))
        for index, record in enumerate(history):
            column = month_columns[index % len(month_columns)]
            with column:
                st.markdown(f"**Ay {record['month']} · {STRATEGY_THEMES[record['strategy']]['name']}**")
                st.metric("Faaliyet sonucu", format_tl(record["financials"]["Faaliyet Sonucu"]))
                st.caption(
                    f"{record['price_policy']} fiyat · kalite {record['quality']}/5 · "
                    f"tanıtım {format_tl(record['budget'])}"
                )
        st.divider()
        st.subheader("Dönem eğilimleri")
        render_history_charts(history)
        st.subheader("Aylık karar kayıtları")
        simulation_rows = [
            {
                "Ay": f"Ay {record['month']}",
                "Strateji": STRATEGY_THEMES[record["strategy"]]["name"],
                "Fiyat": record["price_policy"],
                "Kalite": f"{record['quality']}/5",
                "Tanıtım bütçesi": format_tl(record["budget"]),
                "Müşteri": f"{record['financials']['Aylık Müşteri']:,}".replace(",", "."),
                "Ciro": format_tl(record["financials"]["Ciro"]),
                "Faaliyet sonucu": format_tl(record["financials"]["Faaliyet Sonucu"]),
            }
            for record in history
        ]
        st.dataframe(simulation_rows, hide_index=True, width="stretch")
        with st.expander("Aylık yönetici değerlendirmeleri"):
            for record in history:
                st.markdown(f"**Ay {record['month']} · {STRATEGY_THEMES[record['strategy']]['name']}**")
                for evaluation in record["evaluations"]:
                    st.markdown(f"- {evaluation}")
    else:
        st.info("Henüz bir ay kaydedilmedi. Stratejik Kararlar sayfasından seçimlerinizi yapıp ‘Bir Ay İlerle’ düğmesine basın.")

if active_view == "Performans Analizi":
    st.subheader("Marka performans paneli")
    metric_columns = st.columns(3)
    explanations = {
        "Marka Gücü": "Markanın tanınma ve tercih edilme potansiyelini temsil eden varsayımsal puan.",
        "Finansal Denge": "Fiyat, kalite yatırımı ve tanıtım bütçesi arasındaki model dengesini gösterir.",
        "Toplumsal Erişilebilirlik": "Fiyat ve strateji tercihleriyle hizmete erişimin ne ölçüde desteklendiğini gösterir.",
    }
    for column, (metric_name, score) in zip(metric_columns, scores.items()):
        column.metric(metric_name, f"{score:.1f} / 100")
        column.progress(int(round(score)))
        column.caption(f"**Bu ne anlama geliyor?** {explanations[metric_name]}")

    chart_data = [{"Gösterge": name, "Puan": score} for name, score in scores.items()]
    chart = px.bar(
        chart_data,
        x="Puan",
        y="Gösterge",
        orientation="h",
        range_x=[0, 100],
        text=chart_data and [f"{row['Puan']:.1f}" for row in chart_data],
        color="Gösterge",
        color_discrete_sequence=["#526b4b", "#b48b62", "#7c5942"],
    )
    chart.update_layout(
        showlegend=False,
        height=285,
        margin=dict(l=12, r=20, t=12, b=12),
        xaxis_title="Puan (0-100)",
        yaxis_title=None,
        font=dict(color="#282a25"),
        plot_bgcolor="#fffdf8",
        paper_bgcolor="#f7f5ef",
    )
    chart.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(chart, width="stretch", config={"displayModeBar": False, "responsive": True})

    st.caption(
        "Model notu: Formüller bilimsel olarak doğrulanmış tahminler değildir; marka yönetimi kararları arasındaki ilişkileri öğretmek için tasarlanmış varsayımsal bir simülasyondur."
    )

    st.divider()
    st.subheader("Aylık finansal görünüm")
    st.caption("Aşağıdaki değerler, seçili kararlarla bir ay çalışmanın sentetik tahminidir.")
    financial_top = st.columns(4)
    financial_top[0].metric("Aylık müşteri", f"{financials['Aylık Müşteri']:,}".replace(",", "."))
    financial_top[1].metric("Ortalama harcama", format_tl(financials["Ortalama Harcama"]))
    financial_top[2].metric("Ciro", format_tl(financials["Ciro"]))
    financial_top[3].metric(
        "Faaliyet sonucu",
        format_tl(financials["Faaliyet Sonucu"]),
        help="Ciro eksi ürün, personel, işletme ve tanıtım giderleri. Negatif değer zarar anlamına gelir.",
    )

    expense_columns = st.columns(5)
    expense_columns[0].metric("Ürün maliyeti", format_tl(financials["Ürün Maliyeti"]))
    expense_columns[1].metric("Personel gideri", format_tl(financials["Personel Gideri"]))
    expense_columns[2].metric("İşletme gideri", format_tl(financials["İşletme Gideri"]))
    expense_columns[3].metric("Tanıtım gideri", format_tl(financials["Tanıtım Gideri"]))
    expense_columns[4].metric("Toplam gider", format_tl(financials["Toplam Gider"]))

    with st.expander("Finansal varsayımlar ve terimler"):
        st.markdown(
            f"""
- **Aylık müşteri:** 2.700 temel müşteri + marka gücü farkı × 18 + erişilebilirlik farkı × 10 + ((tanıtım bütçesi − 20.000) / 5.000) × 40. Sonuç 0'ın altına düşmez.
- **Ortalama harcama:** 100 TL + (fiyat indeksi × 18 TL) + (kalite yatırımı × 2 TL).
- **Ciro:** aylık müşteri × ortalama harcama.
- **Ürün maliyeti:** ciro × (%32 + fiyat indeksi başına 1,5 yüzde puan).
- **Personel gideri:** 100.000 TL sabit varsayım + kalite yatırımı × 10.000 TL.
- **İşletme gideri:** 30.000 TL sabit varsayım + müşteri başına 5 TL.
- **Toplam gider:** ürün + personel + işletme + tanıtım giderleri.
- **Faaliyet sonucu:** ciro − toplam gider. Bu değer negatif olabilir ve olduğu gibi gösterilir.

**Ciro**, satışların toplam parasal değeridir. **Faaliyet sonucu**, olağan işletme gelir ve giderleri arasındaki farktır. Bütün tutarlar ve talep katsayıları eğitim için belirlenmiş varsayımlardır.
"""
        )

    history = st.session_state.simulation_history
    st.divider()
    st.subheader("Aylık simülasyon grafikleri")
    if not history:
        st.info("Aylık grafikler için B. Stratejik Kararlar bölümünde ‘Bir Ay İlerle’ seçeneğiyle ilk ayı kaydedin.")
    else:
        history_rows = []
        for month_record in history:
            history_rows.append(
                {
                    "Ay": f"Ay {month_record['month']}",
                    "Ciro": month_record["financials"]["Ciro"],
                    "Toplam Gider": month_record["financials"]["Toplam Gider"],
                    "Faaliyet Sonucu": month_record["financials"]["Faaliyet Sonucu"],
                    "Sonuç Türü": "Pozitif" if month_record["financials"]["Faaliyet Sonucu"] >= 0 else "Negatif",
                    "Marka Gücü": month_record["scores"]["Marka Gücü"],
                    "Toplumsal Erişilebilirlik": month_record["scores"]["Toplumsal Erişilebilirlik"],
                }
            )

        chart_left, chart_right = st.columns(2)
        with chart_left:
            revenue_chart = px.bar(
                history_rows,
                x="Ay",
                y=["Ciro", "Toplam Gider"],
                barmode="group",
                color_discrete_sequence=["#526b4b", "#b48b62"],
                labels={"value": "Tutar (TL)", "variable": "Kalem"},
            )
            revenue_chart.update_layout(
                title="Aylık ciro ve giderler",
                height=360,
                margin=dict(l=12, r=12, t=55, b=12),
                plot_bgcolor="#fffdf8",
                paper_bgcolor="#f7f5ef",
                legend_title=None,
            )
            st.plotly_chart(revenue_chart, width="stretch", config={"displayModeBar": False, "responsive": True})
        with chart_right:
            result_chart = px.bar(
                history_rows,
                x="Ay",
                y="Faaliyet Sonucu",
                color="Sonuç Türü",
                color_discrete_map={"Pozitif": "#526b4b", "Negatif": "#a4473d"},
                labels={"Faaliyet Sonucu": "Sonuç (TL)"},
            )
            result_chart.add_hline(y=0, line_dash="dot", line_color="#654735")
            result_chart.update_layout(
                title="Aylık faaliyet sonucu",
                height=360,
                margin=dict(l=12, r=12, t=55, b=12),
                plot_bgcolor="#fffdf8",
                paper_bgcolor="#f7f5ef",
                showlegend=False,
            )
            st.plotly_chart(result_chart, width="stretch", config={"displayModeBar": False, "responsive": True})

        brand_chart = px.line(
            history_rows,
            x="Ay",
            y=["Marka Gücü", "Toplumsal Erişilebilirlik"],
            markers=True,
            range_y=[0, 100],
            color_discrete_sequence=["#7c5942", "#526b4b"],
            labels={"value": "Puan (0-100)", "variable": "Gösterge"},
        )
        brand_chart.update_layout(
            title="Marka ve toplum göstergeleri",
            height=360,
            margin=dict(l=12, r=12, t=55, b=12),
            plot_bgcolor="#fffdf8",
            paper_bgcolor="#f7f5ef",
            legend_title=None,
        )
        st.plotly_chart(brand_chart, width="stretch", config={"displayModeBar": False, "responsive": True})

if active_view == "Strateji Danışmanı":
    st.subheader("Kural Tabanlı Strateji Danışmanı")
    st.caption("Gerçek bir yapay zekâ servisi kullanılmaz; öneriler seçtiğiniz kararlara göre kurallarla oluşturulur.")
    for recommendation in recommendations:
        st.info(recommendation, icon="💡")

    st.divider()
    st.subheader("Alternatif Stratejileri Karşılaştır")
    st.write("Mevcut fiyat, kalite ve bütçe kararları sabit tutularak üç konumlandırmanın puanları karşılaştırılır.")
    comparison_rows: list[dict[str, Any]] = []
    for alternative_name in STRATEGIES:
        alternative_scores = calculate_performance(alternative_name, price_index, quality, budget)
        alternative_financials = calculate_financials(
            price_index, quality, budget, alternative_scores
        )
        comparison_rows.append(
            {
                "Marka stratejisi": alternative_name,
                **alternative_scores,
                "Aylık müşteri": alternative_financials["Aylık Müşteri"],
                "Ciro": alternative_financials["Ciro"],
                "Toplam gider": alternative_financials["Toplam Gider"],
                "Faaliyet sonucu": alternative_financials["Faaliyet Sonucu"],
            }
        )
    comparison_display = []
    for row in comparison_rows:
        comparison_display.append(
            {
                **row,
                "Ciro": format_tl(row["Ciro"]),
                "Toplam gider": format_tl(row["Toplam gider"]),
                "Faaliyet sonucu": format_tl(row["Faaliyet sonucu"]),
            }
        )
    st.dataframe(comparison_display, hide_index=True, width="stretch")

    comparison_left, comparison_right = st.columns(2)
    with comparison_left:
        comparison_score_chart = px.bar(
            comparison_rows,
            x="Marka stratejisi",
            y=["Marka Gücü", "Toplumsal Erişilebilirlik"],
            barmode="group",
            range_y=[0, 100],
            color_discrete_sequence=["#7c5942", "#526b4b"],
            labels={"value": "Puan (0-100)", "variable": "Gösterge"},
        )
        comparison_score_chart.update_layout(
            title="Marka ve erişilebilirlik",
            height=360,
            margin=dict(l=12, r=12, t=55, b=12),
            plot_bgcolor="#fffdf8",
            paper_bgcolor="#f7f5ef",
            legend_title=None,
        )
        st.plotly_chart(comparison_score_chart, width="stretch", config={"displayModeBar": False, "responsive": True})
    with comparison_right:
        for row in comparison_rows:
            row["Sonuç türü"] = "Pozitif" if row["Faaliyet sonucu"] >= 0 else "Negatif"
        comparison_result_chart = px.bar(
            comparison_rows,
            x="Marka stratejisi",
            y="Faaliyet sonucu",
            color="Sonuç türü",
            color_discrete_map={"Pozitif": "#526b4b", "Negatif": "#a4473d"},
            labels={"Faaliyet sonucu": "Faaliyet sonucu (TL)"},
        )
        comparison_result_chart.add_hline(y=0, line_dash="dot", line_color="#654735")
        comparison_result_chart.update_layout(
            title="Stratejiye göre faaliyet sonucu",
            height=360,
            margin=dict(l=12, r=12, t=55, b=12),
            plot_bgcolor="#fffdf8",
            paper_bgcolor="#f7f5ef",
            showlegend=False,
        )
        st.plotly_chart(comparison_result_chart, width="stretch", config={"displayModeBar": False, "responsive": True})

    report = build_report(
        strategy_name, price_policy, quality, budget, scores, recommendations
    )
    st.download_button(
        "Strateji Raporunu İndir",
        data=report.encode("utf-8"),
        file_name="kent_kafe_strateji_raporu.txt",
        mime="text/plain; charset=utf-8",
        help="Kararlarınızı, puanları, formüllerin açıklamasını ve önerileri UTF-8 TXT olarak indirir.",
    )

st.caption("Tüm veriler eğitim amacıyla kullanılan varsayımsal verilerdir. Gerçek belediye verisi kullanılmamaktadır.")
