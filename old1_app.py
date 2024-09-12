
import streamlit as st
import pandas as pd
from data_analysis import get_summary_statistics
from visualizations import create_visualization

def add_month_year_columns(df):
    # Find columns with datetime types or that can be converted to datetime
    date_columns = df.select_dtypes(include=['datetime64', 'object']).columns
    for column in date_columns:
        try:
            # Try to parse date columns
            df[column] = pd.to_datetime(df[column])
            # Create Month-Year column
            df[column + '_Month_Year'] = df[column].dt.strftime('%B-%Y')
        except Exception:
            # If parsing fails, skip that column
            pass
    return df

def main():
    st.title("Interactive Data Visualization Dashboard")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Add Month-Year columns for date features
        df = add_month_year_columns(df)

        st.subheader("First 5 rows of the dataset")
        st.write(df.head())

        st.subheader("Summary Statistics")
        summary_stats = get_summary_statistics(df)
        st.write(summary_stats)

        st.subheader("Interactive Visualizations")
        
        # Sidebar for selecting visualization type
        viz_type = st.sidebar.selectbox(
            "Choose a visualization",
            ["Scatter Plot", "Bar Chart", "Line Chart", "Box Plot", "Histogram", "Heatmap"]
        )

        # Dynamically get column names based on data types
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        all_columns = df.columns

        # Select columns for visualization
        if viz_type in ["Scatter Plot", "Line Chart", "Bar Chart", "Box Plot"]:
            x_column = st.sidebar.selectbox("Select X-axis", all_columns)
            y_column = st.sidebar.selectbox("Select Y-axis", numeric_columns)
            color_column = st.sidebar.selectbox("Select Color (optional)", ["None"] + list(all_columns))
            color_column = None if color_column == "None" else color_column
            fig = create_visualization(df, viz_type, x=x_column, y=y_column, color=color_column)
        elif viz_type == "Histogram":
            column = st.sidebar.selectbox("Select Column", all_columns)
            fig = create_visualization(df, viz_type, x=column)
        elif viz_type == "Heatmap":
            fig = create_visualization(df, viz_type)

        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
