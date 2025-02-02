import seaborn as sns
import matplotlib.pyplot as plt

def generate_basic_analysis_cost_latency(data, model_type):
    # Create a figure with 3 subplots arranged in a grid (2 rows, 2 columns)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # Adjust figure size as needed

    # Plot 1: Histogram of total_cost
    sns.histplot(data=data, x="total_cost", hue="code_type", ax=axes[0, 0])
    axes[0, 0].set_title("Histogram of Total Cost by Code Type")
    axes[0, 0].set_xlabel("Total Cost ($)")
    axes[0, 0].set_ylabel("Frequency")

    # Plot 2: Scatter plot of input tokens vs total_cost
    sns.scatterplot(data=data, x="input_tokens", y="total_cost", ax=axes[0, 1], label="Input")
    sns.scatterplot(data=data, x="output_tokens", y="total_cost", ax=axes[0, 1], label="Output")
    axes[0, 1].legend()
    axes[0, 1].set_title("Tokens vs Total Cost")
    axes[0, 1].set_xlabel("Tokens")
    axes[0, 1].set_ylabel("Total Cost ($)")

    # Plot 3: Histogram of process_time
    sns.histplot(data=data, x="process_time", hue="code_type", ax=axes[1, 0])
    axes[1, 0].set_title("Histogram of Process Time by Code Type")
    axes[1, 0].set_xlabel("Process Time (s)")
    axes[1, 0].set_ylabel("Frequency")

    # Plot 4: Scatter plot of output tokens vs total cost
    sns.scatterplot(data=data, x="input_tokens", y="process_time", ax=axes[1, 1], label="Input")
    sns.scatterplot(data=data, x="output_tokens", y="process_time", ax=axes[1, 1], label="Output")
    axes[1, 1].legend()
    axes[1, 1].set_title("Tokens vs Process time")
    axes[1, 1].set_xlabel("Tokens")
    axes[1, 1].set_ylabel("Process Time (s)")

    # Add an overall title for the figure
    fig.suptitle(f"Analysis of Total Cost and Process Time ({model_type})", fontsize=16)

    # Adjust layout for better spacing
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for the overall title
    return fig
