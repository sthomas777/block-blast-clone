from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Iterable

type Action[Context] = Callable[[Context], None]


class InvalidTransaction(Exception):
    pass


@dataclass
class StateMachine[State: Enum, Event: Enum, Context]:
    transitions: dict[tuple[State, Event], tuple[State, Action[Context]]] = field(
        default_factory=dict[tuple[State, Event], tuple[State, Action[Context]]]
    )

    def add_transition(
        self, from_state: State, event: Event, to_state: State, func: Action[Context]
    ) -> None:
        self.transitions[(from_state, event)] = (to_state, func)

    def next_state(self, state: State, event: Event) -> tuple[State, Action[Context]]:
        try:
            return self.transitions[(state, event)]
        except KeyError as e:
            raise InvalidTransaction(f"Cannot {event.name} when {state.name}") from e

    def handle(self, context: Context, state: State, event: Event) -> State:
        next_state, action = self.next_state(state, event)
        action(context)
        return next_state

    def transition(
        self, from_state: State | Iterable[State], event: Event, to_state: State
    ):
        if not isinstance(from_state, Iterable):
            from_state = (from_state,)

        def decorator(func: Action[Context]) -> Action[Context]:
            for s in from_state:
                self.add_transition(s, event, to_state, func)
            return func

        return decorator
