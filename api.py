# api.py (Modified)

from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_coordinator import AICoordinator
import os
from dotenv import load_dotenv
# Import your actual AI module class
from vertex_ai_module import VertexAIClient # Assuming vertex_ai_module.py has VertexAIClient

app = Flask(__name__)
CORS(app) # Consider restricting origins in production

# Initialize AI Coordinator
load_dotenv()
project = os.environ.get("VERTEX_PROJECT")
location = os.environ.get("VERTEX_LOCATION")
# Add system instruction loading if needed here or get from context
SYSTEM_INSTRUCTION = """You are an AI assistant specialized... (load your full instruction)"""


if not project or not location:
    raise ValueError("VERTEX_PROJECT and VERTEX_LOCATION environment variables must be set.")

coordinator = AICoordinator()

# --- REGISTER THE ACTUAL AI MODULE ---
try:
    vertex_module = VertexAIClient(project=project, location=location)
    coordinator.register_module("vertex_ai", vertex_module)
    coordinator.set_context("system_instruction", SYSTEM_INSTRUCTION) # Set context if module uses it
    # coordinator.register_tts_module() # Keep if API might trigger TTS
except Exception as e:
    app.logger.error(f"Failed to initialize AI modules: {e}")
    # Decide how to handle this - maybe exit or run with limited functionality?
    # raise e # Or re-raise to stop the app

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    # You might want user_id, session_id from frontend too
    # user_id = data.get('user_id', 'api_user')
    # session_id = data.get('session_id', 'api_session')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # --- Use route_message to send to the AI module ---
        message_to_ai = {
            "target_module": "vertex_ai", # The name you registered the module with
            "content": user_input
            # Add other relevant info if needed by handle_message
            # "user_id": user_id,
        }
        # The coordinator's route_message will pass context (like system_instruction)
        # to the module's handle_message method.
        response = coordinator.route_message(message_to_ai)

        if response is None:
             # Log the error using app.logger or coordinator.logger
             app.logger.error(f"Received no response from module 'vertex_ai' for input: {user_input[:50]}...")
             return jsonify({'error': 'AI module failed to generate a response.'}), 500

        # Optional: Trigger TTS if needed based on response or request
        # tts_message = {"target_module": "text_to_speech", "content": response}
        # coordinator.route_message(tts_message) # Fire-and-forget or handle response

        return jsonify({'response': response})
    except Exception as e:
        # Log the exception
        app.logger.error(f"Error in /chat endpoint: {e}", exc_info=True)
        return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    # Use a production server (like Gunicorn or Waitress) instead of debug=True in production
    app.run(debug=True, port=5000)