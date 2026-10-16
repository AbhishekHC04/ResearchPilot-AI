
import tempfile
from pathlib import Path

import pymupdf
import streamlit as st

from src.researchpilot.pipeline import ResearchPipeline


st.set_page_config(
    page_title="ResearchPilot AI",
    page_icon="📚",
    layout="wide",
)

st.title("📚 ResearchPilot AI")
st.caption(
    "Upload multiple research papers, search their contents, "
    "and ask questions using a local AI model."
)

if "pipeline" not in st.session_state:
    st.session_state.pipeline = None

if "documents" not in st.session_state:
    st.session_state.documents = []

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.header("📄 Your Documents")

    uploaded_files = st.file_uploader(
        "Upload research papers",
        type=["pdf"],
        accept_multiple_files=True,
        help="Select one or more text-based PDF files.",
    )

    if st.button(
        "Process PDFs",
        disabled=not uploaded_files,
        use_container_width=True,
    ):
        try:
            # Start a fresh collection for this processing operation.
            pipeline = ResearchPipeline()
            total_chunks = 0
            processed_names = []

            with st.spinner("Processing research papers..."):
                for uploaded_file in uploaded_files:
                    with pymupdf.open(
                        stream=uploaded_file.getvalue(),
                        filetype="pdf",
                    ) as document:
                        if document.is_encrypted:
                            raise ValueError(
                                f"{uploaded_file.name} is encrypted."
                            )

                    with tempfile.NamedTemporaryFile(
                        suffix=".pdf",
                        delete=False,
                    ) as temp_file:
                        temp_file.write(uploaded_file.getvalue())
                        temp_path = Path(temp_file.name)

                    try:
                        chunk_count = pipeline.ingest_pdf(temp_path)
                        total_chunks += chunk_count

                        # Replace the temporary filename with the real filename.
                        for chunk in pipeline.chunks:
                            if chunk["source"] == temp_path.name:
                                chunk["source"] = uploaded_file.name

                        pipeline.search_engine.chunks = list(pipeline.chunks)
                        processed_names.append(uploaded_file.name)
                    finally:
                        temp_path.unlink(missing_ok=True)

            st.session_state.pipeline = pipeline
            st.session_state.documents = processed_names
            st.session_state.messages = []

            st.success(
                f"Processed {len(processed_names)} PDF(s) "
                f"and indexed {total_chunks} text chunks."
            )

        except Exception as exc:
            st.error(f"Could not process the PDFs: {exc}")

    if st.session_state.documents:
        st.subheader("Indexed documents")
        for document_name in st.session_state.documents:
            st.write(f"📄 {document_name}")


st.subheader("💬 Ask your research papers")

if st.session_state.pipeline is None:
    st.info(
        "Upload one or more PDFs in the sidebar and select "
        "**Process PDFs** to begin."
    )
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question across your PDFs...")

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner(
                    "Searching your papers and generating an answer..."
                ):
                    history = st.session_state.messages[:-1]
                    result = st.session_state.pipeline.ask(question, history=history)

                st.markdown(result["answer"])

                if result["valid_citations"]:
                     with st.expander("📌 Validated Source Citations"):
                         for citation in result["valid_citations"]:
                           st.markdown(f"- {citation}")


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["answer"],
                    }
                )

            except Exception as exc:
                st.error(
                    "I couldn't generate an answer. "
                    "Check that Ollama is running and try again."
                )
                st.caption(str(exc))
