import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from spatial import PointSet

# ---------------------------------------------------------------------------
# File Paths
# ---------------------------------------------------------------------------
DATA_PATH = "../data/points.csv"
OUTPUT_DIR = "../output"
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "lab2_report.json")
PLOT_PATH = os.path.join(OUTPUT_DIR, "lab2_preview.png")

"""
    Set a value for FILTER_TAG if you want to filter the points using a specific tag.
    Doing so will also affect the output scatter plot and JSON file.
    By default, the value is empty and will plot the entire point set.

    Sample usage:
        FILTER_TAG = "poi" 
"""
FILTER_TAG = ""

# Create PointSet object from CSV
point_set = PointSet.from_csv(DATA_PATH)

if(FILTER_TAG):
    print(f"\nA filter has been set. Value is \'{FILTER_TAG}\'")
else:
    print(f"\nNo filters set.")

# Add filtering if a value has been set to the FILTER_TAG variable
filtered_points = point_set.filter_by_tag(FILTER_TAG)

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create scatter plot of valid coordinates
print(f"\nBuilding scatter plot...")
plt.figure()
if(filtered_points.count()>0):      # Plot filtered points if it exists
    for point in filtered_points.points:
        plt.scatter(point.lon, point.lat, label=point.name)
else:                               # Plot unfiltered pointset otherwise
    if(point_set.bbox() is None):
        plt.title("Preview Plot (No valid coordinates to plot)")
    else:
        for point in point_set.points:
            plt.scatter(point.lon, point.lat, label=point.name)
        plt.title("PointSet Preview (Longitude vs Latitude)")

plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Save the plot to the output directory
plt.savefig(PLOT_PATH, dpi=150, bbox_inches="tight")
plt.close()

print(f"Saved scatter plot to {PLOT_PATH}")

# For the optional part of summary report
unique_tags = {point.tag for point in point_set.points} # Set will automatically remove all duplicates
unique_tags_list = list(unique_tags)                    # Convert set to list

# Create a list of counts per unique tag
count = []
for tag in unique_tags_list:
    i = 0
    for point in point_set.points:
        if point.tag == tag:
            i+=1
    count.append(int(i))

# Create a pandas DataFrame of the unique tags and count
tag_df = pd.DataFrame({'tag': unique_tags_list, 'count': count})

#Build summary dictionary
print(f"Building summary dictionary...")
if(filtered_points.count()>0):  # Build summary dictionary of filtered points
    summary = {
        "file": DATA_PATH,
        "tag": FILTER_TAG,
        "total_points": filtered_points.count(),
        "bounding_box": filtered_points.bbox(),
    }
else:                           # Otherwise, build summary dictionary of original points
    summary = {
        "file": DATA_PATH,
        "total_points": point_set.count(),
        "bounding_box": point_set.bbox(),
        "count_per_unique_tag": tag_df.set_index('tag')['count'].to_dict(),
    }

# Write summary to JSON file
with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(f"Saved summary to {SUMMARY_PATH}")