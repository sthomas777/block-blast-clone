from enum import Enum, auto

import pytest

from src.game.statemachine import StateMachine, InvalidTransaction


def test_add_transition() -> None:
    class State(Enum):
        A = auto()
        B = auto()

    class Event(Enum):
        GO = auto()

    sm = StateMachine()
    sm.add_transition(State.A, Event.GO, State.B, lambda ctx: None)
    assert (State.A, Event.GO) in sm.transitions


def test_next_state() -> None:
    class State(Enum):
        A = auto()
        B = auto()

    class Event(Enum):
        GO = auto()

    sm = StateMachine()
    sm.add_transition(State.A, Event.GO, State.B, lambda ctx: None)
    next_state, action = sm.next_state(State.A, Event.GO)
    assert next_state == State.B


def test_invalid_transition() -> None:
    class State(Enum):
        A = auto()
        B = auto()

    class Event(Enum):
        GO = auto()

    sm = StateMachine()
    with pytest.raises(InvalidTransaction):
        sm.next_state(State.A, Event.GO)


def test_handle() -> None:
    class State(Enum):
        A = auto()
        B = auto()

    class Event(Enum):
        GO = auto()

    class Context:
        pass

    sm = StateMachine()
    sm.add_transition(State.A, Event.GO, State.B, lambda ctx: None)
    ctx = Context()
    next_state = sm.handle(ctx, State.A, Event.GO)
    assert next_state == State.B
