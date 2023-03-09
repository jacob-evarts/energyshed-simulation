import agentpy as ap
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import seaborn as sns


def status_stackplot(data, ax):
    """Stackplot of people's condition over time."""
    x = data.index.get_level_values("t")
    y = [data[var] for var in ["store", "buy", "sell"]]

    color_map = {"labels": ["store", "buy", "sell"], "colors": ["blue", "orange", "green"]}
    ax.stackplot(x, y, **color_map)

    ax.legend()
    ax.set_xlim(0, max(1, len(x) - 1))
    ax.set_ylim(0, 1)
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Percentage of population")
    ax.set_title("Proportion of agents taking each action")


def cost_lineplot(data, ax):
    x = data.index.get_level_values("t")[1:]
    y = -data["daily_cost"][1:]

    ax.plot(x, y)
    # Fit a linear regression model
    coeffs = np.polyfit(x, y, 1)
    m = coeffs[0]
    b = coeffs[1]

    # Plot the regression line
    ax.plot(x, m * x + b, color="black", linestyle="--")

    ax.legend()
    ax.set_xlim(0, max(1, len(x) - 1))
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Daily cost (arbitrary units)")


def transfer_lineplot(data, ax):
    x = data.index.get_level_values("t")[1:]
    local = data["local_transfer"][1:]
    grid = data["grid_transfer"][1:]

    sns.set()
    ax.plot(x, local, label="Local transfer")
    ax.plot(x, grid, label="Grid transfer")

    ax.legend()
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Daily energy sources (arbitrary units)")


def reward_lineplot(data, ax):
    x = data.index.get_level_values("t")[1:]
    y = data["reward"][1:]

    ax.plot(x, y)
    # Fit a linear regression model
    coeffs = np.polyfit(x, y, 1)
    m = coeffs[0]
    b = coeffs[1]

    # Plot the regression line
    ax.plot(x, m * x + b, color="black", linestyle="--")

    ax.legend()
    ax.set_xlim(0, max(1, len(x) - 1))
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Reward (arbitrary units)")


def animation_plot(model, ax):
    group_grid = model.network.attr_grid("status")
    color_dict = {-1: "orange", 0: "blue", 1: "green"}
    action_dict = {"buy": "orange", "sell": "green", "store": "blue"}
    cmap = colors.ListedColormap([color_dict[key] for key in color_dict])
    ap.gridplot(group_grid, cmap=cmap, ax=ax)

    # Create legend
    legend_handles = [
        mpatches.Patch(color=color, label=label) for label, color in action_dict.items()
    ]
    ax.legend(handles=legend_handles)

    ax.set_title(f"Energyshed model \n Time-step: {model.t} Weather: {model.weather}")


def q_values_plot(i, q_values):
    # Extract the state and action spaces from the q-values
    state_space = sorted(set([key[0] for q_values in q_values for key in q_values.keys()]))
    action_space = sorted(set([key[1] for q_values in q_values for key in q_values.keys()]))
    q_values = q_values[i]
    # Create an empty matrix to hold the q-values
    q_values_matrix = np.zeros((len(state_space), len(action_space)))
    for j, state in enumerate(state_space):
        for k, action in enumerate(action_space):
            q_values_matrix[j, k] = q_values.get((state, action), 0)

    value_map = {-1: "Neg. energy bal.", 0: "Zero energy bal.", 1: "Pos. energy bal."}
    state_space_labels = [
        (value_map[energy], weather, store) for energy, weather, store in state_space
    ]
    # Clear the previous plot and plot the new heat map
    plt.clf()
    sns.heatmap(
        q_values_matrix,
        annot=True,
        fmt=".3g",
        xticklabels=action_space,
        yticklabels=state_space_labels,
        norm=colors.Normalize(vmin=-50, vmax=10),
    )
