import datetime as _exam_dt
import random as _exam_random
import string as _exam_string
import sys as _exam_sys
import types as _exam_types

class _ExamAssumptionFailed(Exception):
  pass

class _ExamStrategy:
  def __init__(self, fn):
    self._fn = fn

  def draw(self, rng):
    return self._fn(rng)

class _ExamStrategiesModule(_exam_types.ModuleType):
  def integers(self, min_value=-100, max_value=100):
    min_value = -100 if min_value is None else int(min_value)
    max_value = 100 if max_value is None else int(max_value)
    if min_value > max_value:
      min_value, max_value = max_value, min_value
    return _ExamStrategy(lambda rng: rng.randint(min_value, max_value))

  def booleans(self):
    return _ExamStrategy(lambda rng: bool(rng.randint(0, 1)))

  def floats(self, min_value=-1000.0, max_value=1000.0, allow_nan=False, allow_infinity=False):
    min_value = -1000.0 if min_value is None else float(min_value)
    max_value = 1000.0 if max_value is None else float(max_value)
    if min_value > max_value:
      min_value, max_value = max_value, min_value
    def _draw(rng):
      value = rng.uniform(min_value, max_value)
      if not allow_nan and value != value:
        return 0.0
      if not allow_infinity and value in (float("inf"), float("-inf")):
        return 0.0
      return value
    return _ExamStrategy(_draw)

  def sampled_from(self, values):
    values = list(values)
    if not values:
      values = [None]
    return _ExamStrategy(lambda rng: values[rng.randrange(len(values))])

  def text(self, alphabet=None, min_size=0, max_size=12):
    alphabet = alphabet or (_exam_string.ascii_letters + _exam_string.digits)
    min_size = max(0, int(min_size or 0))
    max_size = max(min_size, int(max_size or min_size))
    alphabet = list(alphabet) if alphabet else list("abc")
    if not alphabet:
      alphabet = list("abc")
    def _draw(rng):
      size = rng.randint(min_size, max_size)
      return "".join(alphabet[rng.randrange(len(alphabet))] for _ in range(size))
    return _ExamStrategy(_draw)

  def lists(self, elements=None, min_size=0, max_size=10):
    elements = elements or self.integers()
    min_size = max(0, int(min_size or 0))
    max_size = max(min_size, int(max_size or min_size))
    return _ExamStrategy(lambda rng: [elements.draw(rng) for _ in range(rng.randint(min_size, max_size))])

  def tuples(self, *strategies):
    if not strategies:
      return _ExamStrategy(lambda rng: ())
    return _ExamStrategy(lambda rng: tuple(s.draw(rng) for s in strategies))

  def one_of(self, *strategies):
    if not strategies:
      return self.sampled_from([None])
    return _ExamStrategy(lambda rng: strategies[rng.randrange(len(strategies))].draw(rng))

  def dates(self, min_value=None, max_value=None):
    min_value = min_value or _exam_dt.date(1990, 1, 1)
    max_value = max_value or _exam_dt.date(2035, 12, 31)
    if min_value > max_value:
      min_value, max_value = max_value, min_value
    delta = (max_value - min_value).days
    return _ExamStrategy(lambda rng: min_value + _exam_dt.timedelta(days=rng.randint(0, delta)))

def _exam_assume(condition):
  if not condition:
    raise _ExamAssumptionFailed()

def _exam_settings(*args, **kwargs):
  max_examples = kwargs.get("max_examples")
  def _decorator(fn):
    if max_examples is not None:
      setattr(fn, "_exam_max_examples", int(max_examples))
    return fn
  return _decorator

def _exam_given(*given_args, **given_kwargs):
  def _decorator(fn):
    def _wrapped():
      examples = int(getattr(fn, "_exam_max_examples", 1000))
      attempts = 0
      successes = 0
      rng = _exam_random.Random(1337)
      while successes < examples and attempts < examples * 20:
        attempts += 1
        args = [s.draw(rng) for s in given_args]
        kwargs = {k: s.draw(rng) for k, s in given_kwargs.items()}
        try:
          fn(*args, **kwargs)
          successes += 1
        except _ExamAssumptionFailed:
          continue
        except Exception as exc:
          setattr(exc, "_exam_counterexample", {"args": args, "kwargs": kwargs, "attempt": attempts})
          raise
    _wrapped.__name__ = fn.__name__
    _wrapped.__doc__ = fn.__doc__
    _wrapped._is_exam_given = True
    return _wrapped
  return _decorator

_hypothesis_module = _exam_types.ModuleType("hypothesis")
_strategies_module = _ExamStrategiesModule("hypothesis.strategies")

_hypothesis_module.given = _exam_given
_hypothesis_module.settings = _exam_settings
_hypothesis_module.assume = _exam_assume
_hypothesis_module.strategies = _strategies_module
_hypothesis_module.HealthCheck = _exam_types.SimpleNamespace()

_exam_sys.modules["hypothesis"] = _hypothesis_module
_exam_sys.modules["hypothesis.strategies"] = _strategies_module
