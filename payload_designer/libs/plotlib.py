"""Plotting and visualization tools."""
# external
import plotly.graph_objects as go


def plot_surface(z, x, y):
    """Plots 3D surface data.

    Args:
        z (array_like[float]): height data.
        x (array_like[float]): x-coordinate data.
        y (array_like[float]): y-coordinate data.

    Returns:
        plotly.figure: figure object.
    """
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

    fig.update_traces(
        contours_z=dict(
            show=True, usecolormap=True, highlightcolor="limegreen", project_z=True
        )
    )

    return fig
