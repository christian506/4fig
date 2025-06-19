import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="🚬 Global Smoking Dashboard", layout="wide")
st.title("🚬 Global Smoking Statistics Dashboard")
st.markdown("Explore global patterns of smoking by gender, age, and country in one page.")

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("smoking.csv")  # reads your repo file

df = load_data()
col = "Data.Percentage.Total"

# ─── Sidebar Filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filters")
    years = sorted(df.Year.unique())
    ctrs = sorted(df.Country.unique())
    sel_y = st.multiselect("Year", years, years)
    sel_c = st.multiselect("Country", ctrs, ctrs)

data = df[df.Year.isin(sel_y) & df.Country.isin(sel_c)]

# ─── KPI Row ──────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
k1.metric("Records", data.shape[0])
k2.metric("Countries", data.Country.nunique())
k3.metric("Avg Smoking Rate (%)", f"{data[col].mean():.2f}")

# ─── Row 1: Bar + Box ─────────────────────────────────────────────────────────
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.markdown("### 🌍 Top 10 Countries")
    top10 = data.groupby("Country")[col].mean().nlargest(10).reset_index()
    fig1 = px.bar(top10, x="Country", y=col, title="Smoking Rate by Country")
    st.plotly_chart(fig1, use_container_width=True)

with r1c2:
    st.markdown("### 🧑‍🤝‍🧑 By Gender")
    if "Data.Percentage.Male" in df and "Data.Percentage.Female" in df:
        g = data.melt(
            id_vars=["Country","Year"],
            value_vars=["Data.Percentage.Male","Data.Percentage.Female"],
            var_name="Gender", value_name="Rate"
        )
        g.Gender = g.Gender.str.extract(r"(\w+)$")
        fig2 = px.box(g, x="Gender", y="Rate", color="Gender", title="Smoking by Gender")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No gender split in data.")

# ─── Row 2: Line + Map ─────────────────────────────────────────────────────────
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown("### 📈 Trend Over Time")
    trend = data.groupby("Year")[col].mean().reset_index()
    fig3 = px.line(trend, x="Year", y=col, markers=True, title="Avg Smoking Rate Over Years")
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    st.markdown("### 🗺️ World Map")
    cmap = data.groupby("Country")[col].mean().reset_index()
    fig4 = px.choropleth(
        cmap, locations="Country", locationmode="country names",
        color=col, color_continuous_scale="Reds", title="Smoking Prevalence by Country"
    )
    st.plotly_chart(fig4, use_container_width=True)
