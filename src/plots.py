import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors
import agentpy as ap


def status_stackplot(data, ax):
    """Stackplot of people's condition over time."""
    x = data.index.get_level_values("t")
    y = [data[var] for var in ["none", "buy", "sell"]]

    color_map = {"labels": ["none", "buy", "sell"], "colors": ["b", "r", "g"]}
    ax.stackplot(x, y, **color_map)

    ax.legend()
    ax.set_xlim(0, max(1, len(x) - 1))
    ax.set_ylim(0, 1)
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Percentage of population")


def cost_lineplot(data, ax):
    """Stackplot of people's condition over time."""
    x = data.index.get_level_values("t")
    y = -data["cost"]

    ax.plot(x, y)

    ax.legend()
    ax.set_xlim(0, max(1, len(x) - 1))
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Cost (arbitrary units)")


def transfer_lineplot(data, ax):
    """Stackplot of people's condition over time."""
    x = data.index.get_level_values("t")
    local = data["local_transfer"]
    grid = data["grid_transfer"]

    sns.set()
    ax.plot(x, local, label="Local transfer")
    ax.plot(x, grid, label="Grid transfer")

    ax.legend()
    ax.set_xlim(0, max(1, len(x) - 1))
    ax.set_ylim(0, max(local.max(), grid.max()))
    ax.set_xlabel("Time steps")
    ax.set_ylabel("Energy (arbitrary units)")


def animation_plot(model, ax):
    group_grid = model.network.attr_grid("status")
    color_dict = {0: "b", -1: "r", 1: "g"}
    cmap = colors.ListedColormap([color_dict[key] for key in color_dict])
    ap.gridplot(group_grid, cmap=cmap, ax=ax)
    ax.set_title(
        f"Energyshed model \n Time-step: {model.t}, "
        f"Energy Transfer: {round(model.get_cost(), 3)},"
        f"Weather: {model.get_weather()}"
    )
