
import streamlit as st
from tools import calculate, get_datetime, analyze_text, run_agent


st.set_page_config(
    page_title="Astra AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Improve readability across the application
st.markdown("""
<style>
html, body, [class*="st-"] {
    font-size: 18px !important;
}

.stApp {
    background-color: #f7f9fc;
}

.main .block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    font-size: 38px !important;
    font-weight: 800 !important;
    line-height: 1.3 !important;
    color: #16325c !important;
}

h2 {
    font-size: 30px !important;
    color: #16325c !important;
}

h3 {
    font-size: 24px !important;
    color: #16325c !important;
}

p, li, label, .stMarkdown, .stCaption {
    font-size: 18px !important;
    line-height: 1.7 !important;
}

[data-testid="stSidebar"] {
    background-color: #eaf1fb;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 12px;
}

.stButton button, .stFormSubmitButton button {
    font-size: 18px !important;
    min-height: 45px;
    font-weight: 600;
}

.stTextInput input, .stTextArea textarea {
    font-size: 18px !important;
    line-height: 1.6 !important;
}

[data-testid="stMetricValue"] {
    font-size: 28px !important;
}

.small-note {
    font-size: 16px !important;
    color: #46566d;
}
</style>
""", unsafe_allow_html=True)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am Astra, your multi-tool AI agent. "
                "I can calculate expressions, show the date and time, "
                "and analyze text. Type 'help' to get started."
            )
        }
    ]


# Sidebar
with st.sidebar:
    st.title("🤖 Astra AI")
    st.write("Your Multi-Tool Autonomous AI Agent")
    st.divider()

    st.subheader("🧰 Available Tools")
    st.markdown("""
    - 🧮 **Calculator**
    - 🕒 **Date and Time**
    - 📝 **Text Analyzer**
    - 💬 **Chat Assistant**
    """)

    st.divider()
    st.subheader("💡 Example Commands")

    st.code("calculate 25 * 4")
    st.code("What is the current time?")
    st.code("analyze: Python is easy to learn.")
    st.code("help")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared! How can I help you?"
            }
        ]
        st.rerun()

    st.divider()
    st.caption("Built with Python and Streamlit")


# Main heading
st.title("🤖 Astra – Multi-Tool AI Agent")
st.write(
    "An interactive Python application that uses specialized "
    "tools to perform calculations, retrieve date and time, "
    "and analyze text."
)

# Summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Available Tools", "3")

with col2:
    st.metric("Interface", "Interactive")

with col3:
    st.metric("External API", "Not Required")

st.divider()


# Tool dashboard
st.header("🧰 Tool Dashboard")

tab1, tab2, tab3 = st.tabs([
    "🧮 Calculator",
    "🕒 Date & Time",
    "📝 Text Analyzer"
])

with tab1:
    st.subheader("Calculator")
    st.write("Enter an arithmetic expression to calculate.")

    expression = st.text_input(
        "Arithmetic Expression",
        placeholder="Example: (25 + 5) * 4",
        key="calculator_input"
    )

    if st.button("Calculate", key="calculate_button"):
        if expression.strip():
            result = calculate(expression)
            st.success(f"Result: {result}")
        else:
            st.warning("Please enter an expression.")

with tab2:
    st.subheader("Current Date and Time")
    st.write("Get the current date and time from your computer.")

    if st.button("Get Date and Time"):
        st.info(get_datetime())

with tab3:
    st.subheader("Text Analyzer")
    st.write(
        "Enter text to count words, characters, sentences, "
        "and frequently used words."
    )

    text_to_analyze = st.text_area(
        "Enter Your Text",
        placeholder="Type or paste your text here...",
        height=160,
        key="analyzer_input"
    )

    if st.button("Analyze Text"):
        if text_to_analyze.strip():
            result = analyze_text(text_to_analyze)

            a, b, c = st.columns(3)
            a.metric("Words", result["words"])
            b.metric("Characters", result["characters"])
            c.metric("Sentences", result["sentences"])

            st.write(
                "Characters without spaces:",
                result["characters_without_spaces"]
            )
            st.write("Most common words:")

            if result["most_common_words"]:
                for word, count in result["most_common_words"]:
                    st.write(f"- **{word}**: {count}")
            else:
                st.write("No words found.")
        else:
            st.warning("Please enter some text.")


# Chat assistant
st.divider()
st.header("💬 Chat with Astra")
st.write("Ask a question or enter a command in the chat box.")

# Display existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = run_agent(prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)


st.divider()
st.markdown(
    "<p class='small-note'>"
    "Astra AI Agent | Python + Streamlit | "
    "Local rule-based demonstration"
    "</p>",
    unsafe_allow_html=True
)
