import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors
import agentpy as ap
import numpy as np


def status_stackplot(data, ax):
    """Stackplot of people's condition over time."""
    x = data.index.get_level_values("t")
    y = [data[var] for var in ["store", "buy", "sell"]]

    color_map = {"labels": ["store", "buy", "sell"], "colors": ["b", "r", "g"]}
    ax.stackplot(x, y, **color_map)

    ax.legend()
    ax.set_xlim(0, max(1, len(x) - 1))
    ax.set_ylim(0, 1)
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Percentage of population")


def cost_lineplot(data, ax):
    """Stackplot of people's condition over time."""
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
    """Stackplot of people's condition over time."""
    x = data.index.get_level_values("t")[1:]
    local = data["local_transfer"][1:]
    grid = data["grid_transfer"][1:]

    sns.set()
    ax.plot(x, local, label="Local transfer")
    ax.plot(x, grid, label="Grid transfer")

    ax.legend()
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Daily energy sources (arbitrary units)")


def animation_plot(model, ax):
    group_grid = model.network.attr_grid("status")
    color_dict = {-1: "r", 0: "b", 1: "g"}
    cmap = colors.ListedColormap([color_dict[key] for key in color_dict])
    ap.gridplot(group_grid, cmap=cmap, ax=ax)
    ax.set_title(
        f"Energyshed model \n Time-step: {model.t}, "
        f"Total cost: {round(model.get_cost(), 2)},"
        f"Weather: {model.get_weather()}"
    )
