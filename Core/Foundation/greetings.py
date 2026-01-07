#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A foundational module for generating simple, standardized greetings. Serves as a
basic template and entry point for new entities within Elysia.
"""

import logging
from typing import Union

# Set up a standard logger for the module
logger = logging.getLogger(__name__)


class Greetings:
    """
    A class dedicated to generating various greeting messages.
    """

    def say_hello(self, name: str = 'World') -> str:
        """
        Constructs a personalized greeting string.

        If no name is provided, it defaults to 'Hello, World!'. This method
        gracefully handles non-string inputs by logging an error and returning
        an error message.

        Args:
            name (str, optional): The name to include in the greeting.
                                  Defaults to 'World'.

        Returns:
            str: The formatted greeting string or an error message if the
                 input is invalid.
        """
        logger.info("Attempting to generate a greeting for '%s'.", name)
        try:
            # Explicitly check for the correct type to ensure string formatting works.
            if not isinstance(name, str):
                raise TypeError(f"Argument 'name' must be a string, not {type(name).__name__}.")

            greeting = f"Hello, {name}!"
            logger.debug("Successfully generated greeting: '%s'", greeting)
            return greeting

        except TypeError as e:
            logger.error("Type error while generating greeting: %s", e, exc_info=True)
            return "Error: Invalid name type provided."
        except Exception as e:
            # Catch any other unexpected errors.
            logger.critical("An unexpected error occurred in say_hello: %s", e, exc_info=True)
            return "Error: An unexpected error occurred."


# This block allows the file to be run as a standalone script for testing.
if __name__ == '__main__':
    # Configure basic logging for demonstration purposes.
    # In a real application, logging would be configured at a higher level.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s: %(message)s'
    )

    logger.info("Executing greetings module as a standalone script.")

    # Instantiate the class
    greeter = Greetings()

    # --- Test Cases ---
    print("\n--- Running Test Cases ---")

    # 1. Default case
    print(f"1. Default Call: {greeter.say_hello()}")

    # 2. Standard case with a name
    print(f"2. Named Call: {greeter.say_hello('Elysia')}")

    # 3. Empty string case
    print(f"3. Empty String Call: {greeter.say_hello('')}")

    # 4. Error case with an integer
    # This will trigger the TypeError handling.
    print(f"4. Invalid Type Call (int): {greeter.say_hello(123)}") # type: ignore

    # 5. Error case with a list
    # This will also trigger the TypeError handling.
    print(f"5. Invalid Type Call (list): {greeter.say_hello(['Code', 'Weaver'])}") # type: ignore

    print("\n--- Test Cases Complete ---")