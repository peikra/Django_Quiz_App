import openai


class ChatGPTService:
    def __init__(self):
        self.api_key = "api_key_here"
        # openai.api_key = self.api_key
        self.client = openai.OpenAI(
            api_key=self.api_key,
        )
        # githubze ar itvirteba key

    def generate_question(self, category, difficulty):
        prompt = f"""Generate an open-ended question about {category} with difficulty level {difficulty}.
        Include both the question and a model answer that can be used to evaluate student responses.
        Format:
        Question: [question text]
        Model Answer: [detailed model answer]"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful quiz question generator."},
                    {"role": "user", "content": prompt}
                ]
            )

            return self._parse_question_response(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating question: {e}")
            return None

    def _parse_question_response(self, response):
        # Find the starting index of "Question:" and "Model Answer:"
        question_start = response.find("Question:") + len("Question:")
        answer_start = response.find("Model Answer:")

        # Extract the question and answer using substring slicing
        question_text = response[question_start:answer_start].strip()
        answer_text = response[answer_start + len("Model Answer:"):].strip()

        return {
            'question_text': question_text,
            'model_answer': answer_text,
        }

    def evaluate_answer(self, student_answer, model_answer):
        prompt = f"""Evaluate the student's answer against the model answer and provide a score between 0 and 100.
        Model Answer: {model_answer}
        Student Answer: {student_answer}

        Provide your response in this format:
        Score: [number]
        Feedback: [explanation]"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an educational evaluator."},
                    {"role": "user", "content": prompt}
                ]
            )

            return self._parse_evaluation_response(response.choices[0].message.content)
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return None


    def _parse_evaluation_response(self, response):
        # Find the starting index of "Score:" and "Feedback:"
        score_start = response.find("Score:") + len("Score:")
        feedback_start = response.find("Feedback:")

        # Extract the score and feedback using substring slicing
        score = response[score_start:feedback_start].strip()
        feedback = response[feedback_start + len("Feedback:"):].strip()

        return {
            'score': float(score),
            'feedback': feedback
        }
