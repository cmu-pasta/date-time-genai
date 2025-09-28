import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Improved regex: status can contain letters, digits, underscores and hyphens (case insensitive).
PATTERN = re.compile(r":\s*([a-z0-9_-]+)\s*\(\s*([\d.]+)\s*%\s*\)")
ALLOWED_STATUSES = {"differentiating", "non-differentiating"}


def get_available_model_runs(log_filename: str) -> List[Tuple[str, str]]:
    """
    Automatically discover available model runs and return their log file paths and labels.

    Args:
        log_filename: Name of the log file to look for (e.g., "dt_vs_dt_result_log.txt")

    Returns:
        List of tuples (file_path, label) for each available model run
    """
    results_dir = Path(config.OUTPUT_DIR_PATH)
    model_runs = []

    if not results_dir.exists():
        print(f"Warning: Results directory {results_dir} does not exist.")
        return model_runs

    # Look for run_* directories
    for run_dir in results_dir.glob("run_*"):
        if run_dir.is_dir():
            # Extract model name from directory name
            model_name = run_dir.name.replace("run_", "")

            # Construct log file path using original template (not the modified config)
            # Use the original template to avoid issues when config.LOGS_DIR is modified by run.py
            original_logs_dir_template = "./results/run_{ai_model}/.logs/"
            logs_dir_path = original_logs_dir_template.format(ai_model=model_name)
            logs_dir = Path(logs_dir_path)
            log_file = logs_dir / log_filename

            if log_file.exists():
                # Create a human-readable label from the model name
                label = format_model_label(model_name)
                model_runs.append((str(log_file), label))
            else:
                print(f"Warning: Log file not found for {model_name}: {log_file}")

    return sorted(model_runs, key=lambda x: x[1])  # Sort by label


def format_model_label(model_name: str) -> str:
    """
    Convert model name to a human-readable label.

    Args:
        model_name: Raw model name from directory (e.g., 'gpt-5', 'claude-sonnet-4-20250514')

    Returns:
        Formatted label for display
    """
    # Handle common model name patterns
    if model_name.startswith("gpt"):
        return model_name.upper().replace("-", "-")
    elif model_name.startswith("claude"):
        return "Claude Sonnet 4"
    elif model_name.startswith("gemini"):
        return "Gemini 2.5 Flash"
    else:
        # Generic formatting: capitalize and replace hyphens with spaces
        return model_name.replace("-", " ").title()


def extract_percentages_from_file(path: Path) -> List[float]:
    percents = []
    total_lines = matched = skipped = 0
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            total_lines += 1
            line = line.lower()  # Convert to lowercase
            m = PATTERN.search(line)
            if not m:
                skipped += 1
                continue
            matched += 1
            status, pct_str = m.groups()
            status = status.lower().strip()
            if status in ALLOWED_STATUSES:
                try:
                    percents.append(float(pct_str))
                except ValueError:
                    pass
    print(
        f"{path.name}: total={total_lines}, matched={matched}, kept={len(percents)}, skipped={skipped}"
    )
    return sorted(percents)


def make_step_cdf(
    pcts: List[float], x_start: float = 0.0, x_end: float = 100.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Given sorted percentages, return x and y arrays ready for plt.step(..., where='post')
    with a starting point at (x_start, 0) and an ending point at (x_end, last_count).
    """
    if len(pcts) == 0:
        return np.array([]), np.array([])
    x = np.array(sorted(pcts), dtype=float)
    # clamp to [x_start, x_end] just in case
    x = np.clip(x, x_start, x_end)
    y = np.arange(1, len(x) + 1)
    x_ext = np.concatenate(([x_start], x, [x_end]))
    y_ext = np.concatenate(([0], y, [y[-1]]))
    return x_ext, y_ext


def get_model_color(label: str) -> str:
    """
    Get the appropriate logo color for each model.

    Args:
        label: Model label (e.g., 'GPT-5', 'Claude Sonnet 4', 'Gemini 2.5 Flash')

    Returns:
        Hex color code matching the model's logo color
    """
    if "GPT" in label.upper():
        return "#10A37F"  # OpenAI green
    elif "CLAUDE" in label.upper():
        return "#CC785C"  # Anthropic orange-brown
    elif "GEMINI" in label.upper():
        return "#4285F4"  # Google blue
    else:
        return "#166666"  # Default teal color


def plot_three_logs(
    file_paths: List[str],
    labels: List[str],
    figsize=(12, 6),
    save_path: str = None,
    show_vertical_line: bool = True,
):
    assert len(file_paths) == len(labels), "file_paths and labels must match in length."

    # Set up the default matplotlib style
    plt.style.use("default")

    # Create figure with clean styling
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    ax.set_facecolor("white")

    # Use model-specific logo colors
    colors = [get_model_color(label) for label in labels]
    linestyles = ["-", "--", "-.", ":", "-", "--"]

    for i, (fp, lab) in enumerate(zip(file_paths, labels)):
        p = Path(fp)
        if not p.exists():
            print(f"Warning: {fp} does not exist — skipping.")
            continue

        pcts = extract_percentages_from_file(p)
        if len(pcts) == 0:
            print(
                f"Note: {fp} contains no differentiating/non-differentiating entries."
            )
            continue

        x, y = make_step_cdf(pcts, x_start=0.0, x_end=100.0)

        # Plot with refined styling for better visual appeal
        ax.step(
            x,
            y,
            where="post",
            linestyle=linestyles[i % len(linestyles)],
            linewidth=2,
            color=colors[i],
            label=f"{lab} (n={len(pcts)})",
            alpha=0.9,
        )

    # Refined styling with more balanced font sizes
    ax.set_xlabel(
        "\nPercentage of inputs with differing behavior (P)",
        size=18,
        fontweight="bold",
    )
    ax.set_ylabel("Number of Code Pairs\n", size=18, fontweight="bold")

    # Clean grid styling
    ax.grid(True, linestyle="--", alpha=0.3, linewidth=0.8)
    ax.set_axisbelow(True)

    # Add vertical line at 75% (without legend entry) - only for reliability plots
    if show_vertical_line:
        ax.axvline(x=75, color="red", linestyle="-", linewidth=2, alpha=0.7)

    # Clean legend styling in top left corner
    legend = ax.legend(
        frameon=True,
        fontsize=14,
        loc="upper left",
        framealpha=0.9,
        facecolor="white",
    )
    # Make legend text bold
    for text in legend.get_texts():
        text.set_fontweight("bold")

    # Set limits with padding for better visibility
    ax.set_xlim(-2, 102)  # Add 2% padding on both sides
    ax.set_ylim(0)  # allow matplotlib to auto-scale upper y

    # Refined tick styling with more balanced font sizes
    ax.tick_params(axis="x", labelsize=16)
    ax.tick_params(axis="y", labelsize=16)

    plt.tight_layout()

    if save_path:
        # Save as PDF
        pdf_path = save_path.replace(".png", ".pdf")
        plt.savefig(pdf_path, transparent=True, bbox_inches="tight")
        print(f"Saved figure to {pdf_path}")

    plt.show()


def plot_models_reliability():
    """
    Automatically discover and plot reliability data for all available model runs.
    Uses dt_vs_dt_result_log.txt files.
    Uses config.py to dynamically compute log file paths.
    Saves the plot to ./analyze/figures/model_reliability_comparison.png
    """
    # Automatically discover available model runs
    model_runs = get_available_model_runs("dt_vs_dt_result_log.txt")

    if not model_runs:
        print("No model runs found. Please check that:")
        print(f"1. Results directory exists: {config.OUTPUT_DIR_PATH}")
        print("2. Model run directories exist (format: run_<model_name>)")
        print("3. Log files exist at: <run_dir>/.logs/dt_vs_dt_result_log.txt")
        return

    files = [file_path for file_path, _ in model_runs]
    labels = [label for _, label in model_runs]

    print(f"Found {len(model_runs)} model runs:")
    for file_path, label in model_runs:
        print(f"  - {label}: {file_path}")

    # Create figures directory if it doesn't exist and set save path
    figures_dir = Path("./analyze/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)
    save_path = str(figures_dir / "model_reliability_comparison.png")

    plot_three_logs(files, labels, save_path=save_path)


def plot_models_divergence():
    """
    Automatically discover and plot divergence data for all available model runs.
    Uses dt_vs_pendulum_result_log.txt files.
    Uses config.py to dynamically compute log file paths.
    Saves the plot to ./analyze/figures/model_divergence_comparison.png
    """
    # Automatically discover available model runs for pendulum logs
    model_runs = get_available_model_runs("dt_vs_pendulum_result_log.txt")

    if not model_runs:
        print("No model runs found. Please check that:")
        print(f"1. Results directory exists: {config.OUTPUT_DIR_PATH}")
        print("2. Model run directories exist (format: run_<model_name>)")
        print("3. Log files exist at: <run_dir>/.logs/dt_vs_pendulum_result_log.txt")
        return

    files = [file_path for file_path, _ in model_runs]
    labels = [label for _, label in model_runs]

    print(f"Found {len(model_runs)} model runs:")
    for file_path, label in model_runs:
        print(f"  - {label}: {file_path}")

    # Create figures directory if it doesn't exist and set save path
    figures_dir = Path("./analyze/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)
    save_path = str(figures_dir / "model_divergence_comparison.png")

    plot_three_logs(files, labels, save_path=save_path, show_vertical_line=False)
