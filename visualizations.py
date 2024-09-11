# import plotly.express as px
# import plotly.graph_objects as go

# def create_visualization(df, viz_type, x=None, y=None, color=None):
#     if viz_type == "Scatter Plot":
#         return px.scatter(df, x=x, y=y, color=color, title=f"Scatter Plot: {y} vs {x}")
#     elif viz_type == "Bar Chart":
#         return px.bar(df, x=x, y=df[x].value_counts(), title=f"Bar Chart of {x}")
#     elif viz_type == "Line Chart":
#         return px.line(df, x=x, y=y, color=color, title=f"Line Chart: {y} vs {x}")
#     elif viz_type == "Box Plot":
#         return px.box(df, y=x, title=f"Box Plot of {x}")
#     elif viz_type == "Histogram":
#         return px.histogram(df, x=x, title=f"Histogram of {x}")
#     elif viz_type == "Heatmap":
#         corr_matrix = df.corr()
#         return go.Figure(data=go.Heatmap(
#             z=corr_matrix.values,
#             x=corr_matrix.columns,
#             y=corr_matrix.index,
#             colorscale='RdBu_r',
#             zmin=-1, zmax=1
#         ))

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_visualization(df, viz_type, x=None, y=None, color=None):
    if viz_type == "Scatter Plot":
        return px.scatter(df, x=x, y=y, color=color, title=f"Scatter Plot: {y} vs {x}")
    elif viz_type == "Bar Chart":
        # Aggregate data if necessary
        if df[x].nunique() < len(df):
            agg_df = df.groupby(x)[y].mean().reset_index()
            return px.bar(agg_df, x=x, y=y, title=f"Bar Chart: Average {y} by {x}")
        else:
            return px.bar(df, x=x, y=y, title=f"Bar Chart: {y} by {x}")
    elif viz_type == "Line Chart":
        # Aggregate data if necessary
        if df[x].nunique() < len(df):
            agg_df = df.groupby(x)[y].mean().reset_index()
            return px.line(agg_df, x=x, y=y, title=f"Line Chart: Average {y} vs {x}")
        else:
            return px.line(df, x=x, y=y, color=color, title=f"Line Chart: {y} vs {x}")
    elif viz_type == "Box Plot":
        return px.box(df, y=y, x=x, title=f"Box Plot of {y} by {x}")
    elif viz_type == "Histogram":
        return px.histogram(df, x=x, title=f"Histogram of {x}")
    elif viz_type == "Heatmap":
        corr_matrix = df.select_dtypes(include=['int64', 'float64']).corr()
        return go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu_r',
            zmin=-1, zmax=1
        ))