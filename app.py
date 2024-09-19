import streamlit as st
import pandas as pd
from data_analysis import get_summary_statistics
from visualizations import create_visualization

def add_date_features(df):
    # Find columns with datetime types or that can be converted to datetime
    date_columns = df.select_dtypes(include=['datetime64', 'object']).columns
    for column in date_columns:
        try:
            # Try to parse date columns
            df[column] = pd.to_datetime(df[column])
            # Create Month-Year column
            df[column + '_Month_Year'] = df[column].dt.to_period('M').dt.strftime('%B-%Y')
            # Create Year column
            df[column + '_Year'] = df[column].dt.year
        except Exception:
            # If parsing fails, skip that column
            pass
    return df

def get_supported_chart_types(df):
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    supported_types = ["Scatter Plot", "Box Plot", "Histogram", "Heatmap"]

    if len(numeric_columns) > 0:
        supported_types.extend(["Bar Chart", "Line Chart"])

    return supported_types

def main():
    st.title("Project Insight")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Add Month-Year and Year columns for date features
        df = add_date_features(df)

        # Ensure Month-Year sorting
        month_year_columns = [col for col in df.columns if 'Month_Year' in col]
        for col in month_year_columns:
            # Extract year and month from the Month-Year column for proper sorting
            df[col + '_sorted'] = pd.to_datetime(df[col], format='%B-%Y', errors='coerce').dt.to_period('M').dt.to_timestamp()

        st.subheader("First 5 rows of the dataset")
        st.write(df.head())

        st.subheader("Summary Statistics")
        summary_stats = get_summary_statistics(df)
        st.write(summary_stats)
        st.subheader("Interactive Visualizations")

        # Get supported chart types based on the dataset
        supported_chart_types = get_supported_chart_types(df)

        # Sidebar for selecting visualization type
        viz_type = st.sidebar.selectbox(
            "Choose a visualization",
            supported_chart_types
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
            try:
                fig = create_visualization(df, viz_type, x=x_column, y=y_column, color=color_column)
            except Exception as e:
                st.error(f"Error creating {viz_type}: {str(e)}")
                return
        elif viz_type == "Histogram":
            column = st.sidebar.selectbox("Select Column", all_columns)
            try:
                fig = create_visualization(df, viz_type, x=column)
            except Exception as e:
                st.error(f"Error creating Histogram: {str(e)}")
                return
        elif viz_type == "Heatmap":
            try:
                fig = create_visualization(df, viz_type)
            except Exception as e:
                st.error(f"Error creating Heatmap: {str(e)}")
                return
        else:
            st.error(f"Unsupported chart type: {viz_type}")
            return

        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
