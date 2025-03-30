# ai_coordinator.py

import logging
import os
from dotenv import load_dotenv
from text_to_speech import TextToSpeechModule  # Import the TextToSpeechModule

class AICoordinator:
    def __init__(self):
        self.modules = {}  # Registry of modules
        self.context = {}  # Shared context
        self.logger = logging.getLogger("ai_coordinator")
        load_dotenv()
        self.config = os.environ
        self.register_tts_module()  # Register TextToSpeechModule

    def register_module(self, module_name, module_instance):
        self.modules[module_name] = module_instance
        self.logger.info(f"Module '{module_name}' registered.")

    def register_tts_module(self):
        """Registers the TextToSpeechModule."""
        tts_module = TextToSpeechModule()
        self.register_module("text_to_speech", tts_module)

    def route_message(self, message):
        """
        Routes a message to the appropriate module.

        Args:
            message: A dictionary containing the message details, including:
                - 'target_module': The name of the module to receive the message.
                - 'message_type': The type of message or command.
                - 'content': The actual content of the message.
                - (Other relevant data)

        Returns:
            The response from the module, or None if the module is not found or an error occurs.
        """
        target_module = message.get("target_module")
        if target_module in self.modules:
            try:
                module = self.modules[target_module]
                response = module.handle_message(message, self.context)
                return response
            except Exception as e:
                self.logger.error(f"Error in module '{target_module}': {e}")
                return None
        else:
            self.logger.warning(f"Module '{target_module}' not found.")
            return None

    def set_context(self, key, value):
        self.context[key] = value

    def get_context(self, key, default=None):
        return self.context.get(key, default)

    def load_config(self, key, default=None):
        return self.config.get(key, default)

    def process_input(self, user_input):
        """
        Process user input and generate AI response.
        
        Args:
            user_input: The user's message string
            
        Returns:
            AI-generated response string
        """
        try:
            # Here you would integrate with Vertex AI
            # For now, returning a simple response
            response = f"I received your message: {user_input}. How can I assist you further?"
            return response
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return "Sorry, I encountered an error processing your request."

# Example module (module_example.py)
class ExampleModule:
    def handle_message(self, message, context):
        """
        Handles incoming messages.

        Args:
            message: A dictionary containing the message details.
            context: The shared context.

        Returns:
            The response to the message.
        """
        message_type = message.get("message_type")
        content = message.get("content")

        print(f"ExampleModule received message of type '{message_type}': {content}")
        return f"Response from ExampleModule: {content}"

# Example usage
if __name__ == "__main__":
    coordinator = AICoordinator()
    example_module = ExampleModule()
    coordinator.register_module("example", example_module)

    message = {
        "target_module": "example",
        "message_type": "greet",
        "content": "Hello, coordinator!",
    }

    response = coordinator.route_message(message)
    print(f"Coordinator response: {response}")

    coordinator.set_context("user_id", 123)
    print(f"Context: {coordinator.get_context('user_id')}")

    # Example text to speech usage:
    tts_message = {
        "target_module": "text_to_speech",
        "content": "This is a test speech synthesis.",
    }
    tts_response = coordinator.route_message(tts_message)
    print(f"TTS response: {tts_response}")