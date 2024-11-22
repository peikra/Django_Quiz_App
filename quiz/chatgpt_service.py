import openai


class ChatGPTService:
    def __init__(self):
        self.api_key = "openai_api_key_here"
        openai.api_key = self.api_key
        # githubze ar itvirteba key

    '''
    Error generating question: 

    You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.
    
    You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 
    
    Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28`
    
    A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
    '''
    def generate_question(self, category, difficulty):
        prompt = f"""Generate an open-ended question about {category} with difficulty level {difficulty}.
        Include both the question and a model answer that can be used to evaluate student responses.
        Format:
        Question: [question text]
        Model Answer: [detailed model answer]"""

        try:
            response = openai.ChatCompletion.create(
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
        lines = response.strip().split('\n')
        question_text = ""
        model_answer = ""

        for line in lines:
            if line.startswith('Question:'):
                question_text = line.replace('Question:', '').strip()
            elif line.startswith('Model Answer:'):
                model_answer = line.replace('Model Answer:', '').strip()

        return {
            'question_text': question_text,
            'model_answer': model_answer
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
        lines = response.strip().split('\n')
        score = 0
        feedback = ""

        for line in lines:
            if line.startswith('Score:'):
                score = float(line.replace('Score:', '').strip())
            elif line.startswith('Feedback:'):
                feedback = line.replace('Feedback:', '').strip()

        return {
            'score': score,
            'feedback': feedback
        }
