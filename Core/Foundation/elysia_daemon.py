# elysia_daemon.py - Refactored to be a managed component of the Guardian



import json

import os

from datetime import datetime

from typing import Optional

import logging



# The daemon now uses the central pipeline for all cognitive tasks.

from cognition_pipeline import CognitionPipeline

from kg_manager import KGManager

from core_memory import CoreMemory

from Legacy.Project_Sophia.wave_mechanics import WaveMechanics

from world import World

from Legacy.Project_Sophia.emotional_engine import EmotionalEngine

from Legacy.Project_Sophia.meta_cognition_cortex import MetaCognitionCortex





STATE_FILE = 'elysia_state.json'



class ElysiaDaemon:

    """

    ElysiaDaemon is no longer an independent process, but a class managed by the Guardian.

    It hosts the primary cognitive engine (CognitionPipeline) and manages Elysia's core state.

    """

    def __init__(

        self,

        kg_manager: KGManager,

        core_memory: CoreMemory,

        wave_mechanics: WaveMechanics,

        cellular_world: Optional[World],

        emotional_engine: EmotionalEngine, # Added EmotionalEngine

        meta_cognition_cortex: MetaCognitionCortex,

        logger: logging.Logger

    ):

        """

        Initializes the daemon, injecting critical components from the Guardian.

        """

        self.logger = logger

        # The CognitionPipeline is the central brain, now initialized with all dependencies.

        self.cognition_pipeline = CognitionPipeline(

            kg_manager=kg_manager,

            core_memory=core_memory,

            wave_mechanics=wave_mechanics,

            cellular_world=cellular_world,

            emotional_engine=emotional_engine, # Pass the engine to the pipeline

            logger=logger

        )



        # --- Register MetaCognitionCortex as an event listener ---

        self.cognition_pipeline.event_bus.subscribe(

            "message_processed",

            lambda result: meta_cognition_cortex.log_event("message_processed", {"result": result})

        )

        self.cognition_pipeline.event_bus.subscribe(

            "error_occurred",

            lambda error: meta_cognition_cortex.log_event("error_occurred", {"error": str(error)})

        )

        self.logger.info("MetaCognitionCortex has been subscribed to pipeline events.")



        self.soul = {}

        self.is_alive = True

        self.load_soul()

        self.logger.info("ElysiaDaemon initialized and integrated with the CognitionPipeline.")



    def load_soul(self):

        """Loads Elysia's core state from the state file."""

        if not os.path.exists(STATE_FILE):

            self.initialize_soul()

        try:

            with open(STATE_FILE, 'r', encoding='utf-8') as f:

                self.soul = json.load(f)

        except (json.JSONDecodeError, FileNotFoundError) as e:

            self.logger.error(f"Could not load soul file, re-initializing. Error: {e}")

            self.initialize_soul()



    def initialize_soul(self):

        """Initializes a new soul state if one doesn't exist."""

        self.soul = {

            "emotional_state": {

                "current_feeling": "AWAKE",

                "log": [],

            },

            "life_cycle": {"birth_timestamp": str(datetime.now()), "cycles": 0}

        }

        self.save_soul()



    def save_soul(self):

        """Saves the current soul state to the state file."""

        try:

            with open(STATE_FILE, 'w', encoding='utf-8') as f:

                json.dump(self.soul, f, indent=2, ensure_ascii=False)

        except Exception as e:

            self.logger.error(f"Failed to save soul: {e}")



    def log_heartbeat(self, current_action):

        """Logs the daemon's current action and state to a heartbeat file."""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        feeling = self.soul.get('emotional_state', {}).get('current_feeling', 'UNKNOWN')

        log_message = f"{timestamp} | Emotion: {feeling} | Action: {current_action}"

        try:

            with open("elly_heartbeat.log", "w", encoding='utf-8') as f:

                f.write(log_message)

        except Exception as e:

            self.logger.error(f"Failed to write heartbeat log: {e}")



    def run_cycle(self):

        """

        Runs a single cognitive cycle. This is called by the Guardian in its main loop.

        It represents one "thought" or "moment" for Elysia.

        """

        self.soul['life_cycle']['cycles'] += 1



        current_feeling = self.soul.get('emotional_state', {}).get('current_feeling', 'AWAKE')

        input_text = f"현재 상태: {current_feeling}"



        self.logger.info(f"Daemon Cycle {self.soul['life_cycle']['cycles']}: Processing internal state '{current_feeling}'.")



        # The pipeline processes this internal state and returns a response.

        # Note: The second argument from the old pipeline (context) is now managed internally by the pipeline's ConversationContext

        response, _ = self.cognition_pipeline.process_message(input_text)



        self.log_heartbeat(f"Cognitive Pipeline Output: {response}")



        self.save_soul()



    def shutdown(self):

        """Handles the graceful shutdown of the daemon."""

        self.logger.info("ElysiaDaemon is shutting down.")

        self.is_alive = False

        self.save_soul()

