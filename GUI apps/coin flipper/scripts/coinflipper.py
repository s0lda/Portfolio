import random

class CoinFlipper:
    def __init__(self) -> None:
        super().__init__()

    def flip_the_coin(self) -> str:
        choices = ("edge", "head", "notes", "question", "tail")
        return random.choice(choices)

    def out_message(self, coin: str) -> str:
        if coin == "edge":
            return "Landed on the edge."
        elif coin == "head":
            return "Head!"
        elif coin == "notes":
            return "Are you magician? Turning coins in to notes?"
        elif coin == "question":
            return "Lost the coin."
        else:
            return "Tail!"
