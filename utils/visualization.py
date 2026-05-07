"""
Visualization Module
Creates interactive charts and visualizations using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st

def create_line_chart(df, x, y, title):
    """Create an interactive line chart."""
    fig = px.line(df, x=x, y=y, title=title,
                  markers=True, line_shape='linear')
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig

def create_bar_chart(df, x, y, title, color=None):
    """Create an interactive bar chart."""
    fig = px.bar(df, x=x, y=y, title=title, color=color)
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white',
        hovermode='x'
    )
    return fig

def create_pie_chart(df, values, names, title):
    """Create an interactive pie chart."""
    fig = px.pie(df, values=values, names=names, title=title)
    fig.update_layout(paper_bgcolor='white')
    return fig

def create_scatter_plot(df, x, y, title, color=None, size=None):
    """Create an interactive scatter plot."""
    fig = px.scatter(df, x=x, y=y, title=title, color=color, size=size)
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white',
        hovermode='closest'
    )
    return fig

def create_box_plot(df, y, x=None, title=''):
    """Create a box plot."""
    fig = px.box(df, y=y, x=x, title=title)
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig

def create_histogram(df, x, title='', nbins=30):
    """Create a histogram."""
    fig = px.histogram(df, x=x, title=title, nbins=nbins)
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig

def create_correlation_heatmap(df, title='Correlation Matrix'):
    """Create a correlation heatmap."""
    # Select numeric columns only
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmid=0
    ))
    
    fig.update_layout(
        title=title,
        paper_bgcolor='white'
    )
    return fig

def create_area_chart(df, x, y, title):
    """Create an area chart."""
    fig = px.area(df, x=x, y=y, title=title)
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig

def create_bubble_chart(df, x, y, size, color, title):
    """Create a bubble chart."""
    fig = px.scatter(df, x=x, y=y, size=size, color=color, 
                    title=title, hover_data=df.columns)
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig

def create_sunburst_chart(df, labels, parents, values, title):
    """Create a sunburst chart."""
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total"
    ))
    fig.update_layout(title=title, paper_bgcolor='white')
    return fig

def create_multi_line_chart(df, x, y_columns, title):
    """Create a multi-line chart."""
    fig = go.Figure()
    
    for col in y_columns:
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[col],
            mode='lines+markers',
            name=col
        ))
    
    fig.update_layout(
        title=title,
        hovermode='x unified',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig

def create_stacked_bar_chart(df, x, y_columns, title):
    """Create a stacked bar chart."""
    fig = go.Figure()
    
    for col in y_columns:
        fig.add_trace(go.Bar(
            x=df[x],
            y=df[col],
            name=col
        ))
    
    fig.update_layout(
        title=title,
        barmode='stack',
        plot_bgcolor='rgba(240,240,240,0.5)',
        paper_bgcolor='white'
    )
    return fig

def create_metric_cards_html(metrics):
    """Create HTML for metric cards display."""
    html_content = """
    <style>
        .metric-container {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            min-width: 200px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 14px;
            opacity: 0.9;
        }
    </style>
    <div class="metric-container">
    """
    
    for metric in metrics:
        html_content += f"""
        <div class="metric-card">
            <div class="metric-label">{metric['label']}</div>
            <div class="metric-value">{metric['value']}</div>
        </div>
        """
    
    html_content += "</div>"
    return html_content
