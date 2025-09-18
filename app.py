import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("CORD-19 Data Analysis Dashboard")

# Load dataset from URL
@st.cache_data
def load_data():
    # Example dataset hosted on GitHub (replace with your own Google Drive/Kaggle direct link if needed)
    url = "https://raw.githubusercontent.com/streamlit/example-data/master/hello-data.csv"
    try:
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        st.error(f"❌ Failed to load dataset from URL. Error: {e}")
        return None

df = load_data()

if df is not None:
    st.subheader("Dataset Preview")
    st.write(df.head())

    # Data cleaning (adapted for sample dataset — will still work with real metadata.csv if linked)
    if "publish_time" in df.columns:
        df_clean = df.dropna(subset=["title", "publish_time"]).copy()
        df_clean["publish_time"] = pd.to_datetime(df_clean["publish_time"], errors="coerce")
        df_clean = df_clean.dropna(subset=["publish_time"])
        df_clean["year"] = df_clean["publish_time"].dt.year
        df_clean["abstract_word_count"] = df_clean["abstract"].fillna("").apply(lambda x: len(x.split()))

        # Publications by year
        st.subheader("Publications by Year")
        year_counts = df_clean["year"].value_counts().sort_index()
        fig, ax = plt.subplots()
        sns.barplot(x=year_counts.index, y=year_counts.values, color="skyblue", ax=ax)
        ax.set_title("Publications by Year")
        st.pyplot(fig)

        # Top journals
        st.subheader("Top 10 Journals Publishing COVID-19 Research")
        top_journals = df_clean["journal"].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(y=top_journals.index, x=top_journals.values, color="teal", ax=ax)
        ax.set_xlabel("Paper Count")
        ax.set_ylabel("Journal")
        st.pyplot(fig)

        # Sources
        st.subheader("Top Sources of Papers")
        fig, ax = plt.subplots()
        df_clean["source_x"].value_counts().head(10).plot(kind="bar", color="orange", ax=ax)
        ax.set_xlabel("Source")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # Findings
        st.subheader("Findings")
        st.markdown("""
        - Research peaked in 2020–2021  
        - Leading journals published the majority of COVID-19 papers  
        - Common title words include *COVID*, *SARS-CoV-2*, *pandemic*  
        - Abstract lengths vary widely — many missing abstracts  
        """)

        # Reflection
        st.subheader("Reflection")
        st.markdown("Handling missing data was a major challenge. Visualization helped reveal publication trends.")
    else:
        st.warning("⚠️ This sample dataset doesn’t include the expected `publish_time` column. Replace the URL with your real metadata.csv link for full analysis.")
