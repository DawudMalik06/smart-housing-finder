# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import streamlit as st

# # Load data
# df = pd.read_csv("data/housing_insights.csv")

# st.title("📊 Data Insights")
# st.markdown("Explore key statistics across Sheffield housing areas:")
# st.write(df.head())  # Optional debug check

# # Plotting
# sns.set(style="whitegrid")
# fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# sns.barplot(x="Avg Rent (£)", y="Area", data=df, ax=axs[0, 0], palette="Blues_d")
# axs[0, 0].set_title("Average Rent by Area")

# sns.barplot(x="Transport Score", y="Area", data=df, ax=axs[0, 1], palette="Greens_d")
# axs[0, 1].set_title("Public Transport Accessibility")

# sns.barplot(x="Energy Rating A-B (%)", y="Area", data=df, ax=axs[1, 0], palette="Oranges_d")
# axs[1, 0].set_title("Energy-Efficient Homes")

# sns.barplot(x="Smart Homes (%)", y="Area", data=df, ax=axs[1, 1], palette="Purples_d")
# axs[1, 1].set_title("Smart Feature Adoption")

# plt.tight_layout()
# st.pyplot(fig)
