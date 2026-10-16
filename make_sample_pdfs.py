
import pymupdf


def create_pdf(filename, title, sections):
    doc = pymupdf.open()

    for heading, text in sections:
        page = doc.new_page()
        content = f"{title}\n\n{heading}\n\n{text}"
        page.insert_textbox(
            pymupdf.Rect(60, 60, 535, 740),
            content,
            fontsize=11,
            fontname="helv",
            lineheight=1.5,
        )

    doc.save(filename)
    doc.close()
    print(f"Created: {filename}")


create_pdf(
    "researchpilot_ai_ml_basics.pdf",
    "Machine Learning Basics",
    [
        (
            "Training and Testing Data",
            "Machine learning systems learn patterns from examples. "
            "Training data is used to fit a model. Test data is kept "
            "separate to estimate performance on unseen examples.",
        ),
        (
            "Evaluation Metrics",
            "Accuracy is the proportion of predictions that are correct. "
            "Precision measures how many predicted positive cases are "
            "actually positive. Recall measures how many actual positive "
            "cases the model identifies. Accuracy can be misleading "
            "when classes are imbalanced.",
        ),
    ],
)

create_pdf(
    "researchpilot_ai_rag_safety.pdf",
    "Reliable Document Question Answering",
    [
        (
            "Grounded Answers",
            "A grounded answer should be supported by retrieved document "
            "passages. If evidence is missing or ambiguous, the assistant "
            "should acknowledge that rather than inventing facts.",
        ),
        (
            "Citations and Prompt Injection",
            "Citations identify the source document and page so readers "
            "can verify claims. Uploaded documents must be treated as "
            "data, not as instructions that override the assistant's rules. "
            "Instructions embedded in a document should not override "
            "the assistant's system rules.",
        ),
    ],
)
