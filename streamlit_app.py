import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Marine Construction & Blue Economy Mapping",
    layout="wide"
)

st.title("Impact of Marine Construction & Blue Economy Mapping")
st.markdown("Select items step-by-step to filter and visualize connections across categories using interactive Sankey diagrams.")

# Explicit Column Headers matching requirements
COL_IMPACT = "Impact of Marine Construction"
COL_PRACTICE = "Blue Economy Practice"
COL_CHALLENGE = "Challenges to Implement Blue Economy Practice"
COL_LEAN = "Lean Principles"

EXPECTED_COLUMNS = [COL_IMPACT, COL_PRACTICE, COL_CHALLENGE, COL_LEAN]

@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    # Clean whitespace in column names
    df.columns = df.columns.str.strip()
    return df

def generate_sankey(filtered_df, selected_impact=None, selected_practice=None, selected_challenge=None):
    labels = []
    
    # 1. Impacts
    impacts = list(filtered_df[COL_IMPACT].dropna().unique())
    labels.extend(impacts)
    
    # 2. Practices
    practices = list(filtered_df[COL_PRACTICE].dropna().unique())
    labels.extend(practices)
    
    # 3. Challenges
    challenges = list(filtered_df[COL_CHALLENGE].dropna().unique())
    labels.extend(challenges)
    
    # 4. Lean Principles
    leans = list(filtered_df[COL_LEAN].dropna().unique())
    labels.extend(leans)
    
    label_dict = {label: idx for idx, label in enumerate(labels)}
    
    sources = []
    targets = []
    values = []
    
    def add_links(source_col, target_col):
        grouped = filtered_df.groupby([source_col, target_col]).size().reset_index(name='count')
        for _, row in grouped.iterrows():
            if pd.notna(row[source_col]) and pd.notna(row[target_col]):
                sources.append(label_dict[row[source_col]])
                targets.append(label_dict[row[target_col]])
                values.append(row['count'])

    add_links(COL_IMPACT, COL_PRACTICE)
    
    if selected_impact:
        add_links(COL_PRACTICE, COL_CHALLENGE)
        
    if selected_practice:
        add_links(COL_CHALLENGE, COL_LEAN)
        
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color="#006699"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(180, 200, 220, 0.4)"
        )
    )])
    
    fig.update_layout(
        title_text="Category Flow Mapping (Sankey Diagram)", 
        font_size=12,
        height=500
    )
    return fig

# File upload component
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns in uploaded Excel file: {', '.join(missing_cols)}")
        st.stop()
        
    st.sidebar.success("Excel data loaded successfully!")
    
    # Dynamic 4-column cascading selection interface
    col1, col2, col3, col4 = st.columns(4)
    
    # Column 1: Impacts (Always visible)
    with col1:
        st.subheader("Impact of Marine Construction")
        impact_options = sorted(df[COL_IMPACT].dropna().unique())
        selected_impact = st.radio("Select Impact:", impact_options, index=None, key="impact")
        
    filtered_df = df.copy()
    
    # Column 2: Practices (Filtered by selected Impact)
    selected_practice = None
    with col2:
        st.subheader("Blue Economy Practice")
        if selected_impact:
            filtered_df = filtered_df[filtered_df[COL_IMPACT] == selected_impact]
            practice_options = sorted(filtered_df[COL_PRACTICE].dropna().unique())
            selected_practice = st.radio("Select Practice:", practice_options, index=None, key="practice")
        else:
            st.info("👈 Select an Impact to view mapped practices.")
            
    # Column 3: Challenges (Filtered by selected Practice)
    selected_challenge = None
    with col3:
        st.subheader("Challenges to Implement")
        if selected_practice:
            filtered_df = filtered_df[filtered_df[COL_PRACTICE] == selected_practice]
            challenge_options = sorted(filtered_df[COL_CHALLENGE].dropna().unique())
            selected_challenge = st.radio("Select Challenge:", challenge_options, index=None, key="challenge")
        elif selected_impact:
            st.info("👈 Select a Practice to view mapped challenges.")
        else:
            st.info("👈 Complete prior selections.")

    # Column 4: Lean Principles (Filtered by selected Challenge)
    with col4:
        st.subheader("Lean Principles")
        if selected_challenge:
            filtered_df = filtered_df[filtered_df[COL_CHALLENGE] == selected_challenge]
            lean_principles = sorted(filtered_df[COL_LEAN].dropna().unique())
            
            st.markdown("**Mapped Principles:**")
            for principle in lean_principles:
                st.success(f"✔ {principle}")
        elif selected_practice:
            st.info("👈 Select a Challenge to view Lean principles.")
        else:
            st.info("👈 Complete prior selections.")
            
    st.divider()
    
    # Dynamic Sankey Diagram Visualization Section
    st.subheader("Interactive Flow Diagram")
    
    sankey_df = df.copy()
    if selected_impact:
        sankey_df = sankey_df[sankey_df[COL_IMPACT] == selected_impact]
    if selected_practice:
        sankey_df = sankey_df[sankey_df[COL_PRACTICE] == selected_practice]
    if selected_challenge:
        sankey_df = sankey_df[sankey_df[COL_CHALLENGE] == selected_challenge]
        
    fig = generate_sankey(sankey_df, selected_impact, selected_practice, selected_challenge)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload your Excel file using the sidebar to start.")