import streamlit as st
import requests

# --- Configuration ---
FLASK_API_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Pi Digit Searcher",
    page_icon="ðŸ› ",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Helper Functions ---
def call_api(endpoint):
    try:
        response = requests.get(f"{FLASK_API_URL}/{endpoint}")
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"ðŸ”¥ API Error: Could not connect to the backend. Please ensure the Flask server is running.")
        st.error(e)
        return None

def search_api(sequence):
    try:
        payload = {"sequence": sequence}
        response = requests.post(f"{FLASK_API_URL}/search", json=payload)
        return response.json() # Return JSON regardless of status to handle errors gracefully
    except requests.exceptions.RequestException as e:
        st.error(f"ðŸ”¥ API Error: Could not connect to the backend. Please ensure the Flask server is running.")
        st.error(e)
        return None

# --- UI Sections ---
def render_search_page():
    st.header("ðŸ”Ž Search for a Sequence")
    sequence = st.text_input("Enter a sequence of digits:", "", max_chars=50, placeholder="e.g., 14159")

    if st.button("Search"):
        if not sequence.isdigit():
            st.warning("âš ï¸ Please enter only digits.")
            return

        with st.spinner("Searching..."):
            result = search_api(sequence)
            if result:
                if result.get("error"):
                    st.error(f"Error from API: {result['error']}")
                elif result.get("found"):
                    st.success(f"âœ… Found it! The sequence appears {result['occurrences']:,} time(s).")
                    st.markdown(f"**First occurrence at position:** `{result['first_position']:,}`")
                    st.markdown("**Snippet:**")
                    st.markdown(result['snippet'], unsafe_allow_html=True)
                else:
                    st.warning("ðŸš« Sequence not found in the first 1 million digits of Pi.")

def render_distribution_page():
    st.header("ðŸ“Š Digit Frequency")
    data = call_api("digit-distribution")
    if data:
        st.write("This table shows how many times each digit appears in the first 1 million digits of Pi.")
        
        # Create a markdown table
        table = "| Digit | Count | Percentage |\n|---|---|---|" 
        chart_data = {}
        for digit, values in sorted(data.items()):
            table += f"| {digit} | {values['count']:,} | {values['percent']:.2f}% |\n"
            chart_data[digit] = values['count']

        st.markdown(table)

        st.subheader("Distribution Chart")
        st.bar_chart(chart_data)

def render_randomness_page():
    st.header("ðŸ§ Randomness Statistics")
    data = call_api("randomness-stats")
    if data:
        st.write("These metrics help assess the randomness of Pi's digits.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Mean Digit Value", f"{data['mean']:.4f}")
        col2.metric("Variance", f"{data['variance']:.4f}")
        col3.metric("Shannon Entropy", f"{data['entropy']:.4f} bits", help="A measure of unpredictability. For a truly random sequence of 10 digits, the maximum entropy is ~3.32 bits. Pi is very close!")

# --- Main App Layout ---
st.title("Pi Digit Searcher (Web Edition)")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Search Sequence", "Digit Frequency", "Randomness Stats"])

st.sidebar.markdown("---")
st.sidebar.info("This app searches for digit sequences in the first 1 million digits of Pi.")

if page == "Search Sequence":
    render_search_page()
elif page == "Digit Frequency":
    render_distribution_page()
elif page == "Randomness Stats":
    render_randomness_page()