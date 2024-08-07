import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def visualize_data(df):
    st.subheader("Data Visualization")

    # Correlation heatmap
    st.write("Correlation Heatmap")
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Pairplot
    st.write("Pairplot")
    fig = sns.pairplot(df)
    st.pyplot(fig)

    # Interactive scatter plot
    st.write("Interactive Scatter Plot")
    x_axis = st.selectbox('Choose x-axis', options=df.columns)
    y_axis = st.selectbox('Choose y-axis', options=df.columns)
    fig = px.scatter(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig)

    # Distribution plots
    st.write("Distribution Plots")
    for column in df.select_dtypes(include=[np.number]).columns:
        fig, ax = plt.subplots()
        sns.histplot(df[column], kde=True, ax=ax)
        st.pyplot(fig)