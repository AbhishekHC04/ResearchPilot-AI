import pymupdf

doc = pymupdf.open()
pages = [
    """SAMPLE RESEARCH PAPER
Semantic Search and Retrieval-Augmented Generation

ABSTRACT
This sample explains semantic search and retrieval-augmented generation (RAG) for document question answering.

1. SEMANTIC SEARCH
Semantic search finds information based on meaning rather than matching exact keywords. It uses numerical embeddings to represent text. For example, a question about reducing energy use may retrieve a passage about energy efficiency even when the wording differs.

2. RETRIEVAL-AUGMENTED GENERATION
Retrieval-augmented generation, known as RAG, provides relevant document passages to a language model as context for answering questions. A RAG assistant should base its answer on those passages and cite the source.

3. LIMITATIONS
Retrieval can help ground an answer, but it does not guarantee correctness. If the document does not contain enough information, the assistant should say so instead of inventing facts.

4. CONCLUSION
A document assistant can extract PDF text, split it into chunks, retrieve relevant passages using embeddings, and generate answers supported by the document.""",
    """SAMPLE RESEARCH PAPER — CONTINUED

5. EVALUATION QUESTIONS

Question 1: What is semantic search?
Answer: It finds information based on meaning rather than exact keyword matches.

Question 2: What does RAG provide to a language model?
Answer: It provides relevant document passages as context for generating an answer.

Question 3: Does retrieval guarantee every answer is correct?
Answer: No. Retrieval can improve grounding, but it does not guarantee correctness.

Question 4: What should an assistant do when the document lacks an answer?
Answer: It should acknowledge that there is insufficient information rather than inventing a response.

This is a fictional educational sample for testing PDF processing and AI question answering. It is not a real scientific study."""
]

for text in pages:
    page = doc.new_page()
    page.insert_textbox(
        pymupdf.Rect(60, 60, 535, 740),
        text,
        fontsize=11,
        fontname="helv",
        lineheight=1.5,
    )

doc.save("researchpilot_sample_paper.pdf")
doc.close()
print("Created researchpilot_sample_paper.pdf in your project folder.")
