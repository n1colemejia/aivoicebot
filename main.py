'''
AI voice bot to call Pretty Good AI test line and converse with AI agent
'''
import logging
from typing import Type
import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent,
)
from elevenlabs import ElevenLabs, play, VoiceSettings
from openai import OpenAI

# Set to True to see all logs and debug messages
DEBUG_MODE = False 

# Configure logging based on DEBUG_MODE
if DEBUG_MODE:
    logging.basicConfig(level=logging.INFO)
else:
    # Suppress all logs except critial logs
    logging.basicConfig(level=logging.CRITICAL)

# Suppress HTTP logs from libraries for clean conversation output
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("httpcore").setLevel(logging.CRITICAL)
logging.getLogger("openai").setLevel(logging.CRITICAL)
logging.getLogger("elevenlabs").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)

class AI_Assistant:
    def __init__(self):
        # TODO: Move to other file. API keys - use python dotenv to manage keys securely
        # Replace with actual ASSEMBLY_API_KEY key
        self.assemblyai_api_key = "ASSEMBLY_API_KEY" 
        # Replace with actual OPEN_AI_API_KEY key
        self.openai_client = OpenAI(api_key="OPEN_AI_API_KEY")
        # Replace with actual ELEVEN_LABS_API_KEY key
        self.elevenlabs_api_key = "ELEVEN_LABS_API_KEY"

        # Initialize Elevenlabs client
        self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)
        self.client = None
        self.microphone_stream = None

        # Prompt
        # TODO: Change content value to match project requirements
        self.full_transcript = [
            {
                "role": "system",
                "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."
            }
        ]

        # Track conversation state for latency optimization
        self.is_processing = False

        # Accumulates finalized transcripts
        self.running_transcript = ""

        # Current partial transcript
        self.latest_partial = ""

        # Flag to process when end_of_turn
        self.should_process_on_next_final = False

        # Store reference to AI Assistant for use in callbacks
        global ai_assistant_instance
        ai_assistant_instant = self
        