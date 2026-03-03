import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(page_title="Lumina CMO Dashboard", layout="wide", initial_sidebar_state="collapsed")

N="#0E1B2E"; N2="#1B2A4A"; N3="#243352"; A="#C9716E"; AL="#E8B4B1"
W="#FFFFFF"; G="#8A96A8"; GL="#C5CAD4"; GR="#2D9C6E"

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');
*{font-family:'DM Sans',sans-serif!important}
.main,.main .block-container{background:#0E1B2E!important;padding:0 2rem 2rem!important;max-width:1500px!important}
[data-testid=stAppViewContainer],[data-testid=stHeader]{background:#0E1B2E!important}
[data-testid=stSidebar]{display:none}
[data-baseweb=tab-list]{background:#1B2A4A!important;border-bottom:2px solid #C9716E!important;gap:0!important;padding:0!important;border-radius:0!important}
[data-baseweb=tab]{background:transparent!important;color:#8A96A8!important;font-size:.82rem!important;font-weight:600!important;letter-spacing:.1em!important;text-transform:uppercase!important;padding:.7rem 1.8rem!important;border:none!important;border-radius:0!important}
[data-baseweb=tab]:hover{color:#FFFFFF!important;background:#243352!important}
[aria-selected=true][data-baseweb=tab]{background:#C9716E!important;color:#FFFFFF!important}
[data-baseweb=tab-highlight],[data-baseweb=tab-border]{display:none!important}
[data-baseweb=select]>div{background:#1B2A4A!important;border:1px solid #2A3A5A!important;border-radius:3px!important;color:#FFF!important}
[data-baseweb=option]{background:#1B2A4A!important;color:#FFF!important}
.stSelectbox label,.stSlider label,.stRadio label{color:#8A96A8!important;font-size:.8rem!important}
[data-baseweb=radio] span{background:#C9716E!important;border-color:#C9716E!important}
[data-testid=metric-container]{background:#1B2A4A!important;border-top:3px solid #C9716E!important;border-radius:3px!important;padding:1rem 1.2rem!important}
[data-testid=stMetricLabel]{color:#8A96A8!important;font-size:.72rem!important;text-transform:uppercase!important;letter-spacing:.08em!important}
[data-testid=stMetricValue]{color:#FFF!important;font-family:'DM Serif Display',serif!important;font-size:2rem!important}
[data-testid=stMetricDelta]{display:none!important}
#MainMenu,footer{visibility:hidden}
.stDeployButton,div[data-testid=stToolbar]{display:none}
</style>""", unsafe_allow_html=True)

SEGS = pd.DataFrame({
    "name":["Perdus","Opportunistes","Fideles Engages","Champions","A Risque"],
    "n":[18846,11874,12979,2674,2180],
    "pct_base":[38.8,24.5,26.7,5.5,4.5],
    "pct_ca":[5.4,23.8,4.3,51.2,15.3],
    "recency":[676,185,141,61,273],
    "frequency":[1.7,8.2,2.3,27.7,4.5],
    "monetary":[72,507,85,4842,1773],
    "basket":[40.2,60.5,35.2,181.5,468.5],
    "churn_prob":[0.95,0.35,0.22,0.08,0.82],
    "clv_score":[1,3,2,5,4],
    "color":["#8A96A8","#4A6FA5","#6B8CAE","#C9716E","#B85A57"],
})
SEGS["ca_total"]=(SEGS["n"]*SEGS["monetary"]).round(0)
SEGS["ca_at_risk"]=(SEGS["churn_prob"]*SEGS["ca_total"]).round(0)

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

FUNNEL=pd.DataFrame({
    "stage":["Awareness","Multi-Touch (3+ canaux)","Long Journey (> 30j)","High Intent (10+ pts)","Conversion"],
    "n":[47834,37310,20100,13400,6840],
    "pct":[100.,78.,42.,28.,14.3],
    "bn":[False,False,True,False,False],
})

def bl(fig,h=380):
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans",color=W,size=12),height=h,margin=dict(l=8,r=8,t=32,b=8),
        legend=dict(bgcolor=N2,bordercolor="#2A3A5A",borderwidth=1,font=dict(size=11,color=G)),
        hoverlabel=dict(bgcolor=N2,bordercolor=A,font=dict(family="DM Sans",size=12,color=W)))
    fig.update_xaxes(gridcolor="#1E2E48",linecolor="#2A3A5A",tickfont=dict(color=G,size=11),zeroline=False)
    fig.update_yaxes(gridcolor="#1E2E48",linecolor="#2A3A5A",tickfont=dict(color=G,size=11),zeroline=False)
    return fig

def slbl(t):
    st.markdown(f'<div style="font-size:.65rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{G};border-bottom:1px solid #1E2E48;padding-bottom:.3rem;margin-bottom:.6rem;">{t}</div>',unsafe_allow_html=True)

def ins(title,body,hi=False):
    bg=A if hi else N3; tc="rgba(255,255,255,.78)" if hi else G
    st.markdown(f'<div style="background:{bg};border-left:3px solid {A};border-radius:0 3px 3px 0;padding:.65rem 1rem;margin-bottom:.45rem;"><b style="font-size:.88rem;color:{W};">{title}</b><div style="font-size:.79rem;color:{tc};line-height:1.45;margin-top:.12rem;">{body}</div></div>',unsafe_allow_html=True)

def reco(t):
    st.markdown(f'<div style="background:{A};border-radius:3px;padding:.85rem 1.15rem;margin-top:.8rem;box-shadow:0 4px 18px rgba(201,113,110,.28);"><div style="font-size:.6rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:.28rem;">Recommandation</div><div style="font-size:.95rem;font-weight:600;color:{W};line-height:1.4;">{t}</div></div>',unsafe_allow_html=True)

def btl(title,body):
    st.markdown(f'<div style="background:rgba(201,113,110,.1);border:1.5px solid {A};border-radius:4px;padding:.8rem 1rem;margin:.65rem 0;"><div style="color:{A};font-weight:700;font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.22rem;">Goulot — {title}</div><div style="color:{AL};font-size:.81rem;line-height:1.45;">{body}</div></div>',unsafe_allow_html=True)

def kpis(items):
    cols=st.columns(len(items))
    for c,(v,l,s) in zip(cols,items):
        sub=f'<div style="font-size:.76rem;color:{AL};margin-top:.18rem;">{s}</div>' if s else ""
        c.markdown(f'<div style="background:{N2};border-top:3px solid {A};border-radius:3px;padding:.9rem 1.1rem;margin-bottom:.4rem;box-shadow:0 4px 18px rgba(0,0,0,.2);"><div style="font-family:\'DM Serif Display\',serif;font-size:2rem;color:{W};line-height:1;">{v}</div><div style="font-size:.68rem;color:{G};text-transform:uppercase;letter-spacing:.08em;margin-top:.18rem;">{l}</div>{sub}</div>',unsafe_allow_html=True)

def phdr(pill,title,desc):
    st.markdown(f'<div style="padding:1.1rem 0 .5rem;"><div style="background:{A};display:inline-block;padding:3px 12px;border-radius:2px;font-size:.67rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#fff;margin-bottom:.5rem;">{pill}</div><div style="font-family:\'DM Serif Display\',serif;font-size:1.7rem;color:{W};line-height:1.2;margin-bottom:.18rem;">{title}</div><div style="font-size:.81rem;color:{G};line-height:1.5;">{desc}</div></div>',unsafe_allow_html=True)

st.markdown(f'<div style="background:{N2};border-bottom:3px solid {A};padding:.9rem 2rem;margin:0 -2rem .8rem;display:flex;align-items:center;justify-content:space-between;"><div><span style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">Lumina <span style="color:{A};">&</span> Co</span><span style="color:{G};font-size:.76rem;margin-left:1rem;">CMO Decision Dashboard</span></div><div style="font-size:.7rem;color:{G};">48,553 clients · 1.8M transactions · 692,782 touchpoints · 2007–2011</div></div><div style="background:{N2};padding:.5rem 0;margin:0 -2rem .8rem;border-bottom:1px solid #1E2E48;"><div style="padding:0 2rem;font-family:\'DM Serif Display\',serif;font-size:1rem;color:{W};font-style:italic;">Comment maximiser la valeur client alors que <span style="color:{A};">95% des efforts marketing traitent tout le monde pareil ?</span></div></div>',unsafe_allow_html=True)

t1,t2,t3=st.tabs(["  Client Segmentation  ","  Churn & CLV  ","  Marketing Attribution  "])

# ── TAB 1 ────────────────────────────────────────────────────────────────────
with t1:
    phdr("Q1 - SEGMENTATION","Qui sont nos clients — et pourquoi les traiter differemment ?","RFM scoring + K-Means K=5 · Silhouette=0.449 · 48,553 clients B2C")
    kpis([("48,553","Clients analyses","Base B2C nettoyee"),("5","Segments K-Means","Silhouette 0.449"),("51.2%","CA par 5.5% des clients","Champions — concentration extremes"),("EUR 468","Panier moyen A Risque","Plus eleve de la base"),("38.8%","Part clients Perdus","Seulement 5.4% du CA")])
    st.markdown("<div style='margin-top:1.2rem'></div>",unsafe_allow_html=True)
    cl,cr=st.columns([3,2],gap="large")

    with cl:
        slbl("TAILLE ET PART DU CA PAR SEGMENT")
        view=st.radio("Metrique",["Part du CA (%)","Nombre de clients","Panier moyen (EUR)","Recence (j)"],horizontal=True,key="sv")
        ck={"Part du CA (%)":"pct_ca","Nombre de clients":"n","Panier moyen (EUR)":"basket","Recence (j)":"recency"}[view]
        clb={"pct_ca":"% CA","n":"N clients","basket":"Panier (EUR)","recency":"Recence (j)"}[ck]
        f1=go.Figure()
        for _,r in SEGS.sort_values(ck,ascending=True).iterrows():
            f1.add_trace(go.Bar(x=[r[ck]],y=[r["name"]],orientation="h",marker=dict(color=r["color"],opacity=.9,line=dict(color=N,width=.6)),text=[f"  {r[ck]:,.1f}"],textposition="inside",textfont=dict(color=W,size=11),showlegend=False,hovertemplate=f"<b>{r['name']}</b><br>{clb}: %{{x:,.1f}}<br>N: {r['n']:,}<br>CA: {r['pct_ca']}%<extra></extra>"))
        bl(f1,270);f1.update_layout(xaxis=dict(title=clb,title_font=dict(color=G,size=11)),bargap=.3,showlegend=False)
        st.plotly_chart(f1,use_container_width=True,config={"displayModeBar":False})

        slbl("CONCENTRATION DU REVENU")
        f2=go.Figure(data=[go.Pie(labels=SEGS["name"],values=SEGS["pct_ca"],hole=.58,marker=dict(colors=SEGS["color"].tolist(),line=dict(color=N,width=2.5)),textinfo="label+percent",textfont=dict(size=11,color=W),hovertemplate="<b>%{label}</b><br>CA: %{value}%<br>N: %{customdata:,}<extra></extra>",customdata=SEGS["n"])])
        f2.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(family="DM Sans",color=W),height=270,margin=dict(l=0,r=0,t=8,b=0),legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11,color=G),orientation="h",y=-.1),annotations=[dict(text="<b>CA</b>",x=.5,y=.5,font=dict(size=17,color=W,family="DM Serif Display"),showarrow=False)])
        st.plotly_chart(f2,use_container_width=True,config={"displayModeBar":False})

    with cr:
        slbl("OBSERVATIONS CLES")
        ins("5.5% genere 51.2% du CA","Champions : 27.7x/an, panier EUR 181, tenure 606j. Coeur structurel du business.",hi=True)
        ins("38.8% des clients = 5.4% du CA","Les Perdus sur-consomment les emails generiques sans retour mesurable.")
        ins("A Risque : panier EUR 468 — le plus eleve","Etaient des Champions. 273j de silence. Signal le plus urgent de la base.")
        ins("Opportunistes : potentiel sous-exploite","24.5% de la base, 18 categories. Potentiel de migration vers Champions.")
        reco("3 tracks distincts : VIP Champions / urgence A Risque / low-cost Perdus — lift >= 25%")

    st.markdown("<div style='margin-top:1.5rem'></div>",unsafe_allow_html=True)
    slbl("SCATTER RECENCY x MONETARY — QUI CIBLER EN PRIORITE ?")
    np.random.seed(42)
    pts=[]
    for _,seg in SEGS.iterrows():
        n2=min(seg["n"],200)
        pts.append(pd.DataFrame({"rec":np.random.normal(seg["recency"],seg["recency"]*.22,n2).clip(1,900),"mon":np.random.lognormal(np.log(max(seg["monetary"],10)),.55,n2).clip(1,15000),"seg":seg["name"],"col":seg["color"]}))
    df_sc=pd.concat(pts,ignore_index=True)
    f3=go.Figure()
    for _,seg in SEGS.iterrows():
        d=df_sc[df_sc["seg"]==seg["name"]]
        f3.add_trace(go.Scatter(x=d["rec"],y=d["mon"],mode="markers",marker=dict(size=5,color=seg["color"],opacity=.62,line=dict(color=N,width=.2)),name=seg["name"],hovertemplate=f"<b>{seg['name']}</b><br>Recence: %{{x:.0f}}j<br>CA: EUR %{{y:,.0f}}<extra></extra>"))
    f3.add_vline(x=160,line_dash="dash",line_color=A,line_width=1.5,annotation_text="Seuil churn P90=160j",annotation_font_color=A,annotation_font_size=10,annotation_position="top right")
    f3.add_vrect(x0=0,x1=160,fillcolor="rgba(201,113,110,.04)",line_width=0)
    f3.add_vrect(x0=160,x1=900,fillcolor="rgba(138,150,168,.04)",line_width=0)
    bl(f3,340);f3.update_layout(xaxis=dict(title="Recence (j) — plus bas = plus recent",range=[0,850]),yaxis=dict(title="CA total client (EUR)",type="log"),legend=dict(orientation="h",y=1.06))
    st.plotly_chart(f3,use_container_width=True,config={"displayModeBar":False})
    st.markdown(f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;margin-top:.2rem;"><div style="background:{N2};border-left:3px solid {A};padding:.55rem .85rem;border-radius:0 3px 3px 0;font-size:.78rem;color:{G};"><b style="color:{W};">Zone gauche (< 160j)</b> — clients actifs, priorite protection</div><div style="background:{N2};border-left:3px solid {G};padding:.55rem .85rem;border-radius:0 3px 3px 0;font-size:.78rem;color:{G};"><b style="color:{W};">Zone droite (> 160j)</b> — churnes ou en sortie</div><div style="background:{N2};border-left:3px solid {AL};padding:.55rem .85rem;border-radius:0 3px 3px 0;font-size:.78rem;color:{G};"><b style="color:{W};">A Risque (rouge, droite, haut)</b> — valeur elevee + silence</div></div>',unsafe_allow_html=True)

# ── TAB 2 ────────────────────────────────────────────────────────────────────
with t2:
    phdr("Q2 - CHURN & CLV","Quels clients vont partir — et combien ca coute ?","Gradient Boosting ROC-AUC 0.70–0.80 · Seuil P90=160j · Zero data leakage")
    ca_tot=int(SEGS["ca_total"].sum());ca_risk=int(SEGS["ca_at_risk"].sum())
    kpis([("160j","Seuil churn P90","No purchase >160j = churned"),("0.70–0.80","ROC-AUC Gradient Boosting","Modele retenu"),("EUR "+f"{ca_risk/1e6:.1f}M","CA total a risque",f"{ca_risk/ca_tot*100:.1f}% du CA"),("2,180","Clients A Risque","EUR 468 panier · 15.3% CA"),(">8,000%","ROI simulation top 500","EUR 17,500 → EUR 1.5M+")])
    st.markdown("<div style='margin-top:1.2rem'></div>",unsafe_allow_html=True)
    ca,cb=st.columns([3,2],gap="large")

    with ca:
        slbl("MATRICE CLV x RISQUE CHURN")
        f4=go.Figure()
        for _,seg in SEGS.iterrows():
            sz=(seg["n"]/SEGS["n"].max())*52+12
            f4.add_trace(go.Scatter(x=[seg["churn_prob"]*10],y=[seg["clv_score"]*1.8],mode="markers+text",marker=dict(size=sz,color=seg["color"],opacity=.88,line=dict(color=W,width=1.5 if seg["name"] in ["Champions","A Risque"] else .5)),text=[seg["name"]],textposition="top center",textfont=dict(size=10,color=W),showlegend=False,hovertemplate=f"<b>{seg['name']}</b><br>Churn: {seg['churn_prob']*100:.0f}%<br>CLV: {seg['clv_score']}/5<br>N: {seg['n']:,}<br>CA at risk: EUR {seg['ca_at_risk']:,.0f}<extra></extra>"))
        bl(f4,340);f4.update_layout(xaxis=dict(title="Probabilite de churn (0-10)",range=[0,11]),yaxis=dict(title="Score CLV",range=[0,10.5]))
        for x,y,t,tc in [(2.5,10.,"Q2 - PROTEGER",G),(7.5,10.,"Q1 - PRIORITE #1",A),(2.5,.4,"Q4 - SURVEILLER",G),(7.5,.4,"Q3 - LOW COST",G)]:
            f4.add_annotation(x=x,y=y,text=t,showarrow=False,font=dict(color=tc,size=9),bgcolor=N2)
        f4.add_vline(x=5,line_dash="dash",line_color=G,line_width=1,opacity=.35)
        f4.add_hline(y=5.5,line_dash="dash",line_color=G,line_width=1,opacity=.35)
        st.plotly_chart(f4,use_container_width=True,config={"displayModeBar":False})

        slbl("CA A RISQUE PAR SEGMENT")
        f5=go.Figure()
        for _,row in SEGS.sort_values("ca_at_risk",ascending=True).iterrows():
            f5.add_trace(go.Bar(x=[row["ca_at_risk"]],y=[row["name"]],orientation="h",marker=dict(color=row["color"],opacity=.9,line=dict(color=N,width=.4)),text=[f"  EUR {row['ca_at_risk']/1e6:.2f}M ({row['churn_prob']*100:.0f}% churn)"],textposition="inside",textfont=dict(color=W,size=10),showlegend=False,hovertemplate=f"<b>{row['name']}</b><br>CA at risk: EUR {row['ca_at_risk']:,.0f}<extra></extra>"))
        bl(f5,220);f5.update_layout(xaxis=dict(title="CA a risque (EUR)"),bargap=.3)
        st.plotly_chart(f5,use_container_width=True,config={"displayModeBar":False})

    with cb:
        slbl("DRIVERS DE CHURN")
        CHURN=pd.DataFrame({"label":["Recence","Tendance IPT","Dernier ecart/moy","Tendance panier","Mois inactifs 6m"],"imp":[100,82,65,50,38],"action":["Alerte >120j","Trigger +20% ecart","Urgent si ratio >1.5","Offre si -20% panier","React apres 2 mois"]})
        f6=go.Figure()
        for i,row in CHURN.iterrows():
            f6.add_trace(go.Bar(x=[row["imp"]],y=[row["label"]],orientation="h",marker=dict(color=A,opacity=1-.1*i,line=dict(color=N,width=.4)),text=[f"  {row['imp']}%"],textposition="inside",textfont=dict(color=W,size=11),showlegend=False,hovertemplate=f"<b>{row['label']}</b><br>{row['action']}<extra></extra>"))
        bl(f6,235);f6.update_layout(xaxis=dict(title="Importance (%)",range=[0,120]),yaxis=dict(autorange="reversed"),bargap=.28)
        st.plotly_chart(f6,use_container_width=True,config={"displayModeBar":False})

        slbl("ACTIONS PRIORITAIRES")
        for _,row in CHURN.iterrows():
            st.markdown(f'<div style="background:{N2};border-left:3px solid {A};border-radius:0 3px 3px 0;padding:.5rem .8rem;margin-bottom:.35rem;"><b style="font-size:.84rem;color:{W};">{row["label"]}</b><div style="font-size:.74rem;color:{G};margin-top:.08rem;">{row["action"]}</div></div>',unsafe_allow_html=True)

        slbl("SIMULATEUR ROI — RETENTION Q1")
        nc=st.slider("Clients cibles",50,2180,500,50)
        taux=st.slider("Taux recuperation (%)",1,40,10,1)
        budget=nc*35;rev=nc*30000*(taux/100);roi_v=((rev-budget)/budget)*100
        be=next((r for r in range(1,51) if nc*30000*(r/100)>=budget),None)
        st.markdown(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:.45rem;margin-top:.3rem;"><div style="background:{N2};border-top:2px solid {A};border-radius:3px;padding:.65rem .9rem;"><div style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">EUR {budget:,}</div><div style="font-size:.68rem;color:{G};text-transform:uppercase;">Budget</div></div><div style="background:{N2};border-top:2px solid {GR};border-radius:3px;padding:.65rem .9rem;"><div style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">EUR {rev/1e6:.2f}M</div><div style="font-size:.68rem;color:{G};text-transform:uppercase;">CA recupere</div></div><div style="background:{N2};border-top:2px solid {A};border-radius:3px;padding:.65rem .9rem;"><div style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">{roi_v:,.0f}%</div><div style="font-size:.68rem;color:{G};text-transform:uppercase;">ROI</div></div><div style="background:{N2};border-top:2px solid {AL};border-radius:3px;padding:.65rem .9rem;"><div style="font-family:\'DM Serif Display\',serif;font-size:1.45rem;color:{W};">{be}%</div><div style="font-size:.68rem;color:{G};text-transform:uppercase;">Breakeven</div></div></div>',unsafe_allow_html=True)
        rates=np.arange(1,41);rois2=[((nc*30000*(r/100)-budget)/budget)*100 for r in rates]
        f7=go.Figure()
        f7.add_trace(go.Scatter(x=rates,y=rois2,mode="lines",line=dict(color=A,width=2.5),fill="tozeroy",fillcolor="rgba(201,113,110,.08)",showlegend=False))
        f7.add_vline(x=taux,line_dash="dash",line_color=W,opacity=.45)
        if be:f7.add_vline(x=be,line_dash="dot",line_color=GR,opacity=.8,annotation_text=f"BE {be}%",annotation_font_color=GR,annotation_font_size=9)
        f7.add_hline(y=0,line_color=G,opacity=.3)
        bl(f7,190);f7.update_layout(yaxis=dict(title="ROI (%)"),xaxis=dict(title="Taux (%)"),margin=dict(l=8,r=8,t=8,b=8))
        st.plotly_chart(f7,use_container_width=True,config={"displayModeBar":False})
        reco(f"Top {nc} clients A Risque — EUR {budget:,} — EUR {rev/1e6:.1f}M a {taux}% — breakeven {be}%")

# ── TAB 3 ────────────────────────────────────────────────────────────────────
with t3:
    phdr("Q3 - ATTRIBUTION","Ou fonctionne vraiment le budget marketing ?","692,782 touchpoints · 7 canaux · Markov removal effect · 99,096 parcours · CVR 14.3%")
    kpis([("14.3%","Taux conversion global","47,834 → 6,840"),("155j","Duree moyenne parcours","14.5 touchpoints / client"),("74.6%","Parcours > 30 jours","Goulot principal"),("27x","ROAS Display Markov","5.1% LT → 14.9% Markov"),("+9.8pp","Sous-credit Display & Social","Invisibles en last-touch")])
    st.markdown("<div style='margin-top:1.2rem'></div>",unsafe_allow_html=True)

    slbl("FUNNEL DE CONVERSION — GOULOT D'ETRANGLEMENT")
    cf,cfi=st.columns([3,2],gap="large")

    with cf:
        f8=go.Figure()
        for i,row in FUNNEL.iterrows():
            bn=row["bn"]
            f8.add_trace(go.Bar(x=[row["n"]],y=[row["stage"]],orientation="h",marker=dict(color=A if bn else ("#4A6FA5" if i>0 else G),opacity=1. if bn else .76,line=dict(color=W if bn else N,width=2.5 if bn else .4)),text=[f"  {row['n']:,}   ({row['pct']:.1f}%)"],textposition="inside",textfont=dict(color=W,size=12 if bn else 11),showlegend=False,name=row["stage"],hovertemplate=f"<b>{row['stage']}</b><br>Clients: {row['n']:,}<br>Taux: {row['pct']:.1f}%<extra></extra>",width=.62))
        bl(f8,340);f8.update_layout(xaxis=dict(title="Nombre de clients",range=[0,55000]),yaxis=dict(autorange="reversed",tickfont=dict(size=11.5)),bargap=.32)
        f8.add_annotation(x=21000,y="Long Journey (> 30j)",text="<b>GOULOT D'ETRANGLEMENT</b><br>74.6% des parcours > 30j<br>Last-touch ignore le vrai travail",showarrow=True,arrowhead=2,arrowcolor=A,arrowwidth=2.5,ax=110,ay=-42,font=dict(color=W,size=10),bgcolor=N2,bordercolor=A,borderwidth=1.5,borderpad=5)
        for i in range(len(FUNNEL)-1):
            f8.add_annotation(x=FUNNEL["n"].iloc[i+1]+1600,y=i+.5,text=f"-{FUNNEL['pct'].iloc[i]-FUNNEL['pct'].iloc[i+1]:.1f}pp",showarrow=False,font=dict(color=AL,size=9.5))
        st.plotly_chart(f8,use_container_width=True,config={"displayModeBar":False})

    with cfi:
        slbl("CE QUE LE FUNNEL REVELE")
        btl("74.6% des parcours > 30 jours","Un client est expose 155 jours, 14.5 touchpoints avant d'acheter. Crediter le dernier clic = ignorer 14 etapes sur 14.5.")
        ins("Display & Social demarrent 28.6% des parcours","5% credit last-touch chacun → 14.9% Markov. ROAS 27x et 16x sous-exploites.")
        ins("Email = fermeture, pas moteur","Position ~14 dans le parcours. Recoit 21.6% en LT. Role de cloture uniquement.")
        ins("Cout de l'erreur d'attribution","ROAS Display 27x invisible en LT. Budget massivement mal alloue depuis des annees.")

    st.markdown("<div style='margin-top:1.6rem'></div>",unsafe_allow_html=True)
    slbl("COMPARAISON MODELES — LAST-TOUCH / FIRST-TOUCH / LINEAR / MARKOV")
    cc1,cc2=st.columns([3,2],gap="large")

    with cc1:
        msel=st.radio("Comparer avec Markov",["Last-Touch","First-Touch","Linear","Tous les modeles"],horizontal=True,key="am")
        mcols={"Last-Touch":"last_touch","First-Touch":"first_touch","Linear":"linear"}
        das=ATTR.sort_values("markov",ascending=True)
        if msel=="Tous les modeles":
            f9=go.Figure()
            for mn,mc,mcol in [("Last-Touch","last_touch",G),("First-Touch","first_touch","#4A6FA5"),("Linear","linear",GL),("Markov","markov",A)]:
                f9.add_trace(go.Bar(x=das["channel"],y=das[mc],name=mn,marker=dict(color=mcol,opacity=.88,line=dict(color=N,width=.3)),hovertemplate=f"<b>%{{x}}</b><br>{mn}: %{{y:.1f}}%<extra></extra>"))
            bl(f9,340);f9.update_layout(barmode="group",bargap=.15,bargroupgap=.05,xaxis=dict(title="Canal"),yaxis=dict(title="Attribution (%)"),legend=dict(orientation="h",y=1.06))
        else:
            cc=mcols[msel];ccol=G if msel=="Last-Touch" else ("#4A6FA5" if msel=="First-Touch" else GL)
            f9=go.Figure()
            f9.add_trace(go.Bar(y=das["channel"],x=das[cc],orientation="h",name=msel,marker=dict(color=ccol,opacity=.7,line=dict(color=N,width=.3)),text=[f"{v:.1f}%" for v in das[cc]],textposition="outside",textfont=dict(color=G,size=10),hovertemplate=f"<b>%{{y}}</b><br>{msel}: %{{x:.1f}}%<extra></extra>"))
            f9.add_trace(go.Bar(y=das["channel"],x=das["markov"],orientation="h",name="Markov",marker=dict(color=A,opacity=.92,line=dict(color=N,width=.3)),text=[f"{v:.1f}%" for v in das["markov"]],textposition="outside",textfont=dict(color=AL,size=10),hovertemplate="<b>%{y}</b><br>Markov: %{x:.1f}%<extra></extra>"))
            bl(f9,320);f9.update_layout(barmode="group",bargap=.22,bargroupgap=.06,xaxis=dict(title="Attribution (%)",range=[0,38]),legend=dict(orientation="h",y=1.06))
        st.plotly_chart(f9,use_container_width=True,config={"displayModeBar":False})

        slbl("ECART MARKOV - LAST-TOUCH (pp)")
        dd=ATTR.sort_values("delta")
        f10=go.Figure()
        f10.add_trace(go.Bar(x=dd["channel"],y=dd["delta"],marker=dict(color=[A if d>0 else "#5A6A82" for d in dd["delta"]],opacity=.9,line=dict(color=N,width=.4)),text=[f"{d:+.1f}pp" for d in dd["delta"]],textposition="outside",textfont=dict(color=[AL if d>0 else G for d in dd["delta"]],size=11),showlegend=False,hovertemplate="<b>%{x}</b><br>Ecart: %{y:+.2f}pp<extra></extra>"))
        f10.add_hline(y=0,line_color=G,opacity=.4,line_width=1)
        f10.add_annotation(x=.8,y=11,text="Sous-credites",showarrow=False,font=dict(color=A,size=10),bgcolor=N2)
        f10.add_annotation(x=4.8,y=-9,text="Sur-credites",showarrow=False,font=dict(color=G,size=10),bgcolor=N2)
        bl(f10,230);f10.update_layout(yaxis=dict(title="Ecart Markov - LT (pp)"),margin=dict(t=18))
        st.plotly_chart(f10,use_container_width=True,config={"displayModeBar":False})

    with cc2:
        slbl("ANALYSE CANAL PAR CANAL")
        for _,row in ATTR.sort_values("delta",ascending=False).iterrows():
            ih=row["delta"]>0;bc2=A if ih else "#3A4A62";ds=f"+{row['delta']:.1f}pp" if ih else f"{row['delta']:.1f}pp"
            st.markdown(f'<div style="background:{N2};border-left:3px solid {bc2};border-radius:0 3px 3px 0;padding:.55rem .88rem;margin-bottom:.38rem;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.1rem;"><b style="font-size:.9rem;color:{W};">{row["channel"]}</b><span style="font-size:.6rem;font-weight:700;color:{A if ih else G};letter-spacing:.1em;">{"SOUS-CREDITE" if ih else "SUR-CREDITE"}</span></div><div style="display:flex;gap:.7rem;font-size:.76rem;color:{G};"><span>LT: <b style="color:{W};">{row["last_touch"]:.1f}%</b></span><span>MK: <b style="color:{A if ih else W};">{row["markov"]:.1f}%</b></span><span style="color:{A if ih else G};font-weight:600;">{ds}</span><span style="color:{A if ih else G};">ROAS {row["roas"]}x</span></div><div style="font-size:.72rem;color:{G};margin-top:.1rem;">{row["touchpoints"]:,} touchpoints · {row["role"]}</div></div>',unsafe_allow_html=True)
        btl("Budget mal alloue","Email+Direct+Retargeting sur-credites 7-8pp. Display+Social+Affiliate sous-credites ~10pp. 20% reallocation = +15 a 25% ROAS.")
        reco("Adopter Markov + reallouer 20% Email+Direct vers Display+Social+Affiliates — ROAS +15 a +25%")

    st.markdown(f'<div style="margin-top:1.8rem;padding:.7rem 0;border-top:1px solid #1E2E48;display:flex;justify-content:space-between;"><div style="font-size:.7rem;color:{G};">Lumina & Co — Data Marketing DIA3 · TP1-TP5</div><div style="font-size:.7rem;color:{G};">UCI Online Retail II · 48,553 clients · 2007-2011</div></div>',unsafe_allow_html=True)
