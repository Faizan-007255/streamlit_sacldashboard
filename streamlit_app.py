#import streamlit as st
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go

# Title and current date display
st.title("SACL Deshbord")

# Add image at the top of the dashboard
st.image("C:\\Users\\3TEE\\Pictures\\Screenshots\\sacl.png", caption="Company Logo", use_column_width=True)

current_date = datetime.now().strftime("%d-%m-%Y")
st.write(f"Current Date: {current_date}")

# Sidebar for navigation
option = st.sidebar.selectbox(
    'Select a section:',
    ['Dashboard Overview', 'Detailed Analysis', 'Custom Report']
)

# Excel file upload
uploaded_file = st.file_uploader("Excel file upload karein", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Excel file load karne mein masla: {e}")
        st.stop()

    df.columns = df.columns.str.strip()

    if df.shape[1] >= 2:
        category_column = df.columns[0]
        value_column = df.columns[1]

        # Tabs for different charts and data view
        tab1, tab2, tab3 = st.tabs(["Bar Chart", "Donut Chart", "Data View"])

        with tab1:
            # Bar chart plot
            try:
                fig, ax = plt.subplots(figsize=(6, 4))
                df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
                df = df.dropna(subset=[category_column, value_column])
                
                ax.bar(df[category_column], df[value_column], color='skyblue')
                ax.set_title('Sample Dashboard Chart')
                ax.set_xlabel('Categories')
                ax.set_ylabel('Values')
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Chart plot karne mein masla: {e}")

        with tab2:
            # Donut chart plot using Plotly
            try:
                fig = go.Figure(data=[go.Pie(labels=df[category_column], values=df[value_column], hole=0.5)])
                fig.update_layout(
                    title_text="Donut Chart Example",
                    annotations=[dict(text='Categories', x=0.5, y=0.5, font_size=20, showarrow=False)],
                    height=400,
                    width=600,
                )
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Donut chart plot karne mein masla: {e}")

        with tab3:
            st.write("Data:")
            st.dataframe(df)

            # Multi-select for columns to sum
            sum_columns = st.multiselect("Select columns to sum:", df.columns[1:])  # Exclude first column

            if sum_columns:
                total_sum = df[sum_columns].sum()  # Calculate the sum of selected columns
                
                # Create a DataFrame for displaying sums
                summary_df = pd.DataFrame(total_sum).reset_index()
                summary_df.columns = ['Column Name', 'Total Sum']

                st.write("**Total Sum:**")
                st.dataframe(summary_df)

    else:
        st.error("Excel file mein kam se kam do columns hone chahiye.")

# Button for additional details
if st.button("View More Details"):
    st.write("Yahan par additional information ya chart dikha sakte hain.")

st.markdown("***")
st.markdown("### Created by: Faizan Ahmed")
