import requests
import streamlit as st


API_URL = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="Tesla Model Y GenAI Intelligence",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Tesla Model Y 2026 GenAI Intelligence Platform")

st.caption(
    "RAG + FAISS + OpenAI + LangGraph Multi-Agent Analysis"
)


st.sidebar.header("Navigation")

mode = st.sidebar.selectbox(
    "Choose analysis mode",
    [
        "RAG Assistant",
        "Multi-Agent Analysis",
        "View Drawbacks",
        "Evaluation"
    ]
)


if mode == "RAG Assistant":

    st.subheader("Ask the Tesla RAG Assistant")

    question = st.text_input(
        "Question",
        "What are the biggest drawbacks of the 2026 Tesla Model Y Premium?"
    )

    if st.button("Analyze"):

        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question},
            timeout=120
        )

        data = response.json()

        st.subheader("AI Answer")
        st.write(data.get("answer"))

        st.subheader("Retrieved Evidence")

        for source in data.get("sources", []):
            with st.expander(source.get("title", "Source")):
                st.write("Category:", source.get("category"))
                st.write("Severity:", source.get("severity"))
                st.write("Evidence:", source.get("evidence"))
                st.write(source.get("text"))
                st.write(
                    "Similarity:",
                    source.get("similarity_score")
                )


elif mode == "Multi-Agent Analysis":

    st.subheader("LangGraph Multi-Agent Analysis")

    question = st.text_area(
        "Question",
        "Analyze the biggest drawbacks and give a buyer recommendation."
    )

    if st.button("Run Agents"):

        response = requests.post(
            f"{API_URL}/agent",
            json={"question": question},
            timeout=120
        )

        data = response.json()

        st.subheader("Final Agent Report")

        st.write(
            data.get(
                "final_report",
                data
            )
        )

        with st.expander("Evidence Summary"):
            st.write(
                data.get(
                    "evidence_summary"
                )
            )

        with st.expander("Recommendation"):
            st.write(
                data.get(
                    "recommendation"
                )
            )


elif mode == "View Drawbacks":

    st.subheader("Tesla Drawback Knowledge Base")

    response = requests.get(
        f"{API_URL}/drawbacks",
        timeout=30
    )

    data = response.json()

    st.dataframe(
        data,
        use_container_width=True
    )


elif mode == "Evaluation":

    st.subheader("RAG Evaluation")

    response = requests.get(
        f"{API_URL}/evaluate",
        timeout=60
    )

    data = response.json()

    st.json(data)
