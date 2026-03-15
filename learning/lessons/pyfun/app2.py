import numpy as np
import pandas as pd
import plotly.express as px
import plotly.g***h_objects as go


def create_interactive_plots():
    # Sample data
    np.random.seed(42)
    data = pd.DataFrame(
        {
            "x": np.random.randn(500),
            "y": np.random.randn(500),
            "z": np.random.randn(500),
            "category": np.random.choice(["A", "B", "C"], 500),
            "size": np.random.uniform(10, 100, 500),
        }
    )

    # 3D Scatter plot
    fig_3d = px.scatter_3d(
        data,
        x="x",
        y="y",
        z="z",
        color="category",
        size="size",
        opacity=0.7,
        title="3D Interactive Scatter Plot",
    )

    # Animated plot
    time_data = pd.DataFrame(
        {
            "year": np.repeat(range(2010, 2021), 10),
            "product": np.tile([f"Product {i}" for i in range(1, 11)], 11),
            "sales": np.random.lognormal(mean=10, sigma=1, size=110),
        }
    )

    fig_animated = px.bar(
        time_data,
        x="product",
        y="sales",
        color="product",
        animation_frame="year",
        range_y=[0, time_data["sales"].max() * 1.1],
        title="Sales Growth Animation (2010-2020)",
    )

    return fig_3d, fig_animated


fig1, fig2 = create_interactive_plots()
fig1.show()
fig2.show()
