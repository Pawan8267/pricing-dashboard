import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery
from google.oauth2 import service_account


# =========================
# CONFIG
# =========================
SERVICE_ACCOUNT_FILE = r"C:\Users\Pawan gangwar\Downloads\quick-commerce-ads-5b7987d2e442.json"
PROJECT_ID = "quick-commerce-ads"

MAIN_TABLE = "`quick-commerce-ads.warehouse.all_channel_pricing_data`"
AMAZON_TABLE = "`quick-commerce-ads.warehouse.amazon_Pricing_data`"
FLIPKART_TABLE = "`quick-commerce-ads.warehouse.flipkart_Pricing_data`"
QUICK_TABLE = "`quick-commerce-ads.warehouse.Quick_Commmerce_daily_data`"
INSTAMART_TABLE = "`quick-commerce-ads.warehouse.instamart_sanfe_pricing_data`"
BIGBASKET_TABLE = "`quick-commerce-ads.warehouse.bigbasket_sanfe_pricing_data`"


# =========================
# PAGE SETUP
# =========================
st.set_page_config(
    page_title="Pricing Intelligence Dashboard",
    layout="wide"
)

st.markdown("""
<style>

/* Hide Streamlit menu */
#MainMenu {
    visibility: hidden;
}

/* Hide footer */
footer {
    visibility: hidden;
}

/* Hide header */
header {
    visibility: hidden;
}

/* Hide GitHub/Fork button */
.viewerBadge_container__1QSob,
.styles_viewerBadge__1yB5_,
.viewerBadge_link__1S137,
.stDeployButton {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CSS THEME
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #f0fdf4 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 20px;
        border-radius: 18px;
        border-left: 6px solid #2563eb;
        box-shadow: 0px 8px 22px rgba(15,23,42,0.10);
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-size: 32px;
        font-weight: 800;
    }

    div[data-testid="stMetricLabel"] {
        color: #475569;
        font-weight: 700;
    }

    h1 {
        color: #0f172a;
        font-weight: 900;
    }

    h2, h3 {
        color: #1e293b;
        font-weight: 800;
    }

    .stDataFrame {
        background: white;
        border-radius: 16px;
        box-shadow: 0px 6px 18px rgba(15,23,42,0.08);
        padding: 8px;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        font-weight: 600;
    }

    .stDownloadButton button {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 18px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Multi-Channel Pricing Intelligence Dashboard")
st.caption("Amazon | Flipkart | Blinkit | Zepto | Instamart | BigBasket")


# =========================
# BIGQUERY CONNECTION
# =========================
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)


# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=600)
def load_data():
    query = f"""
    WITH main_data AS (
        SELECT
            date,
            CAST(timestamp AS STRING) AS timestamp,
            CAST(company AS STRING) AS company,
            CAST(brand AS STRING) AS brand,
            CAST(product_label AS STRING) AS product_label,
            CAST(platform AS STRING) AS platform,
            CAST(product_id AS STRING) AS product_id,
            CAST(asin AS STRING) AS asin,
            CAST(pid AS STRING) AS pid,
            CAST(product_name AS STRING) AS product_name,
            CAST(variant AS STRING) AS variant,
            CAST(mrp AS FLOAT64) AS mrp,
            CAST(sp_price AS FLOAT64) AS sp_price,
            CAST(discount_percent AS FLOAT64) AS discount_percent,
            CAST(rating AS FLOAT64) AS rating,
            CAST(stock_status AS STRING) AS stock_status,
            CAST(location AS STRING) AS location,
            CAST(keyword AS STRING) AS keyword,
            CAST(rank AS FLOAT64) AS rank,
            CAST(is_ad AS FLOAT64) AS is_ad,
            CAST(product_url AS STRING) AS product_url,
            CAST(scrape_source AS STRING) AS scrape_source
        FROM {MAIN_TABLE}
    ),

    amazon_data AS (
        SELECT
            date,
            CAST(timestamp AS STRING) AS timestamp,
            'Unknown' AS company,
            CAST(brand AS STRING) AS brand,
            CAST(product_name AS STRING) AS product_label,
            CAST(platform AS STRING) AS platform,
            CAST(asin AS STRING) AS product_id,
            CAST(asin AS STRING) AS asin,
            CAST(NULL AS STRING) AS pid,
            CAST(product_name AS STRING) AS product_name,
            CAST(NULL AS STRING) AS variant,
            CAST(NULL AS FLOAT64) AS mrp,
            CAST(sp_price AS FLOAT64) AS sp_price,
            CAST(NULL AS FLOAT64) AS discount_percent,
            CAST(rating AS FLOAT64) AS rating,
            CAST(NULL AS STRING) AS stock_status,
            'All India' AS location,
            CAST(NULL AS STRING) AS keyword,
            CAST(NULL AS FLOAT64) AS rank,
            CAST(NULL AS FLOAT64) AS is_ad,
            CAST(NULL AS STRING) AS product_url,
            'amazon_old_table' AS scrape_source
        FROM {AMAZON_TABLE}
    ),

    flipkart_data AS (
        SELECT
            date,
            CAST(timestamp AS STRING) AS timestamp,
            'Unknown' AS company,
            CAST(brand AS STRING) AS brand,
            CAST(product_name AS STRING) AS product_label,
            CAST(platform AS STRING) AS platform,
            CAST(pid AS STRING) AS product_id,
            CAST(NULL AS STRING) AS asin,
            CAST(pid AS STRING) AS pid,
            CAST(product_name AS STRING) AS product_name,
            CAST(NULL AS STRING) AS variant,
            CAST(NULL AS FLOAT64) AS mrp,
            CAST(sp_price AS FLOAT64) AS sp_price,
            CAST(NULL AS FLOAT64) AS discount_percent,
            CAST(rating AS FLOAT64) AS rating,
            CAST(NULL AS STRING) AS stock_status,
            'All India' AS location,
            CAST(NULL AS STRING) AS keyword,
            CAST(NULL AS FLOAT64) AS rank,
            CAST(NULL AS FLOAT64) AS is_ad,
            CAST(NULL AS STRING) AS product_url,
            'flipkart_old_table' AS scrape_source
        FROM {FLIPKART_TABLE}
    ),

    quick_data AS (
        SELECT
            SAFE_CAST(date AS DATE) AS date,
            CAST(timestamp AS STRING) AS timestamp,
            'Unknown' AS company,
            CAST(brand AS STRING) AS brand,
            CAST(product_name AS STRING) AS product_label,
            CAST(platform AS STRING) AS platform,
            CAST(product_id AS STRING) AS product_id,
            CAST(NULL AS STRING) AS asin,
            CAST(NULL AS STRING) AS pid,
            CAST(product_name AS STRING) AS product_name,
            CAST(variant AS STRING) AS variant,
            CAST(NULL AS FLOAT64) AS mrp,
            CAST(price AS FLOAT64) AS sp_price,
            CAST(NULL AS FLOAT64) AS discount_percent,
            CAST(NULL AS FLOAT64) AS rating,
            CAST(NULL AS STRING) AS stock_status,
            CAST(location AS STRING) AS location,
            CAST(keyword AS STRING) AS keyword,
            CAST(rank AS FLOAT64) AS rank,
            CAST(is_ad AS FLOAT64) AS is_ad,
            CAST(NULL AS STRING) AS product_url,
            'quick_commerce_table' AS scrape_source
        FROM {QUICK_TABLE}
        WHERE LOWER(platform) IN ('blinkit', 'zepto')
    ),

    instamart_data AS (
        SELECT
            date,
            CAST(timestamp AS STRING) AS timestamp,
            'Unknown' AS company,
            CAST(brand AS STRING) AS brand,
            CAST(product_name AS STRING) AS product_label,
            CAST(platform AS STRING) AS platform,
            CAST(product_id AS STRING) AS product_id,
            CAST(NULL AS STRING) AS asin,
            CAST(NULL AS STRING) AS pid,
            CAST(product_name AS STRING) AS product_name,
            CAST(variant AS STRING) AS variant,
            CAST(mrp AS FLOAT64) AS mrp,
            CAST(sp_price AS FLOAT64) AS sp_price,
            CAST(NULL AS FLOAT64) AS discount_percent,
            CAST(NULL AS FLOAT64) AS rating,
            CAST(stock_status AS STRING) AS stock_status,
            CAST(location AS STRING) AS location,
            CAST(keyword AS STRING) AS keyword,
            CAST(rank AS FLOAT64) AS rank,
            CAST(is_ad AS FLOAT64) AS is_ad,
            CAST(NULL AS STRING) AS product_url,
            'instamart_table' AS scrape_source
        FROM {INSTAMART_TABLE}
    ),

    bigbasket_data AS (
        SELECT
            date,
            CAST(timestamp AS STRING) AS timestamp,
            'Unknown' AS company,
            CAST(brand AS STRING) AS brand,
            CAST(product_name AS STRING) AS product_label,
            CAST(platform AS STRING) AS platform,
            CAST(product_id AS STRING) AS product_id,
            CAST(NULL AS STRING) AS asin,
            CAST(NULL AS STRING) AS pid,
            CAST(product_name AS STRING) AS product_name,
            CAST(variant AS STRING) AS variant,
            CAST(mrp AS FLOAT64) AS mrp,
            CAST(sp_price AS FLOAT64) AS sp_price,
            CAST(NULL AS FLOAT64) AS discount_percent,
            SAFE_CAST(rating AS FLOAT64) AS rating,
            CAST(stock_status AS STRING) AS stock_status,
            CAST(location AS STRING) AS location,
            CAST(keyword AS STRING) AS keyword,
            CAST(rank AS FLOAT64) AS rank,
            CAST(is_ad AS FLOAT64) AS is_ad,
            CAST(product_url AS STRING) AS product_url,
            'bigbasket_table' AS scrape_source
        FROM {BIGBASKET_TABLE}
    )

    SELECT * FROM main_data
    UNION ALL SELECT * FROM amazon_data
    UNION ALL SELECT * FROM flipkart_data
    UNION ALL SELECT * FROM quick_data
    UNION ALL SELECT * FROM instamart_data
    UNION ALL SELECT * FROM bigbasket_data
    """

    df = client.query(query).to_dataframe(
        create_bqstorage_client=False
    )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["sp_price"] = pd.to_numeric(df["sp_price"], errors="coerce")
    df["mrp"] = pd.to_numeric(df["mrp"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
    df["is_ad"] = pd.to_numeric(df["is_ad"], errors="coerce")

    df = df.dropna(subset=["date", "sp_price"])

    df["brand"] = df["brand"].fillna("Unknown")
    df["platform"] = df["platform"].fillna("Unknown").str.title()
    df["location"] = df["location"].fillna("All India")
    df["product_id"] = df["product_id"].fillna("")
    df["asin"] = df["asin"].fillna("")
    df["pid"] = df["pid"].fillna("")
    df["product_name"] = df["product_name"].fillna("")
    df["product_label"] = df["product_label"].fillna(df["product_name"])

    return df


df = load_data()

if df.empty:
    st.warning("No data found in BigQuery.")
    st.stop()


# =========================
# CHANNEL COLORS
# =========================
CHANNEL_COLORS = {
    "Amazon": "#ff9900",
    "Flipkart": "#2874f0",
    "Blinkit": "#facc15",
    "Zepto": "#7c3aed",
    "Instamart": "#fc8019",
    "Bigbasket": "#84c225",
    "BigBasket": "#84c225"
}


# =========================
# SIDEBAR
# =========================
st.sidebar.header("🔍 Search Product")

platform = st.sidebar.selectbox(
    "Select Channel",
    ["All"] + sorted(df["platform"].dropna().unique().tolist())
)

brand_search = st.sidebar.text_input(
    "Enter Brand Name",
    placeholder="Example: Sanfe, Boldfit, Azah"
)

location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + sorted(df["location"].dropna().unique().tolist())
)

base_filter = df.copy()

if platform != "All":
    base_filter = base_filter[base_filter["platform"] == platform]

if brand_search:
    base_filter = base_filter[
        base_filter["brand"].astype(str).str.lower().str.contains(
            brand_search.lower(), na=False
        )
    ]

if location != "All":
    base_filter = base_filter[base_filter["location"] == location]

id_options = sorted(
    base_filter["product_id"]
    .replace("", pd.NA)
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_product_id = st.sidebar.selectbox(
    "Select ASIN / Product ID",
    ["All"] + id_options
)

manual_search = st.sidebar.text_input(
    "Or Enter Product ID / Product Name",
    placeholder="Example: B08R68DYS3"
)

days = st.sidebar.radio(
    "Time Period",
    [7, 14, 31, 60, 90],
    horizontal=True
)


# =========================
# FILTER DATA
# =========================
filtered = base_filter.copy()

if selected_product_id != "All":
    filtered = filtered[filtered["product_id"].astype(str) == selected_product_id]

if manual_search:
    s = manual_search.lower()
    filtered = filtered[
        filtered["product_id"].astype(str).str.lower().str.contains(s, na=False)
        | filtered["asin"].astype(str).str.lower().str.contains(s, na=False)
        | filtered["pid"].astype(str).str.lower().str.contains(s, na=False)
        | filtered["product_name"].astype(str).str.lower().str.contains(s, na=False)
    ]

if filtered.empty:
    st.warning("No data found for selected filter.")
    st.stop()

max_date = filtered["date"].max()
start_date = max_date - pd.Timedelta(days=days)
filtered = filtered[filtered["date"] >= start_date]

if filtered.empty:
    st.warning("No data found for selected time period.")
    st.stop()


# =========================
# LATEST DATA
# =========================
latest = (
    filtered.sort_values(["date", "timestamp"])
    .groupby(["platform", "product_id", "product_name", "location"], dropna=False)
    .tail(1)
)


# =========================
# KPI CARDS
# =========================
lowest_price = latest["sp_price"].min()
highest_price = latest["sp_price"].max()
avg_price = latest["sp_price"].mean()
total_products = latest["product_name"].nunique()

lowest_row = latest.loc[latest["sp_price"].idxmin()]
highest_row = latest.loc[latest["sp_price"].idxmax()]

k1, k2, k3, k4 = st.columns(4)

k1.metric("Lowest Price", f"₹{lowest_price:,.0f}", lowest_row["platform"])
k2.metric("Highest Price", f"₹{highest_price:,.0f}", highest_row["platform"])
k3.metric("Average Price", f"₹{avg_price:,.0f}")
k4.metric("Products Tracked", total_products)

st.divider()


# =========================
# ONE PAGE LAYOUT
# =========================
left, right = st.columns([1.25, 1])


# =========================
# TABLE
# =========================
with left:
    st.subheader("🛒 Current Channel Price Comparison")

    display_df = latest[
        [
            "platform",
            "brand",
            "product_name",
            "product_id",
            "sp_price",
            "rating",
            "location"
        ]
    ].copy()

    display_df.columns = [
        "Platform",
        "Brand",
        "Product Name",
        "Product ID",
        "Selling Price",
        "Rating",
        "Location"
    ]

    st.dataframe(
        display_df.sort_values("Selling Price"),
        use_container_width=True,
        hide_index=True,
        height=260
    )


# =========================
# BAR CHART
# =========================
with right:
    st.subheader("📊 Avg Price by Channel")

    platform_avg = (
        latest.groupby("platform", as_index=False)["sp_price"]
        .mean()
        .sort_values("sp_price")
    )

    fig_bar = px.bar(
        platform_avg,
        x="platform",
        y="sp_price",
        text="sp_price",
        color="platform",
        color_discrete_map=CHANNEL_COLORS
    )

    fig_bar.update_traces(texttemplate="₹%{text:.0f}", textposition="outside")
    fig_bar.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Channel",
        yaxis_title="Avg Price",
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    
# =========================
# RATING CHART
# =========================
st.subheader("⭐ Average Rating by Channel")

rating_df = latest.dropna(subset=["rating"]).copy()

if rating_df.empty:
    st.info("No rating data available for selected filters.")
else:
    rating_avg = (
        rating_df.groupby("platform", as_index=False)["rating"]
        .mean()
        .sort_values("rating", ascending=False)
    )

    fig_rating = px.bar(
        rating_avg,
        x="platform",
        y="rating",
        text="rating",
        color="platform",
        color_discrete_map=CHANNEL_COLORS
    )

    fig_rating.update_traces(texttemplate="%{text:.1f} ⭐", textposition="outside")

    fig_rating.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Channel",
        yaxis_title="Average Rating",
        yaxis=dict(range=[0, 5]),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_rating, use_container_width=True)


# =========================
# LINE CHART
# =========================
st.subheader(f"📈 Price Trend - Last {days} Days")

fig_line = px.line(
    filtered.sort_values("date"),
    x="date",
    y="sp_price",
    color="platform",
    markers=True,
    color_discrete_map=CHANNEL_COLORS,
    hover_data=[
        "brand",
        "product_name",
        "product_id",
        "location",
        "rating",
        "rank",
        "is_ad"
    ]
)

fig_line.update_layout(
    height=420,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Date",
    yaxis_title="Selling Price",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_line, use_container_width=True)


# =========================
# ALERTS + CHEAPEST
# =========================
a1, a2 = st.columns([1, 1])

with a1:
    st.subheader("🚨 Price Change Alerts")

    alert_df = filtered.sort_values(
        ["platform", "product_name", "location", "date"]
    ).copy()

    alert_df["previous_price"] = alert_df.groupby(
        ["platform", "product_name", "location"]
    )["sp_price"].shift(1)

    alert_df["price_change"] = alert_df["sp_price"] - alert_df["previous_price"]

    alerts = alert_df[
        (alert_df["price_change"] >= 20)
        | (alert_df["price_change"] <= -20)
    ]

    if alerts.empty:
        st.success("No major price change found.")
    else:
        alert_show = alerts[
            [
                "date",
                "platform",
                "brand",
                "product_name",
                "location",
                "previous_price",
                "sp_price",
                "price_change"
            ]
        ].sort_values("date", ascending=False)

        st.dataframe(alert_show, use_container_width=True, hide_index=True, height=250)

with a2:
    st.subheader("🏆 Cheapest Channel")

    cheapest = latest.sort_values("sp_price").head(5)

    cheapest_show = cheapest[
        [
            "platform",
            "brand",
            "product_name",
            "product_id",
            "sp_price",
            "location"
        ]
    ].copy()

    cheapest_show.columns = [
        "Platform",
        "Brand",
        "Product Name",
        "Product ID",
        "Price",
        "Location"
    ]

    st.dataframe(cheapest_show, use_container_width=True, hide_index=True, height=250)


# =========================
# DOWNLOAD
# =========================
st.download_button(
    label="⬇ Download Filtered Data",
    data=filtered.to_csv(index=False),
    file_name="pricing_dashboard_filtered_data.csv",
    mime="text/csv"
)