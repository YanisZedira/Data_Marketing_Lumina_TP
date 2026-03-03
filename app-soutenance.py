import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Lumina CMO Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

N="#0E1B2E"; N2="#1B2A4A"; N3="#243352"; A="#C9716E"; AL="#E8B4B1"
W="#FFFFFF"; G="#8A96A8"; GL="#C5CAD4"; GR="#2D9C6E"

if "lang" not in st.session_state:
    st.session_state.lang = "FR"
L = st.session_state.lang

T = {
"FR":{
    "lang_btn":"Switch to English",
    "title":"Tableau de Bord CMO",
    "sub":"48 553 clients · 1,8M transactions · 692 782 touchpoints · 2007–2011",
    "pbq":"Comment maximiser la valeur client alors que",
    "pbq2":"95% des efforts marketing traitent tout le monde pareil ?",
    "t1":"Segmentation Clients","t2":"Churn & CLV","t3":"Attribution Marketing",
    "pill1":"Q1 — SEGMENTATION","h1":"Qui sont nos clients — et pourquoi les traiter differemment ?","d1":"RFM scoring + K-Means K=5 · Silhouette=0.449 · 48 553 clients B2C",
    "kpi1":[("48 553","Clients analyses","Base B2C nettoyee"),("5","Segments K-Means","Silhouette 0.449"),("51,2%","CA par 5,5% des clients","Champions"),("468 EUR","Panier moyen A Risque","Plus eleve de la base"),("38,8%","Part clients Perdus","Seulement 5,4% du CA")],
    "slbl_seg":"TAILLE ET PART DU CA PAR SEGMENT",
    "radio_seg":["Part du CA (%)","Nombre de clients","Panier moyen (EUR)","Recence (j)"],
    "slbl_rev":"CONCENTRATION DU REVENU","slbl_obs":"OBSERVATIONS CLES",
    "ins1t":"5,5% genere 51,2% du CA","ins1b":"Champions : 27,7x/an, panier 181 EUR, tenure 606j. Coeur structurel du business.",
    "ins2t":"38,8% des clients = 5,4% du CA","ins2b":"Les Perdus sur-consomment les emails generiques sans retour mesurable.",
    "ins3t":"A Risque : panier 468 EUR — le plus eleve","ins3b":"Etaient des Champions. 273j de silence. Signal le plus urgent de la base.",
    "ins4t":"Opportunistes : potentiel sous-exploite","ins4b":"24,5% de la base, 18 categories. Migration vers Champions possible.",
    "reco1":"3 tracks distincts : VIP Champions / urgence A Risque / low-cost Perdus — lift >= 25%",
    "slbl_sc":"SCATTER RECENCY x MONETARY — QUI CIBLER EN PRIORITE ?",
    "sc_xlab":"Recence (j) — plus bas = plus recent","sc_ylab":"CA total client (EUR)","sc_vline":"Seuil churn P90=160j",
    "sc_l1":"Zone gauche (< 160j)","sc_l1b":"clients actifs",
    "sc_l2":"Zone droite (> 160j)","sc_l2b":"churnes ou en sortie",
    "sc_l3":"A Risque (rouge, droite)","sc_l3b":"valeur elevee + silence",
    "pill2":"Q2 — CHURN & CLV","h2":"Quels clients vont partir — et combien ca coute ?","d2":"Gradient Boosting ROC-AUC 0.70–0.80 · Seuil P90=160j · Zero data leakage",
    "kpi2_risk_lbl":"CA total a risque","kpi2_risk_sub":"%s du CA",
    "kpi2_rest":[("160j","Seuil churn P90","No purchase >160j = churned"),("0,70–0,80","ROC-AUC Gradient Boosting","Modele retenu"),("2 180","Clients A Risque","468 EUR · 15,3% CA"),(">8 000%","ROI simulation top 500","17 500 EUR → 1,5M EUR+")],
    "slbl_matrix":"MATRICE CLV x RISQUE CHURN","slbl_risk":"CA A RISQUE PAR SEGMENT",
    "q1l":"Q1 — PRIORITE #1","q2l":"Q2 — PROTEGER","q3l":"Q3 — LOW COST","q4l":"Q4 — SURVEILLER",
    "xchurn":"Probabilite de churn (0-10)","yclv":"Score CLV","xrisk":"CA a risque (EUR)",
    "slbl_drv":"DRIVERS DE CHURN",
    "drv_labels":["Recence","Tendance IPT","Dernier ecart/moy","Tendance panier","Mois inactifs 6m"],
    "drv_actions":["Alerte >120j","Trigger +20% ecart","Urgent si ratio >1.5","Offre si -20% panier","React apres 2 mois"],
    "slbl_act":"ACTIONS PRIORITAIRES","slbl_sim":"SIMULATEUR ROI — RETENTION Q1",
    "sim_s1":"Clients cibles","sim_s2":"Taux recuperation (%)","sim_budget":"Budget","sim_rev":"CA recupere","sim_roi":"ROI","sim_be":"Breakeven","sim_be_lbl":"BE",
    "reco2":"Top {nc} clients A Risque — {budget} EUR — {rev:.1f}M EUR a {taux}% — breakeven {be}%",
    "pill3":"Q3 — ATTRIBUTION","h3":"Ou fonctionne vraiment le budget marketing ?","d3":"692 782 touchpoints · 7 canaux · Markov removal effect · CVR 14,3%",
    "kpi3":[("14,3%","Taux conversion global","47 834 → 6 840"),("155j","Duree moyenne parcours","14,5 touchpoints / client"),("74,6%","Parcours > 30 jours","Goulot principal"),("27x","ROAS Display Markov","5,1% LT → 14,9% Markov"),("+9,8pp","Sous-credit Display & Social","Invisibles en last-touch")],
    "slbl_funnel":"FUNNEL DE CONVERSION — GOULOT D'ETRANGLEMENT",
    "funnel_stages":["Awareness","Multi-Touch (3+ canaux)","Long Journey (> 30j)","High Intent (10+ pts)","Conversion"],
    "funnel_xlab":"Nombre de clients","funnel_ann":"GOULOT D'ETRANGLEMENT\n74,6% parcours > 30j",
    "slbl_fi":"CE QUE LE FUNNEL REVELE",
    "btl_t":"74,6% des parcours > 30 jours","btl_b":"Un client est expose 155 jours, 14,5 touchpoints avant d'acheter. Crediter le dernier clic = ignorer 14 etapes sur 14,5.",
    "fi1t":"Display & Social : 28,6% des parcours","fi1b":"5% credit LT → 14,9% Markov. ROAS 27x et 16x sous-exploites.",
    "fi2t":"Email = fermeture, pas moteur","fi2b":"Position ~14 dans le parcours. 21,6% en LT. Role de cloture uniquement.",
    "fi3t":"Cout de l'erreur d'attribution","fi3b":"ROAS Display 27x invisible en LT. Budget massivement mal alloue.",
    "slbl_attr":"COMPARAISON MODELES D'ATTRIBUTION",
    "radio_attr":["Last-Touch","First-Touch","Linear","Tous les modeles"],"all_key":"Tous les modeles",
    "attr_xlab":"Attribution (%)","attr_clab":"Canal",
    "slbl_delta":"ECART MARKOV - LAST-TOUCH (pp)","delta_ylab":"Ecart Markov - LT (pp)",
    "ann_under":"Sous-credites","ann_over":"Sur-credites",
    "slbl_canal":"ANALYSE CANAL PAR CANAL","badge_u":"SOUS-CREDITE","badge_o":"SUR-CREDITE",
    "btl2_t":"Budget mal alloue","btl2_b":"Email+Direct+Retargeting sur-credites 7-8pp. Display+Social+Affiliate sous-credites ~10pp. 20% reallocation = +15 a 25% ROAS.",
    "reco3":"Adopter Markov + reallouer 20% Email+Direct vers Display+Social+Affiliates — ROAS +15 a +25%",
    "rec_lbl":"Recommandation","goulot_lbl":"Goulot —","tp_lbl":"touchpoints",
    "seg_names":["Perdus","Opportunistes","Fideles Engages","Champions","A Risque"],
    "footer1":"Lumina & Co — Data Marketing DIA3 · TP1-TP5","footer2":"UCI Online Retail II · 48 553 clients · 2007-2011",
},
"EN":{
    "lang_btn":"Passer en Francais",
    "title":"CMO Decision Dashboard",
    "sub":"48,553 clients · 1.8M transactions · 692,782 touchpoints · 2007–2011",
    "pbq":"How do we maximize customer value when",
    "pbq2":"95% of marketing efforts treat everyone the same?",
    "t1":"Client Segmentation","t2":"Churn & CLV","t3":"Marketing Attribution",
    "pill1":"Q1 — SEGMENTATION","h1":"Who are our clients — and why treat them differently?","d1":"RFM scoring + K-Means K=5 · Silhouette=0.449 · 48,553 B2C clients",
    "kpi1":[("48,553","Clients analysed","Cleaned B2C base"),("5","K-Means Segments","Silhouette 0.449"),("51.2%","Revenue by 5.5% of clients","Champions"),("EUR 468","Avg basket At Risk","Highest in database"),("38.8%","Lost clients share","Only 5.4% of revenue")],
    "slbl_seg":"SEGMENT SIZE AND REVENUE SHARE",
    "radio_seg":["Revenue share (%)","Number of clients","Avg basket (EUR)","Recency (days)"],
    "slbl_rev":"REVENUE CONCENTRATION","slbl_obs":"KEY OBSERVATIONS",
    "ins1t":"5.5% generates 51.2% of revenue","ins1b":"Champions: 27.7x/year, basket EUR 181, tenure 606d. Structural core of the business.",
    "ins2t":"38.8% of clients = 5.4% of revenue","ins2b":"Lost clients over-consume generic emails with no measurable return.",
    "ins3t":"At Risk: basket EUR 468 — the highest","ins3b":"Were Champions. 273 days of silence. Most urgent signal in the database.",
    "ins4t":"Opportunists: untapped potential","ins4b":"24.5% of the base, 18 categories. Migration to Champions achievable.",
    "reco1":"3 distinct tracks: VIP Champions / urgent At Risk / low-cost Lost — lift >= 25%",
    "slbl_sc":"SCATTER RECENCY x MONETARY — WHO TO TARGET FIRST?",
    "sc_xlab":"Recency (days) — lower = more recent","sc_ylab":"Total client revenue (EUR)","sc_vline":"Churn threshold P90=160d",
    "sc_l1":"Left zone (< 160d)","sc_l1b":"active clients",
    "sc_l2":"Right zone (> 160d)","sc_l2b":"churned or exiting",
    "sc_l3":"At Risk (red, right)","sc_l3b":"high value + silence",
    "pill2":"Q2 — CHURN & CLV","h2":"Which clients will leave — and what does it cost?","d2":"Gradient Boosting ROC-AUC 0.70–0.80 · P90 threshold=160d · Zero data leakage",
    "kpi2_risk_lbl":"Total revenue at risk","kpi2_risk_sub":"%s of total revenue",
    "kpi2_rest":[("160d","Churn threshold P90","No purchase >160d = churned"),("0.70–0.80","ROC-AUC Gradient Boosting","Selected model"),("2,180","At Risk clients","EUR 468 · 15.3% rev"),(">8,000%","ROI sim. top 500","EUR 17,500 → EUR 1.5M+")],
    "slbl_matrix":"CLV x CHURN RISK MATRIX","slbl_risk":"REVENUE AT RISK BY SEGMENT",
    "q1l":"Q1 — PRIORITY #1","q2l":"Q2 — PROTECT","q3l":"Q3 — LOW COST","q4l":"Q4 — MONITOR",
    "xchurn":"Churn probability (0-10)","yclv":"CLV score","xrisk":"Revenue at risk (EUR)",
    "slbl_drv":"CHURN DRIVERS",
    "drv_labels":["Recency","IPT trend","Last gap vs avg","Basket trend","Inactive months 6m"],
    "drv_actions":["Alert >120d","Trigger +20% gap","Urgent if ratio >1.5","Offer if -20% basket","React after 2 months"],
    "slbl_act":"PRIORITY ACTIONS","slbl_sim":"ROI SIMULATOR — Q1 RETENTION",
    "sim_s1":"Targeted clients","sim_s2":"Recovery rate (%)","sim_budget":"Budget","sim_rev":"Revenue recovered","sim_roi":"ROI","sim_be":"Breakeven","sim_be_lbl":"BE",
    "reco2":"Top {nc} At Risk clients — EUR {budget} — EUR {rev:.1f}M at {taux}% — breakeven {be}%",
    "pill3":"Q3 — ATTRIBUTION","h3":"Where does the marketing budget actually work?","d3":"692,782 touchpoints · 7 channels · Markov removal effect · CVR 14.3%",
    "kpi3":[("14.3%","Global conversion rate","47,834 → 6,840"),("155d","Avg journey length","14.5 touchpoints / client"),("74.6%","Journeys > 30 days","Main bottleneck"),("27x","Display ROAS Markov","5.1% LT → 14.9% Markov"),("+9.8pp","Display & Social under-credited","Invisible in last-touch")],
    "slbl_funnel":"CONVERSION FUNNEL — BOTTLENECK",
    "funnel_stages":["Awareness","Multi-Touch (3+ channels)","Long Journey (> 30d)","High Intent (10+ pts)","Conversion"],
    "funnel_xlab":"Number of clients","funnel_ann":"BOTTLENECK\n74.6% journeys > 30d",
    "slbl_fi":"WHAT THE FUNNEL REVEALS",
    "btl_t":"74.6% of journeys > 30 days","btl_b":"A client is exposed for 155 days, 14.5 touchpoints before buying. Crediting last click = ignoring 14 out of 14.5 steps.",
    "fi1t":"Display & Social start 28.6% of journeys","fi1b":"5% LT credit → 14.9% Markov. ROAS 27x and 16x under-exploited.",
    "fi2t":"Email = closing, not engine","fi2b":"Position ~14 in journey. Gets 21.6% in LT. Closing role only.",
    "fi3t":"Cost of attribution error","fi3b":"Display ROAS 27x invisible in LT. Budget massively misallocated.",
    "slbl_attr":"ATTRIBUTION MODEL COMPARISON",
    "radio_attr":["Last-Touch","First-Touch","Linear","All models"],"all_key":"All models",
    "attr_xlab":"Attribution (%)","attr_clab":"Channel",
    "slbl_delta":"MARKOV - LAST-TOUCH GAP (pp)","delta_ylab":"Markov - LT gap (pp)",
    "ann_under":"Under-credited","ann_over":"Over-credited",
    "slbl_canal":"CHANNEL-BY-CHANNEL ANALYSIS","badge_u":"UNDER-CREDITED","badge_o":"OVER-CREDITED",
    "btl2_t":"Misallocated budget","btl2_b":"Email+Direct+Retargeting over-credited 7-8pp. Display+Social+Affiliate under-credited ~10pp. 20% reallocation = +15 to 25% ROAS.",
    "reco3":"Adopt Markov + reallocate 20% Email+Direct to Display+Social+Affiliates — ROAS +15 to +25%",
    "rec_lbl":"Recommendation","goulot_lbl":"Bottleneck —","tp_lbl":"touchpoints",
    "seg_names":["Lost","Opportunists","Engaged Loyals","Champions","At Risk"],
    "footer1":"Lumina & Co — Data Marketing DIA3 · TP1-TP5","footer2":"UCI Online Retail II · 48,553 clients · 2007-2011",
}}

tx = T[L]

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');
*{{font-family:'DM Sans',sans-serif!important}}
.main,.main .block-container{{background:{N}!important;padding:0 2rem 2rem!important;max-width:1500px!important}}
[data-testid=stAppViewContainer]{{background:{N}!important}}
[data-testid=stHeader]{{background:{N}!important}}
[data-baseweb=tab-list]{{background:{N2}!important;border-bottom:2px solid {A}!important;gap:0!important;padding:0!important;border-radius:0!important}}
[data-baseweb=tab]{{background:transparent!important;color:{G}!important;font-size:.82rem!important;font-weight:600!important;letter-spacing:.1em!important;text-transform:uppercase!important;padding:.7rem 1.8rem!important;border:none!important;border-radius:0!important}}
[data-baseweb=tab]:hover{{color:{W}!important;background:{N3}!important}}
[aria-selected=true][data-baseweb=tab]{{background:{A}!important;color:{W}!important}}
[data-baseweb=tab-highlight],[data-baseweb=tab-border]{{display:none!important}}
[data-baseweb=select]>div{{background:{N2}!important;border:1px solid #2A3A5A!important;border-radius:3px!important;color:{W}!important}}
[data-baseweb=option]{{background:{N2}!important;color:{W}!important}}
.stSelectbox label,.stSlider label,.stRadio label,.stRadio div,.stSlider div{{color:{G}!important;font-size:.8rem!important}}
[data-baseweb=radio] span{{background:{A}!important;border-color:{A}!important}}
[data-testid=metric-container]{{background:{N2}!important;border-top:3px solid {A}!important;border-radius:4px!important;padding:1rem 1.2rem!important}}
[data-testid=stMetricLabel]{{color:{G}!important;font-size:.72rem!important;text-transform:uppercase!important;letter-spacing:.08em!important}}
[data-testid=stMetricValue]{{color:{W}!important;font-family:'DM Serif Display',serif!important;font-size:2rem!important}}
[data-testid=stMetricDelta]{{display:none!important}}
section[data-testid=stSidebar]{{background:{N2}!important;border-right:1px solid #2A3A5A!important;min-width:200px!important;max-width:220px!important}}
section[data-testid=stSidebar] .stButton button{{background:{A}!important;color:{W}!important;border:none!important;border-radius:4px!important;font-weight:700!important;font-size:.85rem!important;letter-spacing:.08em!important;width:100%!important;padding:.6rem 1rem!important;margin-top:.5rem!important}}
section[data-testid=stSidebar] .stButton button:hover{{background:#B5605D!important}}
#MainMenu,footer{{visibility:hidden}}
.stDeployButton,div[data-testid=stToolbar]{{display:none}}
</style>""", unsafe_allow_html=True)

# ── SIDEBAR (langue) ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:1.5rem 0 1rem;">
        <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:{W};">Lumina <span style="color:{A};">&</span> Co</div>
        <div style="font-size:.72rem;color:{G};margin-top:.3rem;">{tx['title']}</div>
    </div>
    <hr style="border:none;border-top:1px solid #2A3A5A;margin:.5rem 0 1rem;">
    <div style="font-size:.65rem;color:{G};text-transform:uppercase;letter-spacing:.12em;margin-bottom:.5rem;">Langue / Language</div>
    """, unsafe_allow_html=True)

    if st.button(tx["lang_btn"], key="lang_btn"):
        st.session_state.lang = "EN" if L == "FR" else "FR"
        st.rerun()

    st.markdown(f"""
    <hr style="border:none;border-top:1px solid #2A3A5A;margin:1.2rem 0;">
    <div style="font-size:.65rem;color:{G};text-transform:uppercase;letter-spacing:.12em;margin-bottom:.8rem;">Donnees</div>
    <div style="font-size:.78rem;color:{GL};line-height:1.9;">
        48 553 clients<br>1,8M transactions<br>692 782 touchpoints<br>7 canaux<br>2007–2011
    </div>
    <hr style="border:none;border-top:1px solid #2A3A5A;margin:1.2rem 0;">
    <div style="font-size:.65rem;color:{G};line-height:1.7;">TP1 · TP2 · TP3 · TP4 · TP5<br>UCI Online Retail II</div>
    """, unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
sn = tx["seg_names"]
SEGS = pd.DataFrame({
    "name":sn,"n":[18846,11874,12979,2674,2180],
    "pct_base":[38.8,24.5,26.7,5.5,4.5],"pct_ca":[5.4,23.8,4.3,51.2,15.3],
    "recency":[676,185,141,61,273],"frequency":[1.7,8.2,2.3,27.7,4.5],
    "monetary":[72,507,85,4842,1773],"basket":[40.2,60.5,35.2,181.5,468.5],
    "churn_prob":[0.95,0.35,0.22,0.08,0.82],"clv_score":[1,3,2,5,4],
    "color":["#8A96A8","#4A6FA5","#6B8CAE","#C9716E","#B85A57"],
})
SEGS["ca_total"]=(SEGS["n"]*SEGS["monetary"]).round(0)
SEGS["ca_at_risk"]=(SEGS["churn_prob"]*SEGS["ca_total"]).round(0)
ca_tot=int(SEGS["ca_total"].sum()); ca_risk=int(SEGS["ca_at_risk"].sum())

ATTR = pd.DataFrame({
    "channel":["Display","Social","Affiliate","Email","Retargeting","Direct","Search Paid"],
    "last_touch":[5.12,5.07,4.96,21.64,22.03,20.61,20.56],
    "first_touch":[29.8,28.6,28.4,4.2,3.1,3.4,2.5],
    "linear":[14.8,14.5,14.3,14.4,14.1,14.2,13.7],
    "markov":[14.87,14.87,14.85,14.79,14.78,12.92,12.91],
    "roas":[27,16,15,8,7,5,4],
    "touchpoints":[54131,54049,53772,13709,13582,24777,24693],
    "role":["Awareness","Awareness","Awareness","Conversion","Conversion","Conversion","Conversion"],
    "color":["#C9716E","#B85A57","#A5524F","#8A96A8","#C5CAD4","#5A6A82","#4A5A72"],
})
ATTR["delta"]=ATTR["markov"]-ATTR["last_touch"]

fn_stages=tx["funnel_stages"]
fn_n=[47834,37310,20100,13400,6840]
fn_pct=[100.,78.,42.,28.,14.3]
fn_bn=[False,False,True,False,False]

CHURN=pd.DataFrame({
    "label":tx["drv_labels"],"imp":[100,82,65,50,38],"action":tx["drv_actions"]
})

# ── HELPERS ───────────────────────────────────────────────────────────────────
def bl(fig, h=380):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=W, size=12),
        height=h, margin=dict(l=8,r=8,t=32,b=8),
        legend=dict(bgcolor=N2, bordercolor="#2A3A5A", borderwidth=1, font=dict(size=11,color=G)),
        hoverlabel=dict(bgcolor=N2, bordercolor=A, font=dict(family="DM Sans",size=12,color=W))
    )
    fig.update_xaxes(gridcolor="#1E2E48", linecolor="#2A3A5A", tickfont=dict(color=G,size=11), zeroline=False)
    fig.update_yaxes(gridcolor="#1E2E48", linecolor="#2A3A5A", tickfont=dict(color=G,size=11), zeroline=False)
    return fig

def pc(fig): st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

def slbl(t):
    st.markdown(f'<div style="font-size:.63rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:{G};border-bottom:1px solid #1E2E48;padding-bottom:.3rem;margin-bottom:.7rem;">{t}</div>', unsafe_allow_html=True)

def ins(title, body, hi=False):
    bg=A if hi else N3; tc="rgba(255,255,255,.8)" if hi else G
    st.markdown(f'<div style="background:{bg};border-left:3px solid {A};border-radius:0 4px 4px 0;padding:.7rem 1rem;margin-bottom:.5rem;box-shadow:0 2px 8px rgba(0,0,0,.15);"><b style="font-size:.88rem;color:{W};">{title}</b><div style="font-size:.79rem;color:{tc};line-height:1.5;margin-top:.15rem;">{body}</div></div>', unsafe_allow_html=True)

def reco(t):
    st.markdown(f'<div style="background:{A};border-radius:4px;padding:.9rem 1.2rem;margin-top:.9rem;box-shadow:0 4px 20px rgba(201,113,110,.3);"><div style="font-size:.58rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:.3rem;">{tx["rec_lbl"]}</div><div style="font-size:.95rem;font-weight:600;color:{W};line-height:1.45;">{t}</div></div>', unsafe_allow_html=True)

def btl(title, body):
    st.markdown(f'<div style="background:rgba(201,113,110,.08);border:1.5px solid {A};border-radius:4px;padding:.85rem 1rem;margin:.7rem 0;"><div style="color:{A};font-weight:700;font-size:.78rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.25rem;">{tx["goulot_lbl"]} {title}</div><div style="color:{AL};font-size:.8rem;line-height:1.5;">{body}</div></div>', unsafe_allow_html=True)

def kpis(items):
    cols=st.columns(len(items))
    for c,(v,l,s) in zip(cols,items):
        sub=f'<div style="font-size:.74rem;color:{AL};margin-top:.2rem;">{s}</div>' if s else ""
        c.markdown(f'<div style="background:{N2};border-top:3px solid {A};border-radius:4px;padding:1rem 1.15rem;margin-bottom:.4rem;box-shadow:0 4px 20px rgba(0,0,0,.22);"><div style="font-family:\'DM Serif Display\',serif;font-size:2rem;color:{W};line-height:1;">{v}</div><div style="font-size:.67rem;color:{G};text-transform:uppercase;letter-spacing:.09em;margin-top:.2rem;">{l}</div>{sub}</div>', unsafe_allow_html=True)

def phdr(pill, title, desc):
    st.markdown(f'<div style="padding:1.2rem 0 .7rem;"><div style="background:{A};display:inline-block;padding:3px 14px;border-radius:2px;font-size:.66rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:#fff;margin-bottom:.55rem;">{pill}</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.75rem;color:{W};line-height:1.2;margin-bottom:.2rem;">{title}</div><div style="font-size:.8rem;color:{G};line-height:1.55;">{desc}</div></div>', unsafe_allow_html=True)

# ── TOP BAR ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{N2};border-bottom:3px solid {A};padding:.85rem 0 .85rem 0;margin-bottom:.5rem;display:flex;align-items:center;justify-content:space-between;">
    <div>
        <span style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:{W};">Lumina <span style="color:{A};">&</span> Co</span>
        <span style="color:{G};font-size:.76rem;margin-left:1rem;">{tx['title']}</span>
    </div>
    <div style="font-size:.7rem;color:{G};">{tx['sub']}</div>
</div>
<div style="background:{N2};padding:.5rem 0;margin-bottom:.9rem;border-bottom:1px solid #1E2E48;">
    <span style="font-family:'DM Serif Display',serif;font-size:.98rem;color:{W};font-style:italic;">{tx['pbq']} </span>
    <span style="font-family:'DM Serif Display',serif;font-size:.98rem;color:{A};font-style:italic;">{tx['pbq2']}</span>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
t1, t2, t3 = st.tabs([tx["t1"], tx["t2"], tx["t3"]])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SEGMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
with t1:
    phdr(tx["pill1"], tx["h1"], tx["d1"])
    kpis(tx["kpi1"])
    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)
    cl, cr = st.columns([3,2], gap="large")

    with cl:
        slbl(tx["slbl_seg"])
        view = st.radio("", tx["radio_seg"], horizontal=True, key="sv")
        ck_map = {tx["radio_seg"][0]:"pct_ca", tx["radio_seg"][1]:"n", tx["radio_seg"][2]:"basket", tx["radio_seg"][3]:"recency"}
        ck = ck_map.get(view, "pct_ca")

        f1 = go.Figure()
        for _, r in SEGS.sort_values(ck, ascending=True).iterrows():
            f1.add_trace(go.Bar(x=[r[ck]], y=[r["name"]], orientation="h",
                marker=dict(color=r["color"], opacity=.9, line=dict(color=N,width=.5)),
                text=[f"  {r[ck]:,.1f}"], textposition="inside", textfont=dict(color=W,size=11),
                showlegend=False, hovertemplate=f"<b>{r['name']}</b><br>N: {r['n']:,}<br>CA: {r['pct_ca']}%<extra></extra>"))
        bl(f1, 275)
        f1.update_layout(bargap=.32, showlegend=False)
        pc(f1)

        slbl(tx["slbl_rev"])
        f2 = go.Figure(data=[go.Pie(
            labels=SEGS["name"], values=SEGS["pct_ca"], hole=.58,
            marker=dict(colors=SEGS["color"].tolist(), line=dict(color=N,width=2.5)),
            textinfo="label+percent", textfont=dict(size=11,color=W),
            hovertemplate="<b>%{label}</b><br>%{value}%<br>N: %{customdata:,}<extra></extra>",
            customdata=SEGS["n"])])
        f2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans",color=W),
            height=265, margin=dict(l=0,r=0,t=8,b=0),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11,color=G), orientation="h", y=-.1),
            annotations=[dict(text="<b>CA</b>", x=.5, y=.5, font=dict(size=17,color=W,family="DM Serif Display"), showarrow=False)])
        pc(f2)

    with cr:
        slbl(tx["slbl_obs"])
        ins(tx["ins1t"], tx["ins1b"], hi=True)
        ins(tx["ins2t"], tx["ins2b"])
        ins(tx["ins3t"], tx["ins3b"])
        ins(tx["ins4t"], tx["ins4b"])
        reco(tx["reco1"])

    st.markdown("<div style='margin-top:1.6rem'></div>", unsafe_allow_html=True)
    slbl(tx["slbl_sc"])
    np.random.seed(42)
    pts = []
    for _, seg in SEGS.iterrows():
        n2 = min(seg["n"], 200)
        pts.append(pd.DataFrame({
            "rec": np.random.normal(seg["recency"], seg["recency"]*.22, n2).clip(1,900),
            "mon": np.random.lognormal(np.log(max(seg["monetary"],10)), .55, n2).clip(1,15000),
            "seg": seg["name"], "col": seg["color"]
        }))
    df_sc = pd.concat(pts, ignore_index=True)
    f3 = go.Figure()
    for _, seg in SEGS.iterrows():
        d = df_sc[df_sc["seg"]==seg["name"]]
        f3.add_trace(go.Scatter(x=d["rec"], y=d["mon"], mode="markers",
            marker=dict(size=5, color=seg["color"], opacity=.62, line=dict(color=N,width=.2)),
            name=seg["name"], hovertemplate=f"<b>{seg['name']}</b><br>EUR %{{y:,.0f}}<extra></extra>"))
    f3.add_vline(x=160, line_dash="dash", line_color=A, line_width=1.5,
        annotation_text=tx["sc_vline"], annotation_font_color=A, annotation_font_size=10, annotation_position="top right")
    f3.add_vrect(x0=0, x1=160, fillcolor="rgba(201,113,110,.04)", line_width=0)
    f3.add_vrect(x0=160, x1=900, fillcolor="rgba(138,150,168,.04)", line_width=0)
    bl(f3, 340)
    f3.update_layout(xaxis=dict(title=tx["sc_xlab"], range=[0,850]), yaxis=dict(title=tx["sc_ylab"], type="log"), legend=dict(orientation="h", y=1.06))
    pc(f3)
    st.markdown(f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem;margin-top:.3rem;">'
        f'<div style="background:{N2};border-left:3px solid {A};padding:.6rem .9rem;border-radius:0 4px 4px 0;font-size:.78rem;color:{G};"><b style="color:{W};">{tx["sc_l1"]}</b> — {tx["sc_l1b"]}</div>'
        f'<div style="background:{N2};border-left:3px solid {G};padding:.6rem .9rem;border-radius:0 4px 4px 0;font-size:.78rem;color:{G};"><b style="color:{W};">{tx["sc_l2"]}</b> — {tx["sc_l2b"]}</div>'
        f'<div style="background:{N2};border-left:3px solid {AL};padding:.6rem .9rem;border-radius:0 4px 4px 0;font-size:.78rem;color:{G};"><b style="color:{W};">{tx["sc_l3"]}</b> — {tx["sc_l3b"]}</div>'
        f'</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CHURN & CLV
# ═══════════════════════════════════════════════════════════════════════════════
with t2:
    phdr(tx["pill2"], tx["h2"], tx["d2"])
    kpi2_all = [(f'EUR {ca_risk/1e6:.1f}M', tx["kpi2_risk_lbl"], tx["kpi2_risk_sub"] % f'{ca_risk/ca_tot*100:.1f}%')] + list(tx["kpi2_rest"])
    kpis(kpi2_all)
    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)
    ca, cb = st.columns([3,2], gap="large")

    with ca:
        slbl(tx["slbl_matrix"])
        f4 = go.Figure()
        for _, seg in SEGS.iterrows():
            sz = (seg["n"]/SEGS["n"].max())*52+12
            is_key = seg["name"] in [sn[3], sn[4]]
            f4.add_trace(go.Scatter(
                x=[seg["churn_prob"]*10], y=[seg["clv_score"]*1.8],
                mode="markers+text",
                marker=dict(size=sz, color=seg["color"], opacity=.88, line=dict(color=W, width=1.5 if is_key else .5)),
                text=[seg["name"]], textposition="top center", textfont=dict(size=10,color=W),
                showlegend=False,
                hovertemplate=f"<b>{seg['name']}</b><br>Churn: {seg['churn_prob']*100:.0f}%<br>CLV: {seg['clv_score']}/5<br>N: {seg['n']:,}<br>EUR {seg['ca_at_risk']:,.0f}<extra></extra>"))
        bl(f4, 340)
        f4.update_layout(xaxis=dict(title=tx["xchurn"], range=[0,11]), yaxis=dict(title=tx["yclv"], range=[0,10.5]))
        for x,y,t,tc in [(2.5,10.,tx["q2l"],G),(7.5,10.,tx["q1l"],A),(2.5,.4,tx["q4l"],G),(7.5,.4,tx["q3l"],G)]:
            f4.add_annotation(x=x, y=y, text=t, showarrow=False, font=dict(color=tc,size=9), bgcolor=N2)
        f4.add_vline(x=5, line_dash="dash", line_color=G, line_width=1, opacity=.3)
        f4.add_hline(y=5.5, line_dash="dash", line_color=G, line_width=1, opacity=.3)
        pc(f4)

        slbl(tx["slbl_risk"])
        f5 = go.Figure()
        for _, row in SEGS.sort_values("ca_at_risk", ascending=True).iterrows():
            f5.add_trace(go.Bar(x=[row["ca_at_risk"]], y=[row["name"]], orientation="h",
                marker=dict(color=row["color"], opacity=.9, line=dict(color=N,width=.4)),
                text=[f"  EUR {row['ca_at_risk']/1e6:.2f}M ({row['churn_prob']*100:.0f}% churn)"],
                textposition="inside", textfont=dict(color=W,size=10), showlegend=False,
                hovertemplate=f"<b>{row['name']}</b><br>EUR {row['ca_at_risk']:,.0f}<extra></extra>"))
        bl(f5, 220)
        f5.update_layout(xaxis=dict(title=tx["xrisk"]), bargap=.3)
        pc(f5)

    with cb:
        slbl(tx["slbl_drv"])
        f6 = go.Figure()
        for i, row in CHURN.iterrows():
            f6.add_trace(go.Bar(x=[row["imp"]], y=[row["label"]], orientation="h",
                marker=dict(color=A, opacity=1-.1*i, line=dict(color=N,width=.4)),
                text=[f"  {row['imp']}%"], textposition="inside", textfont=dict(color=W,size=11),
                showlegend=False, hovertemplate=f"<b>{row['label']}</b><br>{row['action']}<extra></extra>"))
        bl(f6, 235)
        f6.update_layout(xaxis=dict(title="Importance (%)", range=[0,120]), yaxis=dict(autorange="reversed"), bargap=.28)
        pc(f6)

        slbl(tx["slbl_act"])
        for _, row in CHURN.iterrows():
            st.markdown(f'<div style="background:{N2};border-left:3px solid {A};border-radius:0 4px 4px 0;padding:.5rem .85rem;margin-bottom:.38rem;"><b style="font-size:.84rem;color:{W};">{row["label"]}</b><div style="font-size:.73rem;color:{G};margin-top:.1rem;">{row["action"]}</div></div>', unsafe_allow_html=True)

        slbl(tx["slbl_sim"])
        nc = st.slider(tx["sim_s1"], 50, 2180, 500, 50)
        taux = st.slider(tx["sim_s2"], 1, 40, 10, 1)
        budget = nc*35; rev = nc*30000*(taux/100); roi_v = ((rev-budget)/budget)*100
        be = next((r for r in range(1,51) if nc*30000*(r/100)>=budget), None)
        st.markdown(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin-top:.35rem;">'
            f'<div style="background:{N2};border-top:2px solid {A};border-radius:4px;padding:.7rem .95rem;"><div style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">EUR {budget:,}</div><div style="font-size:.67rem;color:{G};text-transform:uppercase;">{tx["sim_budget"]}</div></div>'
            f'<div style="background:{N2};border-top:2px solid {GR};border-radius:4px;padding:.7rem .95rem;"><div style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">EUR {rev/1e6:.2f}M</div><div style="font-size:.67rem;color:{G};text-transform:uppercase;">{tx["sim_rev"]}</div></div>'
            f'<div style="background:{N2};border-top:2px solid {A};border-radius:4px;padding:.7rem .95rem;"><div style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">{roi_v:,.0f}%</div><div style="font-size:.67rem;color:{G};text-transform:uppercase;">{tx["sim_roi"]}</div></div>'
            f'<div style="background:{N2};border-top:2px solid {AL};border-radius:4px;padding:.7rem .95rem;"><div style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">{be}%</div><div style="font-size:.67rem;color:{G};text-transform:uppercase;">{tx["sim_be"]}</div></div>'
            f'</div>', unsafe_allow_html=True)
        rates = np.arange(1,41); rois2 = [((nc*30000*(r/100)-budget)/budget)*100 for r in rates]
        f7 = go.Figure()
        f7.add_trace(go.Scatter(x=rates, y=rois2, mode="lines", line=dict(color=A,width=2.5),
            fill="tozeroy", fillcolor="rgba(201,113,110,.08)", showlegend=False))
        f7.add_vline(x=taux, line_dash="dash", line_color=W, opacity=.4)
        if be: f7.add_vline(x=be, line_dash="dot", line_color=GR, opacity=.8,
            annotation_text=f"{tx['sim_be_lbl']} {be}%", annotation_font_color=GR, annotation_font_size=9)
        f7.add_hline(y=0, line_color=G, opacity=.3)
        bl(f7, 185)
        f7.update_layout(yaxis=dict(title="ROI (%)"), xaxis=dict(title=tx["sim_s2"]), margin=dict(l=8,r=8,t=8,b=8))
        pc(f7)
        reco(tx["reco2"].format(nc=nc, budget=f"{budget:,}", rev=rev/1e6, taux=taux, be=be))

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ATTRIBUTION
# ═══════════════════════════════════════════════════════════════════════════════
with t3:
    phdr(tx["pill3"], tx["h3"], tx["d3"])
    kpis(tx["kpi3"])
    st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)

    slbl(tx["slbl_funnel"])
    cf, cfi = st.columns([3,2], gap="large")

    with cf:
        f8 = go.Figure()
        for i in range(5):
            bn = fn_bn[i]
            f8.add_trace(go.Bar(
                x=[fn_n[i]], y=[fn_stages[i]], orientation="h",
                marker=dict(color=A if bn else ("#4A6FA5" if i>0 else G),
                    opacity=1. if bn else .76,
                    line=dict(color=W if bn else N, width=2.5 if bn else .4)),
                text=[f"  {fn_n[i]:,}   ({fn_pct[i]:.1f}%)"],
                textposition="inside", textfont=dict(color=W, size=12 if bn else 11),
                showlegend=False, name=fn_stages[i],
                hovertemplate=f"<b>{fn_stages[i]}</b><br>N: {fn_n[i]:,}<br>{fn_pct[i]:.1f}%<extra></extra>",
                width=.62))
        bl(f8, 340)
        f8.update_layout(
            xaxis=dict(title=tx["funnel_xlab"], range=[0,55000]),
            yaxis=dict(autorange="reversed", tickfont=dict(size=11.5)),
            bargap=.32)
        f8.add_annotation(
            x=21000, y=fn_stages[2],
            text=tx["funnel_ann"],
            showarrow=True, arrowhead=2, arrowcolor=A, arrowwidth=2.5, ax=110, ay=-42,
            font=dict(color=W, size=10), bgcolor=N2, bordercolor=A, borderwidth=1.5, borderpad=5)
        for i in range(4):
            f8.add_annotation(x=fn_n[i+1]+1600, y=i+.5,
                text=f"-{fn_pct[i]-fn_pct[i+1]:.1f}pp", showarrow=False,
                font=dict(color=AL, size=9.5))
        pc(f8)

    with cfi:
        slbl(tx["slbl_fi"])
        btl(tx["btl_t"], tx["btl_b"])
        ins(tx["fi1t"], tx["fi1b"])
        ins(tx["fi2t"], tx["fi2b"])
        ins(tx["fi3t"], tx["fi3b"])

    st.markdown("<div style='margin-top:1.8rem'></div>", unsafe_allow_html=True)
    slbl(tx["slbl_attr"])
    cc1, cc2 = st.columns([3,2], gap="large")

    with cc1:
        msel = st.radio("", tx["radio_attr"], horizontal=True, key="am")
        mcols = {"Last-Touch":"last_touch","First-Touch":"first_touch","Linear":"linear"}
        das = ATTR.sort_values("markov", ascending=True)
        if msel == tx["all_key"]:
            f9 = go.Figure()
            for mn,mc,mcol in [("Last-Touch","last_touch",G),("First-Touch","first_touch","#4A6FA5"),("Linear","linear",GL),("Markov","markov",A)]:
                f9.add_trace(go.Bar(x=das["channel"], y=das[mc], name=mn,
                    marker=dict(color=mcol, opacity=.88, line=dict(color=N,width=.3)),
                    hovertemplate=f"<b>%{{x}}</b><br>{mn}: %{{y:.1f}}%<extra></extra>"))
            bl(f9, 340)
            f9.update_layout(barmode="group", bargap=.15, bargroupgap=.05,
                xaxis=dict(title=tx["attr_clab"]), yaxis=dict(title=tx["attr_xlab"]),
                legend=dict(orientation="h", y=1.06))
        else:
            cc = mcols.get(msel, "last_touch")
            ccol = G if msel=="Last-Touch" else ("#4A6FA5" if msel=="First-Touch" else GL)
            f9 = go.Figure()
            f9.add_trace(go.Bar(y=das["channel"], x=das[cc], orientation="h", name=msel,
                marker=dict(color=ccol, opacity=.7, line=dict(color=N,width=.3)),
                text=[f"{v:.1f}%" for v in das[cc]], textposition="outside", textfont=dict(color=G,size=10),
                hovertemplate=f"<b>%{{y}}</b><br>{msel}: %{{x:.1f}}%<extra></extra>"))
            f9.add_trace(go.Bar(y=das["channel"], x=das["markov"], orientation="h", name="Markov",
                marker=dict(color=A, opacity=.92, line=dict(color=N,width=.3)),
                text=[f"{v:.1f}%" for v in das["markov"]], textposition="outside", textfont=dict(color=AL,size=10),
                hovertemplate="<b>%{y}</b><br>Markov: %{x:.1f}%<extra></extra>"))
            bl(f9, 320)
            f9.update_layout(barmode="group", bargap=.22, bargroupgap=.06,
                xaxis=dict(title=tx["attr_xlab"], range=[0,38]),
                legend=dict(orientation="h", y=1.06))
        pc(f9)

        slbl(tx["slbl_delta"])
        dd = ATTR.sort_values("delta")
        f10 = go.Figure()
        f10.add_trace(go.Bar(x=dd["channel"], y=dd["delta"],
            marker=dict(color=[A if d>0 else "#5A6A82" for d in dd["delta"]], opacity=.9, line=dict(color=N,width=.4)),
            text=[f"{d:+.1f}pp" for d in dd["delta"]], textposition="outside",
            textfont=dict(color=[AL if d>0 else G for d in dd["delta"]], size=11),
            showlegend=False, hovertemplate="<b>%{x}</b><br>%{y:+.2f}pp<extra></extra>"))
        f10.add_hline(y=0, line_color=G, opacity=.4, line_width=1)
        f10.add_annotation(x=.8, y=11, text=tx["ann_under"], showarrow=False, font=dict(color=A,size=10), bgcolor=N2)
        f10.add_annotation(x=4.8, y=-9, text=tx["ann_over"], showarrow=False, font=dict(color=G,size=10), bgcolor=N2)
        bl(f10, 230)
        f10.update_layout(yaxis=dict(title=tx["delta_ylab"]), margin=dict(t=18))
        pc(f10)

    with cc2:
        slbl(tx["slbl_canal"])
        for _, row in ATTR.sort_values("delta", ascending=False).iterrows():
            ih = row["delta"] > 0
            bc2 = A if ih else "#3A4A62"
            ds = f"+{row['delta']:.1f}pp" if ih else f"{row['delta']:.1f}pp"
            badge = tx["badge_u"] if ih else tx["badge_o"]
            st.markdown(
                f'<div style="background:{N2};border-left:3px solid {bc2};border-radius:0 4px 4px 0;padding:.6rem .9rem;margin-bottom:.4rem;box-shadow:0 2px 8px rgba(0,0,0,.12);">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.12rem;">'
                f'<b style="font-size:.9rem;color:{W};">{row["channel"]}</b>'
                f'<span style="font-size:.59rem;font-weight:700;color:{A if ih else G};letter-spacing:.1em;">{badge}</span></div>'
                f'<div style="display:flex;gap:.7rem;font-size:.76rem;color:{G};">'
                f'<span>LT: <b style="color:{W};">{row["last_touch"]:.1f}%</b></span>'
                f'<span>MK: <b style="color:{A if ih else W};">{row["markov"]:.1f}%</b></span>'
                f'<span style="color:{A if ih else G};font-weight:600;">{ds}</span>'
                f'<span style="color:{A if ih else G};">ROAS {row["roas"]}x</span></div>'
                f'<div style="font-size:.71rem;color:{G};margin-top:.1rem;">{row["touchpoints"]:,} {tx["tp_lbl"]} · {row["role"]}</div>'
                f'</div>', unsafe_allow_html=True)
        btl(tx["btl2_t"], tx["btl2_b"])
        reco(tx["reco3"])

    st.markdown(
        f'<div style="margin-top:2rem;padding:.8rem 0;border-top:1px solid #1E2E48;display:flex;justify-content:space-between;">'
        f'<div style="font-size:.69rem;color:{G};">{tx["footer1"]}</div>'
        f'<div style="font-size:.69rem;color:{G};">{tx["footer2"]}</div>'
        f'</div>', unsafe_allow_html=True)
