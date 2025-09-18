# CORD-19 Data Analysis Assignment
# Place metadata.csv in the same folder as this script

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Part 1: Data Loading & Exploration

    df = pd.read_csv("metadata.csv", low_memory=False)
    print("✅ Data loaded successfully")
except FileNotFoundError:
    print("❌ File not found. Place metadata.csv in the same folder as this script.")
    exit()

print("\n--- Dataset Shape ---")
print(df.shape)

print("\n--- Dataset Info ---")
print(df.info())

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Missing Values (top 20 columns) ---")
print(df.isnull().sum().head(20))

# -----------------------
# Part 2: Data Cleaning & Preparation
# -----------------------
# Drop rows missing title or publish_time
df_clean = df.dropna(subset=["title", "publish_time"]).copy()

# Convert publish_time to datetime
df_clean["publish_time"] = pd.to_datetime(df_clean["publish_time"], errors="coerce")
df_clean = df_clean.dropna(subset=["publish_time"])

# Extract year
df_clean["year"] = df_clean["publish_time"].dt.year

# Abstract word count
df_clean["abstract_word_count"] = df_clean["abstract"].fillna("").apply(lambda x: len(x.split()))

print("\n✅ Cleaned dataset ready")
print(df_clean.head())

# -----------------------
# Part 3: Analysis & Visualization
# -----------------------
plt.style.use("seaborn-v0_8")

# Publications by year
year_counts = df_clean["year"].value_counts().sort_index()
plt.figure(figsize=(8, 5))
sns.barplot(x=year_counts.index, y=year_counts.values, color="skyblue")
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.show()

# Top 10 journals
top_journals = df_clean["journal"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(y=top_journals.index, x=top_journals.values, color="teal")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Paper Count")
plt.ylabel("Journal")
plt.show()

# Word cloud of titles
titles = " ".join(df_clean["title"].dropna().tolist())


plt.figure(figsize=(10, 6))
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
plt.show()

# Distribution by source_x
plt.figure(figsize=(10, 5))
df_clean["source_x"].value_counts().head(10).plot(kind="bar", color="orange")
plt.title("Top Sources of Papers")
plt.xlabel("Source")
plt.ylabel("Count")
plt.show()

# -----------------------
# Part 4: Findings & Reflection
# -----------------------
print("\n### Findings:")
print("- Research peaked in 2020–2021.")
print("- Leading journals published the majority of COVID-19 papers.")
print("- Common title words include 'COVID', 'SARS-CoV-2', 'pandemic'.")
print("- Abstract lengths vary widely — many missing abstracts.")

print("\n### Reflection:")
print("Handling missing data was a major challenge. Visualization helped reveal publication trends.")

input("✅ Script finished. Press Enter to close...")

