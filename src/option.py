#!/usr/bin/env python3

class Option:

    description: str


    def __init__(self, description: str):
        self.description = description


    def __str__(self) -> str:
        return self.description
    

    # TODO: define apply(GameState)