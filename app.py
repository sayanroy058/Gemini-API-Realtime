import asyncio
import streamlit as st
from threading import Thread
from src.handlers.audio_handler import AudioOnlyHandler
# from src.handlers.text_handler import TextOnlyHandler
from src.config import INPUT_MODE_AUDIO
from src.utils.logger import setup_logger

# Initialize logger
logger = setup_logger("StreamlitApp")

# Streamlit layout
st.set_page_config(page_title="Gemini Live Streaming", layout="wide")
st.title("Sayan Live Streaming")

# Input mode selector
input_mode = st.radio("Select Input Mode:", [INPUT_MODE_AUDIO], horizontal=True)

# Control buttons
col1, col2 = st.columns(2)
with col1:
    start_button = st.button("Start", use_container_width=True)
with col2:
    stop_button = st.button("Stop", use_container_width=True)

# Output display
output_placeholder = st.empty()

# Global state variables
handler = None
running = False

def start_handler(mode):
    """Start the appropriate handler based on the selected mode."""
    global handler, running
    if running:
        st.warning("Handler is already running!")
        return

    try:
        if mode == INPUT_MODE_AUDIO:
            handler = AudioOnlyHandler(logger)
        # elif mode == INPUT_MODE_TEXT:
        #     handler = TextOnlyHandler(logger)
        else:
            st.error("Unsupported mode selected!")
            return

        running = True
        thread = Thread(target=lambda: asyncio.run(handler.run()))
        thread.start()
        st.success("Handler started successfully!")
    except Exception as e:
        logger.error(f"Error starting handler: {e}")
        st.error(f"Error starting handler: {str(e)}")

def stop_handler():
    """Stop the running handler."""
    global handler, running
    if not running:
        st.warning("No handler is running!")
        return

    try:
        if handler:
            handler.close()
        running = False
        st.success("Handler stopped successfully!")
    except Exception as e:
        logger.error(f"Error stopping handler: {e}")
        st.error(f"Error stopping handler: {str(e)}")

# Streamlit button actions
if start_button:
    start_handler(input_mode)

if stop_button:
    stop_handler()

# Displaying status
if running:
    output_placeholder.info("Handler is running...")
else:
    output_placeholder.info("Handler is stopped.")
