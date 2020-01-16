from unittest import TestCase
from atsd_client.models import EvaluateMode, Evaluate

MODE = EvaluateMode.NOT_STRICT
LIBS = ["lib.mvel"]
EXPRESSION = "expression"
SCRIPT = "script.mvel"
ORDER = 1
TIMEZONE = "Europe/Moscow"

INCORRECT_VALUE = "INCORRECT_VALUE"


class TestEvaluate(TestCase):

    def test_init(self):
        evaluate = Evaluate(MODE, LIBS, EXPRESSION, SCRIPT, ORDER, TIMEZONE)
        self.assertEqual(MODE, evaluate.mode)
        self.assertEqual(LIBS, evaluate.libs)
        self.assertEqual(EXPRESSION, evaluate.expression)
        self.assertEqual(SCRIPT, evaluate.script)
        self.assertEqual(ORDER, evaluate.order)
        self.assertEqual(TIMEZONE, evaluate.timezone)

    def test_set_mode(self):
        evaluate = Evaluate()
        evaluate.set_mode(MODE)
        self.assertEqual(MODE, evaluate.mode)
        self.assertRaises(ValueError, evaluate.set_mode, INCORRECT_VALUE)

    def test_set_libs(self):
        evaluate = Evaluate()
        evaluate.set_libs(LIBS)
        self.assertEqual(LIBS, evaluate.libs)

    def test_set_expression(self):
        evaluate = Evaluate()
        evaluate.set_expression(EXPRESSION)
        self.assertEqual(EXPRESSION, evaluate.expression)
        self.assertRaises(ValueError, evaluate.set_expression, 1)

    def test_set_script(self):
        evaluate = Evaluate()
        evaluate.set_script(SCRIPT)
        self.assertEqual(SCRIPT, evaluate.script)
        self.assertRaises(ValueError, evaluate.set_script, 1)

    def test_set_order(self):
        evaluate = Evaluate()
        evaluate.set_order(ORDER)
        self.assertEqual(ORDER, evaluate.order)
        self.assertRaises(ValueError, evaluate.set_order, INCORRECT_VALUE)

    def test_set_timezone(self):
        evaluate = Evaluate()
        evaluate.set_timezone(TIMEZONE)
        self.assertEqual(TIMEZONE, evaluate.timezone)
        self.assertRaises(ValueError, evaluate.set_timezone, 1)
