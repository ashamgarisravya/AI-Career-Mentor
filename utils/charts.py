"""Plotly chart helpers."""

from __future__ import annotations

import plotly.graph_objects as go


def gauge(title: str, value: int, color: str = "#2563eb") -> go.Figure:
    """Build a compact gauge chart."""
    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": color}},
        )
    )
    figure.update_layout(height=240, margin={"l": 10, "r": 10, "t": 45, "b": 10})
    return figure


def bar_progress(labels: list[str], values: list[int]) -> go.Figure:
    """Build a horizontal progress chart."""
    figure = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker_color="#0f766e"))
    figure.update_xaxes(range=[0, 100], ticksuffix="%")
    figure.update_layout(height=300, margin={"l": 20, "r": 20, "t": 20, "b": 20})
    return figure
