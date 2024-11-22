def extract_score_feedback(text):
    # Find the starting index of "Score:" and "Feedback:"
    score_start = text.find("Score:") + len("Score:")
    feedback_start = text.find("Feedback:")

    # Extract the score and feedback using substring slicing
    score = text[score_start:feedback_start].strip()
    feedback = text[feedback_start + len("Feedback:"):].strip()

    return score, feedback


# Example input
text = """
Score: 8
Feedback: The response demonstrates a good understanding of the concept and provides a clear explanation. However, it could have included more examples to strengthen the argument.
"""

# Extract score and feedback
score, feedback = extract_score_feedback(text)

# Output results
print("Extracted Score:")
print(score)
print("\nExtracted Feedback:")
print(feedback)
