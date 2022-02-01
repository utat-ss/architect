"""Plotting and visualization tools."""
# stdlib
import logging
from datetime import datetime
from pathlib import Path

# external
import plotly.express as px
import plotly.graph_objects as go

LOG = logging.getLogger(__name__)

output_path = Path("output/images")


def line(x, y):
    """Plots line plot. Supports up to 2D data.

    Args:     x (array_like): 1st dimension of data.     y (array_like): 2nd dimension
    of data.  Returns:     plotly.figure: figure object.

    """

    fig = px.line(x=x, y=y, markers=True)

    fig.show()

    return fig


def surface(x, y, z):
    """Plots surface data. Supports up to 3D data.

    Args:     x (array_like[float]): x-coordinate data.     y (array_like[float]):
    y-coordinate data.     z (array_like[float]): height data.  Returns:
    plotly.figure: figure object.

    """
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

    fig.update_traces(
        contours_z=dict(
            show=True, usecolormap=True, highlightcolor="limegreen", project_z=True
        )
    )

    fig.show()

    return fig


def scatter(x, y, z=None, w=None):
    """Plots scatter plot. Supports up to 4D data.

    Args:     x (array_like): 1st dimension of data.     y (array_like): 2nd dimension
    of data.     color (array_like, optional): 3rd dimension of data. Defaults to None.
    size (array_like, optional): 4th dimension of data. Defaults to None.  Returns:
    plotly.figure: figure object.

    """
    fig = px.scatter(x=x, y=y, color=z, size=w)

    fig.show()

    return fig


def scatter3(x, y, z, w=None, v=None):
    """Plots 3D scatter plot. Supports up to 5D data.

    Args:
        x (array_like): 1st dimension of data.
        y (array_like): 2nd dimension of data.
        z (array-like): 3rd dimension of data.
        w (array_like, optional): 4th dimension of data. Defaults to None.

    Returns:
        plotly.figure: figure object.

    """
    fig = px.scatter_3d(x=x, y=y, z=z, color=w, size=v, size_max=18, opacity=0.9)

    fig.show()

    return fig


def save(fig, filename):  # Unable to find installation candidates for kaleido
    """Saves figure to output path.

    Args:     fig (plotly.figure): figure object.     filename (str): filename.

    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
    file_path = output_path / f"{filename}_{timestamp}.png"
    fig.write_image(file_path)
    LOG.info(f"Saved figure to {file_path}")
