import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_visualization(df, viz_type, x=None, y=None, color=None):
    if x is not None and pd.api.types.is_datetime64_any_dtype(df[x]):
        df = df.sort_values(by=x)

    if viz_type == "Scatter Plot":
        return px.scatter(df, x=x, y=y, color=color, title=f"Scatter Plot: {y} vs {x}")
    elif viz_type == "Bar Chart":
        if df[x].nunique() < len(df):
            agg_df = df.groupby(x)[y].mean().reset_index()
            return px.bar(agg_df, x=x, y=y, title=f"Bar Chart: Average {y} by {x}")
        else:
            return px.bar(df, x=x, y=y, title=f"Bar Chart: {y} by {x}")
    elif viz_type == "Line Chart":
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

def create_prediction_visualization(prediction_df, viz_option):
    if viz_option == "Actual vs Predicted":
        # Create a sorted index
        prediction_df = prediction_df.reset_index(drop=True)

        fig = go.Figure()

        # Add actual values line
        fig.add_trace(go.Scatter(
            x=prediction_df.index,
            y=prediction_df['Actual'],
            mode='lines',
            name='Actual',
            line=dict(color='blue')
        ))

        # Add predicted values line
        fig.add_trace(go.Scatter(
            x=prediction_df.index,
            y=prediction_df['Predicted'],
            mode='lines',
            name='Predicted',
            line=dict(color='red')
        ))

        fig.update_layout(
            title="Actual vs Predicted Values Over Samples",
            xaxis_title="Sample Index",
            yaxis_title="Values",
            showlegend=True
        )
        return fig

    elif viz_option == "Prediction Distribution":
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=prediction_df['Actual'],
            name='Actual',
            opacity=0.7,
            nbinsx=30
        ))
        fig.add_trace(go.Histogram(
            x=prediction_df['Predicted'],
            name='Predicted',
            opacity=0.7,
            nbinsx=30
        ))
        fig.update_layout(
            title="Distribution of Actual vs Predicted Values",
            barmode='overlay',
            xaxis_title="Values",
            yaxis_title="Count"
        )
        return fig

    elif viz_option == "Prediction Error Analysis":
        prediction_df['Error'] = prediction_df['Actual'] - prediction_df['Predicted']
        fig = px.histogram(
            prediction_df,
            x='Error',
            nbins=30,
            title="Distribution of Prediction Errors"
        )
        fig.update_layout(
            xaxis_title="Prediction Error",
            yaxis_title="Count"
        )
        return fig
