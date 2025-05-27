import unittest
import discord
from discord.ext import commands
from src.bot import bot

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.bot = bot

    def test_verify_command(self):
        # Test the verify command (mocking Discord interactions)
        pass

    def test_menu_command(self):
        # Test the menu command
        pass

if __name__ == '__main__':
    unittest.main()