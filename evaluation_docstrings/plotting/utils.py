import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from evaluation_docstrings.task.utils import assemble_cohen_kappa
from evaluation_docstrings.llm.config import costs


def generate_cohen_kappa_plot(evaluation_result_df, model_name):
    cohen_kappa = assemble_cohen_kappa(
        evaluation_result_df,
        scores_columns={
            "accuracy_score": "gt_accuracy_score",
            "clarity_score": "gt_clarity_score",
            "coverage_score": "gt_coverage_score",
        },
    )
    cohen_kappa = pd.Series(
        cohen_kappa, index=["accuracy_score", "clarity_score", "coverage_score"]
    )
    cohen_kappa = cohen_kappa.reindex(
        ["accuracy_score", "clarity_score", "coverage_score"]
    )
    plt.barh(cohen_kappa.index, cohen_kappa.values)
    plt.xlabel("Cohen Kappa")
    plt.title(f"Evaluation Cohen Kappa ({model_name})")
    plt.savefig(f"{model_name}_cohen_kappa.png")


def generate_basic_analysis_cost_latency(data, model_name):
    # Create a figure with 3 subplots arranged in a grid (2 rows, 2 columns)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # Adjust figure size as needed

    # Plot 1: Histogram of total_cost
    sns.histplot(data=data, x="total_cost", hue="code_type", ax=axes[0, 0])
    axes[0, 0].set_title(
        "Histogram of Total Cost by Code Type, Overall mean /1000 calls: ${:.3f}".format(
            1000 * data["total_cost"].mean()
        )
    )
    axes[0, 0].set_xlabel("Total Cost ($)")
    axes[0, 0].set_ylabel("Frequency")

    # Plot 2: Scatter plot of input tokens vs total_cost
    data["input_cost"] = data["input_tokens"] * costs[model_name]["input"] / 1e6
    data["fraction_cost_input"] = data["input_cost"] / data["total_cost"]
    sns.histplot(data=data, x="fraction_cost_input", ax=axes[0, 1])
    axes[0, 1].set_title("Histogram of fraction input cost")
    axes[0, 1].set_xlabel("Fraction cost on input")
    axes[0, 1].set_ylabel("Frequency")

    # Plot 3: Histogram of process_time
    sns.histplot(data=data, x="process_time", hue="code_type", ax=axes[1, 0])
    axes[1, 0].set_title(
        "Histogram of Process Time by Code Type. Overall mean: {:.3f}s".format(
            data["process_time"].mean()
        )
    )
    axes[1, 0].set_xlabel("Process Time (s)")
    axes[1, 0].set_ylabel("Frequency")

    # Plot 4: Scatter plot of output tokens vs total cost
    data.plot.scatter(
        y="total_cost", x="process_time", c="fraction_cost_input", ax=axes[1, 1]
    )
    axes[1, 1].legend()
    axes[1, 1].set_title("Process time vs. Total Cost")
    axes[1, 1].set_xlabel("Process time (s)")
    axes[1, 1].set_ylabel("Total cost ($)")

    # Add an overall title for the figure
    fig.suptitle(f"Analysis of Total Cost and Process Time ({model_name})", fontsize=16)

    # Adjust layout for better spacing
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for the overall title
    return fig


def generate_scores_barplot_dataset(scores_df, id_cols):
    melted_df = scores_df.melt(
        id_vars=id_cols,
        value_name="score",
        value_vars=[c for c in scores_df if c not in id_cols],
        var_name="score_type",
    )
    totals = (
        melted_df.groupby(["score_type", "code_type"])
        .agg({"score": "sum", "code_name": "count"})
        .reset_index()
        .rename(columns={"code_name": "total"})
    )
    totals["fraction"] = totals["score"] / totals["total"]
    return totals
