from enum import Enum
import csv


class StateType(Enum):
    NON_FINAL = 0
    FINAL = 1


class Transition:
    def __init__(self, _from, _to, _input):
        self._from = _from
        self._to = _to
        self._input = _input


class State:
    def __init__(
            self,
            identifier,
            state_type: StateType = StateType.NON_FINAL):
        self.identifier = identifier
        self.state_type: StateType = state_type
        self._out: list[Transition] = []
        self._in: list[Transition] = []

    def connect_to(self, _to: '__class__', _input):
        transition = Transition(_from=self, _to=_to, _input=_input)
        self._out.append(transition)

    def connect_from(self, _from: '__class__', _input):
        transition = Transition(_from=_from, _to=self, _input=_input)
        self._in.append(transition)


class Automaton:
    def __init__(self, csv_file_or_dict):
        self.table: dict = dict()
        if(type(csv_file_or_dict) == str):
            self.table = self.get_table_from_csv(csv_file_or_dict)
        else:
            self.table = self.get_table_from_dict(csv_file_or_dict)

    def get_table_from_dict(self, d):
        table = {State(k): dict() for k in d}
        for k in d:

