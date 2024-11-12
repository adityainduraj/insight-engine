import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from lazypredict.Supervised import LazyClassifier, LazyRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from data_analysis import get_summary_statistics
from visualizations import create_visualization, create_prediction_visualization

def recommend_problem_type(df, target_column):
    unique_values = df[target_column].nunique()
    value_counts = df[target_column].value_counts()

    # Check if target is categorical or numerical
    is_numeric = pd.api.types.is_numeric_dtype(df[target_column])

    if not is_numeric:
        return "Classification", "The target variable is non-numeric, suggesting a classification problem."

    if unique_values <= 10 and max(value_counts)/len(df) > 0.01:
        return "Classification", "The target variable has few unique values, suggesting a classification problem."
    else:
        return "Regression", "The target variable appears to be continuous, suggesting a regression problem."

def add_date_features(df):
    date_columns = df.select_dtypes(include=['datetime64', 'object']).columns
    for column in date_columns:
        try:
            df[column] = pd.to_datetime(df[column])
            df[column + '_Month_Year'] = df[column].dt.to_period('M').dt.strftime('%B-%Y')
            df[column + '_Year'] = df[column].dt.year
        except Exception:
            pass
    return df

def get_supported_chart_types(df):
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    supported_types = ["Scatter Plot", "Box Plot", "Histogram", "Heatmap"]
    if len(numeric_columns) > 0:
        supported_types.extend(["Bar Chart", "Line Chart"])
    return supported_types

def add_prediction_section(df, features, target, problem_type, X_train, X_test, y_train, y_test):
    st.subheader("Model Predictions & Visualization")

    # Get the best model based on problem type
    if problem_type == "Classification":
        best_model = RandomForestClassifier(random_state=42)
    else:
        best_model = RandomForestRegressor(random_state=42)

    # Train the best model
    best_model.fit(X_train, y_train)

    # Make predictions
    predictions = best_model.predict(X_test)

    # Create a prediction dataframe
    prediction_df = pd.DataFrame({
        'Actual': y_test,
        'Predicted': predictions
    }).reset_index(drop=True)

    # Display prediction metrics
    st.write("### Prediction Results")
    st.write("Sample of Actual vs Predicted Values:")
    st.write(prediction_df.head(10))

    # Visualization options for predictions
    viz_option = st.selectbox(
        "Choose Prediction Visualization",
        ["Actual vs Predicted", "Prediction Distribution", "Prediction Error Analysis"]
    )

    # Create and display the selected visualization
    fig = create_prediction_visualization(prediction_df, viz_option)
    st.plotly_chart(fig)

    # Interactive prediction section
    st.write("### Make New Predictions")

    # Create input fields for each feature
    new_data = {}
    for feature in features.columns:
        new_data[feature] = st.number_input(
            f"Enter value for {feature}",
            value=float(features[feature].mean())
        )

    if st.button("Predict"):
        input_df = pd.DataFrame([new_data])
        new_prediction = best_model.predict(input_df)

        st.write("### Prediction Result:")
        st.write(f"The predicted value is: {new_prediction[0]:.2f}")

def main():
    st.title("Project Insight with AutoML")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = add_date_features(df)

        st.subheader("First 5 rows of the dataset")
        st.write(df.head())

        st.subheader("Summary Statistics")
        summary_stats = get_summary_statistics(df)
        st.write(summary_stats)

        st.subheader("Interactive Visualizations")
        supported_chart_types = get_supported_chart_types(df)
        viz_type = st.sidebar.selectbox("Choose a visualization", supported_chart_types)

        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        all_columns = df.columns

        if viz_type in ["Scatter Plot", "Line Chart", "Bar Chart", "Box Plot"]:
            x_column = st.sidebar.selectbox("Select X-axis", all_columns)
            y_column = st.sidebar.selectbox("Select Y-axis", numeric_columns)
            color_column = st.sidebar.selectbox("Select Color (optional)", ["None"] + list(all_columns))
            color_column = None if color_column == "None" else color_column
            try:
                fig = create_visualization(df, viz_type, x=x_column, y=y_column, color=color_column)
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error creating {viz_type}: {str(e)}")
        elif viz_type == "Histogram":
            column = st.sidebar.selectbox("Select Column", all_columns)
            try:
                fig = create_visualization(df, viz_type, x=column)
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error creating Histogram: {str(e)}")
        elif viz_type == "Heatmap":
            try:
                fig = create_visualization(df, viz_type)
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error creating Heatmap: {str(e)}")

        st.subheader("AutoML Model Training")
        target = st.selectbox("Select target variable", df.columns)

        # Add problem type recommendation
        recommended_type, reason = recommend_problem_type(df, target)
        st.info(f"💡 Recommended problem type: **{recommended_type}**\n\n{reason}")

        numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
        selected_features = st.multiselect("Select features for the model",
                                         numeric_features,
                                         default=list(numeric_features))
        features = df[selected_features]

        problem_type = st.radio("Select problem type",
                              ["Classification", "Regression"],
                              index=0 if recommended_type == "Classification" else 1)

        # Feature scaling
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        features_scaled = pd.DataFrame(
            scaler.fit_transform(features),
            columns=features.columns
        )

        if st.button("Run AutoML"):
            X_train, X_test, y_train, y_test = train_test_split(
                features, df[target], test_size=0.2, random_state=42
            )

            if problem_type == "Classification":
                clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
                models, predictions = clf.fit(X_train, X_test, y_train, y_test)
            else:
                reg = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
                models, predictions = reg.fit(X_train, X_test, y_train, y_test)

            st.write("Model Performance:")
            st.write(models)

            # Visualize model performance
            fig = px.bar(
                models,
                x=models.index,
                y='Accuracy' if problem_type == "Classification" else 'R-Squared',
                title=f"Model Performance ({'Accuracy' if problem_type == 'Classification' else 'R-Squared'})"
            )
            st.plotly_chart(fig)

            # Add the prediction section
            add_prediction_section(df, features, target, problem_type,
                                 X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main()
