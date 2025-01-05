from flask import Flask, jsonify, request
import asyncio
from threading import Thread
from src.handlers.audio_handler import AudioOnlyHandler
from src.handlers.text_handler import TextOnlyHandler
from src.config import INPUT_MODE_AUDIO, INPUT_MODE_TEXT
from src.utils.logger import setup_logger

app = Flask(__name__)
logger = setup_logger("FlaskAPI")

# Global state variables
handler = None
running = False

@app.route("/start", methods=["POST"])
def start():
    global handler, running
    if running:
        return jsonify({"message": "Already running!"}), 400

    input_mode = request.json.get("input_mode", INPUT_MODE_TEXT)
    try:
        if input_mode == INPUT_MODE_AUDIO:
            handler = AudioOnlyHandler(logger)
        elif input_mode == INPUT_MODE_TEXT:
            handler = TextOnlyHandler(logger)
        else:
            return jsonify({"error": "Unsupported input mode"}), 400

        running = True
        Thread(target=lambda: asyncio.run(handler.run())).start()
        return jsonify({"message": "Handler started successfully."}), 200

    except Exception as e:
        logger.error(f"Error starting handler: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/stop", methods=["POST"])
def stop():
    global handler, running
    if not running:
        return jsonify({"message": "Not running!"}), 400

    try:
        if handler:
            handler.close()
        running = False
        return jsonify({"message": "Handler stopped successfully."}), 200
    except Exception as e:
        logger.error(f"Error stopping handler: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
