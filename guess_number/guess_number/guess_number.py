"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

import random

num_min, num_max = 1, 10

class GameState(rx.State):
    """The game state."""
    secret_number: int = random.randint(num_min, num_max)
    guess: int = 0
    message: str = f"I've chosen a number between {num_min} and {num_max}. Can you guess it?"
    def check_guess(self):
        """Check the player's guess against the secret number."""
        if self.guess == self.secret_number:
            self.message = "Congratulations! You guessed it!"
        elif self.guess < self.secret_number:
            self.message = "Too low! Try again."
        else:
            self.message = "Too high! Try again."

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Number Guessing Game"),
            rx.text(GameState.message),
            rx.input(type="number", on_change=GameState.set_guess),
            rx.button("Guess", on_click=GameState.check_guess),
            align_items="center",
        ),
        width="100%",
        height="100vh",
    )


app = rx.App()
app.add_page(index, title="Number Guessing Game")
