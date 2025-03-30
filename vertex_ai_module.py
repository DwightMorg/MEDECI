# vertex_ai_module.py
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

class VertexAIClient:
    def __init__(self, project, location, model="gemini-2.0-flash-001"):
        self.project = project
        self.location = location
        self.model = model
        self.client = genai.Client(vertexai=True, project=self.project, location=self.location)

    def generate_response(self, user_input, system_instruction):
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)]
            )
        ]
        config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=8192,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
            ],
            system_instruction=[types.Part.from_text(text=system_instruction)],
        )

        response_chunks = self.client.models.generate_content_stream(
            model=self.model, contents=contents, config=config
        )

        for chunk in response_chunks:
            yield chunk.text

    def handle_message(self, message, context):
        user_input = message.get("content")
        system_instruction = context.get("system_instruction")
        if not user_input:
            return "Error: No user input provided."

        responses = ""
        for text in self.generate_response(user_input, system_instruction):
            responses += text
        return responses