import re
import json
import streamlit as st
fname = "data.json"
def latex_to_quiz_json(latex_code: str) -> dict:
    """
    Extracts quiz questions and options from LaTeX code into a JSON-like dictionary.
    """
    pattern = r"\\item\s*(.*?)\s*\\\\\s*A\)(.*?)B\)(.*?)C\)(.*?)D\)(.*?)(?=(?:\\item|\\end\{enumerate\}))"
    matches = re.findall(pattern, latex_code, flags=re.S)

    quiz_dict = {}
    for match in matches:
        question = " ".join(match[0].split())
        options = [
            "A) " + match[1].replace("\\quad","").strip(),
            "B) " + match[2].replace("\\quad","").strip(),
            "C) " + match[3].replace("\\quad","").strip(),
            "D) " + match[4].replace("\\quad","").strip(),
            "Correct "
        ]
        quiz_dict[question] = options

    return quiz_dict


# ---- Streamlit App ----
st.title("LaTeX to Quiz JSON Converter")

uploaded_file = st.file_uploader("Upload your LaTeX file (.tex)", type=["tex"])

if uploaded_file is not None:
    latex_code = uploaded_file.read().decode("utf-8")

    # Process LaTeX to quiz JSON
    quiz_json = latex_to_quiz_json(latex_code)

    # Convert to JSON string
    json_str = json.dumps(quiz_json, ensure_ascii=False, indent=2)
    
    # Download button
    st.download_button(
        label="Download quiz.json",
        data=json_str.encode("utf-8"),
        file_name=fname,
        mime="application/json"
    )

    # Display preview
    st.subheader("Extracted Quiz JSON Preview")
    st.code(json_str, language="json")


# --- Load Quiz Data ---
def load_quiz(filename=fname):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# --- App ---
st.title("📘 Quiz Viewer with LaTeX Support")

if quiz_data != quiz_json:

# Iterate over questions
for i, (question, options) in enumerate(quiz_data.items(), start=1):
    st.markdown(f"### Q{i}:")
    
    # Render the question as LaTeX if it contains math
    if "$" in question:
        st.write(question)  # Remove $ for st.latex
    else:
        st.write(question)

    # Extract options (ignore "Correct" if present)
    choices = [opt for opt in options if not opt.startswith("Correct")]

    # Show options as radio buttons
    selected = st.radio(f"Choose an answer for Q{i}:", choices, key=f"q{i}")
    st.write("---")
