def extract_question_answer_simple(text):
    # Find the starting index of "Question:" and "Model Answer:"
    question_start = text.find("Question:") + len("Question:")
    answer_start = text.find("Model Answer:")

    # Extract the question and answer using substring slicing
    question = text[question_start:answer_start].strip()
    answer = text[answer_start + len("Model Answer:"):].strip()

    return question, answer


# Example input
text = """
Question: How does the concept of electronegativity explain the polarity of a water molecule? Use the periodic trends of electronegativity and molecular geometry in your explanation.
Model Answer: Electronegativity refers to the ability of an atom to attract shared electrons in a chemical bond. In a water molecule (H₂O), the oxygen atom has a much higher electronegativity (3.44) compared to hydrogen (2.20), based on the Pauling scale. This difference creates a polar covalent bond because the shared electrons in each O-H bond are drawn closer to the oxygen atom.

Additionally, the water molecule has a bent molecular geometry with a bond angle of approximately 104.5°. This shape arises from the two lone pairs of electrons on the oxygen atom, which push the bonded hydrogen atoms closer together. The combination of bond polarity and asymmetrical shape results in an uneven distribution of charge, with a partial negative charge (δ⁻) on the oxygen atom and partial positive charges (δ⁺) on the hydrogen atoms. This makes water a polar molecule.

The polarity of water is essential for its unique properties, such as high boiling and melting points and its ability to dissolve many ionic and polar substances.
"""

# Extract question and answer
question, answer = extract_question_answer_simple(text)

# Output results
print("Extracted Question:")
print(question)
print("Extracted Model Answer:")
print(answer)
