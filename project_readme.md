# Marine Construction & Blue Economy Mapping App

An interactive Streamlit application designed to map the relationships between Marine Construction Impacts, Blue Economy Practices, Implementation Challenges, and Lean Principles using cascading drill-down menus and dynamic Sankey diagrams.

## App Features
- **4-Column Cascading Navigation:**
  1. `Impact of Marine Construction` (Always visible initially)
  2. `Blue Economy Practice` (Filtered based on selected Impact)
  3. `Challenges to Implement Blue Economy Practice` (Filtered based on selected Practice)
  4. `Lean Principles` (Displays principles corresponding to the selected Challenge)
- **Dynamic Sankey Diagrams:** Interactive flow visualizations built using Plotly that update based on active filters.

## Excel File Requirements
Your Excel dataset (`.xlsx`) must contain the exact column headers:
- `Impact of Marine Construction`
- `Blue Economy Practice`
- `Challenges to Implement Blue Economy Practice`
- `Lean Principles`

## Quick Start & Deployment

1. **Install requirements locally:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   streamlit run app.py
   ```

3. **Deploy to GitHub & Streamlit Community Cloud:**
   - Push `app.py`, `requirements.txt`, and `README.md` to your GitHub repository.
   - Go to [share.streamlit.io](https://share.streamlit.io/), link your GitHub repository, set `app.py` as the entry file, and click **Deploy**.