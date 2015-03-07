from unittest import TestCase
from Simulators import HardSimulator
from Simulators import RealisticSimulator
from Simulators import RandomizedSimulator
from Tennis import Player


class HardSimulatorTest(TestCase):
    def test_StrongestWins(self):
        a = Player("a", 0.0)
        b = Player("b", 0.2)
        c = Player("c", 0.4)
        d = Player("d", 1.0)
        simulator = HardSimulator()
        self.assertFalse(simulator.firstPlayerWon(a, b))
        self.assertFalse(simulator.firstPlayerWon(b, c))
        self.assertFalse(simulator.firstPlayerWon(c, d))
        self.assertFalse(simulator.firstPlayerWon(a, c))
        self.assertFalse(simulator.firstPlayerWon(a, d))
        self.assertFalse(simulator.firstPlayerWon(b, d))

class RealisticSimulatorTest(TestCase):
    def test_TheSameWinsAlways(self):
        a = Player("a")
        b = Player("b")
        simulator = RealisticSimulator()
        winner = simulator.getWinner(a, b)
        self.assertEqual(simulator.getWinner(a, b), winner)
        self.assertEqual(simulator.getWinner(a, b), winner)

class RandomizedSimulatorTest(TestCase):
    def test_EqualChances(self):
        simulator = RandomizedSimulator()
        self.assertEqual(simulator.getFirstVictoryProbability(0.7, 0.7), 0.5)
        self.assertEqual(simulator.getFirstVictoryProbability(0.0, 0.0), 0.5)
        self.assertEqual(simulator.getFirstVictoryProbability(1.0, 1.0), 0.5)