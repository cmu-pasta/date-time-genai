import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Set up paths using config-style approach
SCRIPT_DIR = Path(__file__).parent
RELIABILITY_FILE = SCRIPT_DIR / "reliability_results.tsv"
DIVERGENCE_FILE = SCRIPT_DIR / "divergence_results.tsv"
SAVE_PATH = SCRIPT_DIR / "figures/"

# Create figures directory if it doesn't exist
SAVE_PATH.mkdir(exist_ok=True)

# define the colors for the bar chart
from matplotlib.colors import to_rgb

colors = ["#80c2c2"]
darker_colors = ["#166666"]

sns.set_theme(style="white")


def read_and_process_data():
    """Read both TSV files and merge their data."""

    # Read reliability results
    reliability_df = pd.read_csv(RELIABILITY_FILE, sep="\t")
    reliability_df["Source"] = "Reliability"

    # Read divergence results
    divergence_df = pd.read_csv(DIVERGENCE_FILE, sep="\t")
    divergence_df["Source"] = "Divergence"

    # Merge the dataframes
    merged_df = pd.concat([reliability_df, divergence_df], ignore_index=True)

    print(
        f"Loaded {len(reliability_df)} reliability records and {len(divergence_df)} divergence records"
    )
    print(f"Total merged records: {len(merged_df)}")

    return merged_df


def create_category_bar_chart(df):
    """Create a styled bar chart showing category distribution."""

    # Group by Category and Source to get counts
    category_counts = df.groupby(["Category", "Source"]).size().unstack(fill_value=0)

    # Sort by total counts (descending for better visualization)
    category_counts["Total"] = category_counts.sum(axis=1)
    category_counts = category_counts.sort_values("Total", ascending=True).drop(
        columns=["Total"]
    )

    print("\nCategory distribution:")
    print(category_counts)

    # Assign colors for each source type
    bar_colors = []
    for i in range(len(category_counts)):
        bar_colors.append(
            (darker_colors[i % len(darker_colors)], colors[i % len(colors)])
        )

    # Plotting the stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, (source_type, color_pair) in enumerate(
        zip(category_counts.columns, zip(*bar_colors))
    ):
        ax.barh(
            category_counts.index,
            category_counts.iloc[:, i],
            label=source_type,
            color=color_pair,
            height=0.85,
            edgecolor="white",
            align="center",
            left=category_counts.iloc[:, :i].sum(axis=1) if i > 0 else None,
        )

    # Adding data labels
    for container in ax.containers:
        labels = [
            f"{int(value)}" if value > 0 else "" for value in container.datavalues
        ]
        ax.bar_label(
            container,
            labels=labels,
            label_type="center",
            color="white",
            fontsize=14,
            fontweight="bold",
        )

    # Customizing the chart
    ax.set_xlabel(
        "\nNumber of Differentiating Code Pairs", fontsize=18, fontweight="bold"
    )
    ax.set_ylabel("Categories\n", fontsize=18, fontweight="bold")
    ax.legend(
        ["Datetime vs Pendulum", "Datetime vs Datetime"],
        title="Source Type",
        fontsize=14,
        title_fontsize=14,
        loc="lower right",
    )

    # Adjusting ticks
    ax.tick_params(axis="x", labelsize=16)
    ax.tick_params(axis="y", labelsize=16, length=0)

    # Display and save the chart
    plt.tight_layout()

    # Save as PDF
    save_file_pdf = SAVE_PATH / "merged_categories_distribution.pdf"
    plt.savefig(save_file_pdf, bbox_inches="tight")
    print(f"\nChart saved to: {save_file_pdf}")

    plt.show()


def plot_merged_categories():
    """
    Main function to create merged categories plot.
    This function can be called from run.py as part of the analysis pipeline.
    """
    print("Reading and processing TSV files...")
    merged_df = read_and_process_data()

    print("\nCreating stacked bar chart by source type...")
    create_category_bar_chart(merged_df)

    print("\nMerged categories analysis complete!")


def main():
    """Main function to orchestrate the analysis."""
    plot_merged_categories()


if __name__ == "__main__":
    main()
