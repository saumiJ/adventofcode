# Link to task: https://adventofcode.com/2022/day/7

import re

from ctypes import c_ushort
from typing import Optional, List, Tuple, Union

Source = Union["Component", "Signal"]


class Signal:
    def __init__(self, value: Union[int, str]):
        self._value = int(value)
        self.reading = None

    def resolve(self):
        if self.reading is not None:
            return self.reading
        self.reading = c_ushort(self._value).value
        return self.reading

    def reset(self):
        self.reading = None


class Component:
    def __init__(self, label: str, srcs: Optional[List[Source]] = None):
        self.label = label
        self.srcs = list() if srcs is None else srcs
        self.reading = None

    def add_srcs(self, srcs: List[Source]):
        self.srcs.extend(srcs)

    def resolve(self):
        if self.reading is not None:
            return self.reading
        for _src in self.srcs:
            if _src.reading is None:
                _src.resolve()
        self.reading = self.resolver()
        return self.reading

    def resolver(self):
        raise NotImplementedError

    def reset(self):
        if self.reading is None:
            return
        for _src in self.srcs:
            if _src.reading is not None:
                _src.reset()
        self.reading = None
        return


class Wire(Component):
    def add_srcs(self, srcs: List[Source]):
        super().add_srcs(srcs)
        assert len(self.srcs) <= 1

    def resolver(self):
        return self.srcs[0].resolve()


class Not(Component):
    def __init__(self, srcs: Optional[List[Source]] = None):
        assert len(srcs) == 1
        super().__init__("NOT", srcs)

    def resolver(self):
        return Signal(~self.srcs[0].reading).resolve()


class LeftShift(Component):
    def __init__(self, shift_size: int, srcs: Optional[List[Source]] = None):
        assert len(srcs) == 1
        super().__init__("LSHIFT", srcs)
        self.shift_size = shift_size

    def resolver(self):
        return Signal(self.srcs[0].reading << self.shift_size).resolve()


class RightShift(Component):
    def __init__(self, shift_size: int, srcs: Optional[List[Source]] = None):
        assert len(srcs) == 1
        super().__init__("RSHIFT", srcs)
        self.shift_size = shift_size

    def resolver(self):
        return Signal(self.srcs[0].reading >> self.shift_size).resolve()


class And(Component):
    def __init__(self, srcs: Optional[List[Source]] = None):
        assert len(srcs) == 2
        super().__init__("AND", srcs)

    def resolver(self):
        return Signal(self.srcs[0].reading & self.srcs[1].reading).resolve()


class Or(Component):
    def __init__(self, srcs: Optional[List[Source]] = None):
        assert len(srcs) == 2
        super().__init__("OR", srcs)

    def resolver(self):
        return Signal(self.srcs[0].reading | self.srcs[1].reading).resolve()


class Circuit:
    def __init__(self):
        self.wire_label_to_wire_object = self.l2o = dict()

    def add_wires(self, labels: Union[str, List[str]]) -> Union[Wire, List[Wire]]:
        if isinstance(labels, str):
            labels = [labels]
        wires = list()
        for label in labels:
            if label not in self.l2o.keys():
                self.l2o[label] = Wire(label)
            wires.append(self.l2o[label])
        _w = wires[0] if len(wires) == 1 else wires
        return _w

    def get_reading_for_wire(self, label: str) -> int:
        return self.wire_label_to_wire_object[label].resolve()

    def reset(self, label: str):
        self.wire_label_to_wire_object[label].reset()


def create_sources(txt: Union[str, List[str]], _crc: Circuit) -> Tuple[Union[Source, List[Source]], Circuit]:
    if isinstance(txt, str):
        txt = [txt]
    s_list = list()
    for txt_i in txt:
        s = Signal(txt_i) if txt_i.isnumeric() else _crc.add_wires(txt_i)
        s_list.append(s)
    s = s_list[0] if len(s_list) == 1 else s_list
    return s, _crc


def parse_not_gate(line: str, crc: Circuit):
    lb_l, lb_r = re.search(r"NOT ([a-z]+|[0-9]+) -> ([a-z]+)", line).groups()
    (s_l, crc), w_r = create_sources(lb_l, crc), crc.add_wires(lb_r)
    g = Not([s_l])
    w_r.add_srcs([g])


def parse_shift_gate(line: str, crc: Circuit, gate_name: str):
    lb_l, shift, lb_r = re.search(rf"([a-z]+|[0-9]+) {gate_name} ([0-9]+) -> ([a-z]+)", line).groups()
    (s_l, crc), w_r = create_sources(lb_l, crc), crc.add_wires(lb_r)
    gate_class = LeftShift if gate_name == "LSHIFT" else RightShift
    g = gate_class(int(shift), [s_l])
    w_r.add_srcs([g])


def parse_binary_gate(line: str, crc: Circuit, gate_name: str):
    lb_l1, lb_l2, lb_r = re.search(rf"([a-z]+|[0-9]+) {gate_name} ([a-z]+|[0-9]+) -> ([a-z]+)", line).groups()
    ((s_l1, s_l2), crc), w_r = create_sources([lb_l1, lb_l2], crc), crc.add_wires(lb_r)
    gate_class = And if gate_name == "AND" else Or
    g = gate_class([s_l1, s_l2])
    w_r.add_srcs([g])


def parse_signal_assignment(line: str, crc: Circuit):
    src, lb = re.search(r"([0-9]+) -> ([a-z]+)", line).groups()
    w = crc.add_wires(lb)
    w.add_srcs([Signal(src)])


def parse_wire_connection(line: str, crc: Circuit):
    lb_l, lb_r = re.search(r"([a-z]+) -> ([a-z]+)", line).groups()
    w_l, w_r = crc.add_wires([lb_l, lb_r])
    w_r.add_srcs([w_l])


def run_circuit(instruction_manual_path: str, crc: Circuit):
    with open(instruction_manual_path, "r") as f:
        lines = f.read().splitlines()
    for line in lines:
        gate_search = re.search(r"[A-Z]+", line)
        if gate_search:
            gate_name = gate_search.group()
            if gate_name == "NOT":
                parse_not_gate(line, crc)
            elif gate_name in ["LSHIFT", "RSHIFT"]:
                parse_shift_gate(line, crc, gate_name)
            elif gate_name in ["AND", "OR"]:
                parse_binary_gate(line, crc, gate_name)
            else:
                raise NotImplementedError(f"Unsupported gate: {gate_name}")
        else:
            if re.search(r"[0-9]+ -> [a-z]+", line):
                parse_signal_assignment(line, crc)
            elif re.search(r"[a-z]+ -> [a-z]+", line):
                parse_wire_connection(line, crc)
            else:
                raise NotImplementedError(f"Unsupported instruction: {line}")
    return crc


_crc = Circuit()
_crc = run_circuit(instruction_manual_path="input/2015.07.1.in", crc=_crc)
print(f"Reading for wire-a (part-1): {_crc.get_reading_for_wire('a')}")
_crc = Circuit()
_crc = run_circuit(instruction_manual_path="input/2015.07.2.in", crc=_crc)
print(f"Reading for wire-a (part-2): {_crc.get_reading_for_wire('a')}")
