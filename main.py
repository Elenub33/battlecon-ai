#!/usr/bin/env python3
from src.agent import Agent
from src.fighters.fighter_loader import FighterLoader


if __name__ == "__main__":
    f1 = FighterLoader.load_fighter_from_module("eligor")
    f2 = FighterLoader.load_fighter_from_module("shekhtur")
    a1 = Agent(f1)
    a2 = Agent(f2)
    print(f1)
    print(f2)