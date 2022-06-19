from vendor.states import State, build_state_map, BaseState


class CashlessDevice:

    def __init__(self):
        self.current_state: State = State.INACTIVE
        self._state_map: dict[State:BaseState] = build_state_map()

    def start(self):
        while True:
            next_state = self._state_map[self.current_state].run()

            if next_state is None:
                break

            self.set_state(next_state)

    def set_state(self, state: State):
        self.current_state = state
