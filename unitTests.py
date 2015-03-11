from unittest import TestCase
import Simulators
from Tennis import Player


class HardSimulatorTest(TestCase):
    def test_FullProbability(self):
        simulator = Simulators.HardSimulator()
        skill1, skill2 = 0.2, 0.8
        prob1 = simulator.getFirstVictoryProbability(skill1, skill2)
        prob2 = simulator.getFirstVictoryProbability(skill2, skill1)
        self.assertAlmostEqual(prob1 + prob2, 1.0)

    def test_StrongestWins(self):
        a = Player("a", 0.0)
        b = Player("b", 0.2)
        c = Player("c", 0.4)
        d = Player("d", 1.0)
        simulator = Simulators.HardSimulator()
        self.assertFalse(simulator.firstPlayerWon(a, b))
        self.assertFalse(simulator.firstPlayerWon(b, c))
        self.assertFalse(simulator.firstPlayerWon(c, d))
        self.assertFalse(simulator.firstPlayerWon(a, c))
        self.assertFalse(simulator.firstPlayerWon(a, d))
        self.assertFalse(simulator.firstPlayerWon(b, d))

class RandomizedSimulatorTest(TestCase):
    def test_FullProbability(self):
        simulator = Simulators.RandomizedSimulator()
        skill1, skill2 = 0.2, 0.8
        prob1 = simulator.getFirstVictoryProbability(skill1, skill2)
        prob2 = simulator.getFirstVictoryProbability(skill2, skill1)
        self.assertAlmostEqual(prob1 + prob2, 1.0)
    def test_EqualChances(self):
        simulator = Simulators.RandomizedSimulator()
        self.assertEqual(simulator.getFirstVictoryProbability(0.7, 0.7), 0.5)
        self.assertEqual(simulator.getFirstVictoryProbability(0.0, 0.0), 0.5)
        self.assertEqual(simulator.getFirstVictoryProbability(1.0, 1.0), 0.5)
    def test_skewnessGrowth(self):
        simulator1 = Simulators.RandomizedSimulator(5)
        simulator2 = Simulators.RandomizedSimulator(20)
        skill1, skill2 = 0.2, 0.8
        prob1 = simulator1.getFirstVictoryProbability(skill1, skill2)
        prob2 = simulator2.getFirstVictoryProbability(skill1, skill2)
        self.assertGreater(prob1, prob2)

class HardRandomSimulatorTest(TestCase):
    def test_FullProbability(self):
        simulator = Simulators.HardRandomSimulator()
        skill1, skill2 = 0.2, 0.8
        prob1 = simulator.getFirstVictoryProbability(skill1, skill2)
        prob2 = simulator.getFirstVictoryProbability(skill2, skill1)
        self.assertAlmostEqual(prob1 + prob2, 1.0)
    def test_EqualChances(self):
        simulator = Simulators.HardRandomSimulator()
        self.assertEqual(simulator.getFirstVictoryProbability(0.7, 0.7), 0.5)
        self.assertEqual(simulator.getFirstVictoryProbability(0.0, 0.0), 0.5)
        self.assertEqual(simulator.getFirstVictoryProbability(1.0, 1.0), 0.5)

def NonTransitiveSimulatorTest(TestCase):
    def test_NewbieWins(self):
        a = Player("a", 0.0)
        b = Player("b", 0.2)
        c = Player("c", 0.4)
        d = Player("d", 1.0)
        simulator = Simulators.NonTransitiveSimulator()
        self.assertFalse(simulator.firstPlayerWon(a, b))
        self.assertFalse(simulator.firstPlayerWon(b, a))
        self.assertFalse(simulator.firstPlayerWon(b, c))
        self.assertFalse(simulator.firstPlayerWon(c, b))
        self.assertFalse(simulator.firstPlayerWon(c, d))
        self.assertFalse(simulator.firstPlayerWon(d, c))

class RealisticSimulatorTest(TestCase):
    def test_TheSameWinsAlways(self):
        a = Player("a")
        b = Player("b")
        simulator = Simulators.RealisticSimulator()
        winner = simulator.getWinner(a, b)
        self.assertEqual(simulator.getWinner(a, b), winner)
        self.assertEqual(simulator.getWinner(a, b), winner)
