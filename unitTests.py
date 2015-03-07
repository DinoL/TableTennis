from unittest import TestCase
from Simulators import HardSimulator
from Simulators import RealisticSimulator
from Tennis import Player


class SimulatorTest(TestCase):
    def test_HardSimulator(self):
        a = Player("a", 0.2)
        b = Player("b", 0.4)
        simulator = HardSimulator()
        self.assertFalse(simulator.firstPlayerWon(a, b))

    def test_RealisticSimulator(self):
        a = Player("a")
        b = Player("b")
        simulator = RealisticSimulator()
        winner = simulator.getWinner(a, b)
        self.assertEqual(simulator.getWinner(a, b), winner)