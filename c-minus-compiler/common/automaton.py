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
        if
        transition = Transition(_from=self, _to=_to, _input=_input)
        self._out.append(transition)

    def connect_from(self, _from: '__class__', _input):
        transition = Transition(_from=_from, _to=self, _input=_input)
        self._in.append(transition)


class Automaton:
    def __init__(self, csv_file_or_dict):
        dict_table: dict = dict()
        if(type(csv_file_or_dict) == str):
            dict_table = self.get_table_from_csv(csv_file_or_dict)
        elif(type(csv_file_or_dict) == dict):
            dict_table = csv_file_or_dict
        self.table = self.dict_to_table(dict_table)

    def get_table_from_csv(csv_file: str):
        pass

    def dict_to_table(dict_table: dict):
        table = dict()
