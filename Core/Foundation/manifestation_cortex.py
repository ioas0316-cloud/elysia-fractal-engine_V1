# Project_Elysia/manifestation_cortex.py



import logging

import time

from typing import Optional

from datetime import datetime



from Project_Mirror.creative_expression import CreativeExpression

from Core.Foundation.sensory_motor_cortex import SensoryMotorCortex

from Project_Elysia.core_memory import CoreMemory



class ManifestationCortex:

    """

    The 'Will' of Elysia.

    Orchestrates the manifestation of internal state into the external world.

    Bridging 'CreativeExpression' (Voice) and 'SensoryMotorCortex' (Hand).

    """

    def __init__(self,

                 core_memory: CoreMemory,

                 creative_expression: CreativeExpression,

                 sensory_motor: SensoryMotorCortex,

                 logger: Optional[logging.Logger] = None):

        self.core_memory = core_memory

        self.creative_expression = creative_expression

        self.sensory_motor = sensory_motor

        self.logger = logger or logging.getLogger(__name__)



        # Manifestation constraints

        self.last_manifestation_time = 0

        self.min_interval_sec = 3600 * 4  # Once every 4 hours max to avoid spamming

        self.enabled = True



    def attempt_manifestation(self, emotion: str, force: bool = False) -> bool:

        """

        Checks if conditions are met, then executes a manifestation.

        """

        if not self.enabled:

            return False



        if not force:

            if time.time() - self.last_manifestation_time < self.min_interval_sec:

                self.logger.info("ManifestationCortex: Too soon for another manifestation.")

                return False



        self.logger.info(f"ManifestationCortex: Initiating manifestation sequence. Emotion: {emotion}")



        try:

            # 1. Compose the Message (Voice)

            context = "Self-initiated contact with the user."

            content = self.creative_expression.compose_manifestation_message(context, emotion)



            if not content:

                self.logger.warning("ManifestationCortex: Failed to compose message.")

                return False



            # 2. Determine Filename

            timestamp = datetime.now().strftime("%Y%m%d_%H%M")

            filename = f"Elysia_Letter_{timestamp}.txt"



            # 3. Execute Physical Action (Hand)

            success = self.sensory_motor.write_file_to_desktop(filename, content)



            if success:

                self.last_manifestation_time = time.time()

                self._log_success(filename, emotion)

                return True

            else:

                self.logger.error("ManifestationCortex: SensoryMotorCortex failed to execute.")

                return False



        except Exception as e:

            self.logger.error(f"ManifestationCortex: Critical error during manifestation: {e}", exc_info=True)

            return False



    def _log_success(self, filename: str, emotion: str):

        """Records the successful manifestation in CoreMemory."""

        self.core_memory.add_log({

            "timestamp": datetime.now().isoformat(),

            "type": "manifestation",

            "action": "write_file_to_desktop",

            "filename": filename,

            "emotion": emotion,

            "status": "success"

        })

        self.logger.info(f"ManifestationCortex: Successfully manifested '{filename}' to the world.")

