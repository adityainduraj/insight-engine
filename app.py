import streamlit as st
import pandas as pd
from data_processor import preprocess_data
from visualizer import visualize_data

def main():
    st.title("Project Insight")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the file
        df = pd.read_csv(uploaded_file)
        st.write("Data loaded successfully!")

        # Display raw data
        st.subheader("Raw Data")
        st.write(df.head())

        # Preprocess data
        df_processed = preprocess_data(df)

        # Visualize data
        visualize_data(df_processed)

if __name__ == "__main__":
    main()