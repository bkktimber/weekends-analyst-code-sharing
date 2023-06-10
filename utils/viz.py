# %%
import themepy
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from utils.misc import add_font

add_font()
theme = themepy.Theme()
theme.set_spines("off", which=["top", "right"]).set_font("Anakotmai")


def generate_heat_map_zone(
    df: pd.DataFrame, ax: plt.axes = None, normalize=False, annotate=False
) -> plt.axes:
    """
    Generate heatmap of player action
    Input:
        df: Player action from event data
        ax: Matplotlib Axis
    Output:
        Matplotlib Axis
    """

    from matplotlib.colors import LinearSegmentedColormap
    from scipy.ndimage import gaussian_filter

    # (Lenght, Width)
    BIN_GRID = (6, 3)
    cmap = LinearSegmentedColormap.from_list(
        "Pearl Earring - 100 colors", ["#15242e", "#4393c4"], N=100
    )

    pitch = VerticalPitch(
        pitch_type="opta",
        corner_arcs=True,
        line_zorder=2,
        half=False,
        line_color="black",
    )
    pitch.draw(figsize=(16, 10), constrained_layout=True, tight_layout=False, ax=ax)
    bin_statistic = pitch.bin_statistic(
        df.x, df.y, statistic="count", normalize=normalize, bins=BIN_GRID
    )
    bin_statistic["statistic"] = gaussian_filter(bin_statistic["statistic"], 1)
    pitch.heatmap(
        bin_statistic,
        cmap=cmap,
        edgecolor="black",
        ax=ax,
    )
    pitch.scatter(
        df.x,
        df.y,
        marker="o",
        alpha=0.2,
        s=40,
        c="grey",
        edgecolor="black",
        zorder=1,
        ax=ax,
    )
    if annotate:
        labels = pitch.label_heatmap(
            bin_statistic,
            color="#ecf4f9",
            fontsize=18,
            ha="center",
            va="center",
            str_format="{:.0%}",
            zorder=2.1,
            ax=ax,
        )

    return ax


def generate_pass_location_map(
    df: pd.DataFrame = None, ax: plt.axes = None
) -> plt.axes:
    """
    Generate Pass location map
    Input:
        df: Player action from event data
        ax: Matplotlib Axis
    Output:
        Matplotlib Axis
    """

    pitch = VerticalPitch(
        pitch_type="opta",
        corner_arcs=True,
        line_zorder=1,
        half=False,
        line_color="black",
    )
    pitch.draw(figsize=(16, 10), constrained_layout=True, tight_layout=False, ax=ax)
    sucess_pass_filter = df["event_outcome"] == "Successful"
    keypass_filter = df["is_keypass"]
    DF_FILTERS = sucess_pass_filter & keypass_filter

    pitch.lines(
        df.loc[
            DF_FILTERS,
            "start_x",
        ],
        df.loc[
            DF_FILTERS,
            "start_y",
        ],
        df.loc[
            DF_FILTERS,
            "end_x",
        ],
        df.loc[
            DF_FILTERS,
            "end_y",
        ],
        comet=True,
        color="#4393c4",
        zorder=1.8,
        ax=ax,
    )
    pitch.lines(
        df.loc[~DF_FILTERS, "start_x"],
        df.loc[~DF_FILTERS, "start_y"],
        df.loc[~DF_FILTERS, "end_x"],
        df.loc[~DF_FILTERS, "end_y"],
        comet=True,
        zorder=1.5,
        color="grey",
        alpha=0.1,
        ax=ax,
    )
    return ax
