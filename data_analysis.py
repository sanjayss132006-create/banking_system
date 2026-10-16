
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# 1. Load data from REST API
url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url, timeout=20)
response.raise_for_status()
data = response.json()

print("API data loaded successfully!")

# 2. Convert JSON into DataFrame
df = pd.DataFrame(data)
print("\nOriginal Data:")
print(df.head())

# 3. Data Cleaning
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df["title"] = df["title"].str.strip()
df["body"] = df["body"].str.strip()
df = df[(df["title"] != "") & (df["body"] != "")]

# 4. Data Manipulation
df["title_length"] = df["title"].str.len()
df["word_count"] = df["body"].str.split().str.len()

print("\nCleaned Data:")
print(df.head())

# 5. NumPy Analysis
lengths = np.array(df["title_length"])
print("\nData Analysis:")
print("Total Posts:", len(df))
print("Average Title Length:", np.mean(lengths))
print("Maximum Title Length:", np.max(lengths))
print("Minimum Title Length:", np.min(lengths))

# 6. Pandas Analysis
print("\nPosts by User:")
user_posts = df.groupby("userId").size()
print(user_posts)

# 7. Data Visualization
sns.set_theme(style="whitegrid")
user_posts.plot(kind="bar", figsize=(10, 5))
plt.title("Number of Posts by User")
plt.xlabel("User ID")
plt.ylabel("Number of Posts")
plt.tight_layout()
plt.savefig("user_posts.png")
plt.show()

# 8. Save cleaned dataset
df.to_csv("cleaned_data.csv", index=False)

# 9. Generate report
report = {
    "total_posts": int(len(df)),
    "average_title_length": float(np.mean(lengths)),
    "maximum_title_length": int(np.max(lengths)),
    "minimum_title_length": int(np.min(lengths)),
    "total_users": int(df["userId"].nunique())
}

with open("analysis_report.json", "w") as file:
    json.dump(report, file, indent=4)

print("\nFinal Report:")
print(json.dumps(report, indent=4))
print("\nProject completed successfully!")
print("Files saved: cleaned_data.csv, analysis_report.json, user_posts.png")