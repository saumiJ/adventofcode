import re

from ctypes import c_ushort
from typing import Optional, List, Union

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

    def get_reading_for_wire(self, label) -> int:
        return self.wire_label_to_wire_object[label].resolve()


def create_sources(txt: Union[str, List[str]], _crc: Circuit) -> (Union[Source, List[Source]], Circuit):
    if isinstance(txt, str):
        txt = [txt]
    s_list = list()
    for txt_i in txt:
        s = Signal(txt_i) if txt_i.isnumeric() else _crc.add_wires(txt_i)
        s_list.append(s)
    s = s_list[0] if len(s_list) == 1 else s_list
    return s, _crc


crc = Circuit()

with open("input/2015.07.in", "r") as f:
    lines = f.readlines()
for line in lines:
    gate_search = re.search(r"[A-Z]+", line)
    if gate_search is not None:
        gate_name = gate_search.group()
        if gate_name == "NOT":
            lb_l, lb_r = re.search(r"NOT ([a-z]+|[0-9]+) -> ([a-z]+)", line).groups()
            (s_l, crc), w_r = create_sources(lb_l, crc), crc.add_wires(lb_r)
            g = Not([s_l])
            w_r.add_srcs([g])
        elif gate_name == "LSHIFT":
            lb_l, shift, lb_r = re.search(r"([a-z]+|[0-9]+) LSHIFT ([0-9]+) -> ([a-z]+)", line).groups()
            (s_l, crc), w_r = create_sources(lb_l, crc), crc.add_wires(lb_r)
            g = LeftShift(int(shift), [s_l])
            w_r.add_srcs([g])
        elif gate_name == "RSHIFT":
            lb_l, shift, lb_r = re.search(r"([a-z]+|[0-9]+) RSHIFT ([0-9]+) -> ([a-z]+)", line).groups()
            (s_l, crc), w_r = create_sources(lb_l, crc), crc.add_wires(lb_r)
            g = RightShift(int(shift), [s_l])
            w_r.add_srcs([g])
        elif gate_name == "AND":
            lb_l1, lb_l2, lb_r = re.search(r"([a-z]+|[0-9]+) AND ([a-z]+|[0-9]+) -> ([a-z]+)", line).groups()
            ((s_l1, s_l2), crc), w_r = create_sources([lb_l1, lb_l2], crc), crc.add_wires(lb_r)
            g = And([s_l1, s_l2])
            w_r.add_srcs([g])
        elif gate_name == "OR":
            lb_l1, lb_l2, lb_r = re.search(r"([a-z]+|[0-9]+) OR ([a-z]+|[0-9]+) -> ([a-z]+)", line).groups()
            ((s_l1, s_l2), crc), w_r = create_sources([lb_l1, lb_l2], crc), crc.add_wires(lb_r)
            g = Or([s_l1, s_l2])
            w_r.add_srcs([g])
        else:
            raise NotImplementedError(gate_name)
    else:
        source_search = re.search(r"([0-9]+) -> ([a-z]+)", line)
        if source_search is not None:
            src, lb = source_search.groups()
            w = crc.add_wires(lb)
            w.add_srcs([Signal(src)])
        else:
            connector_search = re.search("([a-z]+) -> ([a-z]+)", line)
            if connector_search is not None:
                lb_l, lb_r = connector_search.groups()
                w_l, w_r = crc.add_wires([lb_l, lb_r])
                w_r.add_srcs([w_l])
            else:
                raise NotImplementedError(line)

print(f"Reading for wire-a (part-1): {crc.get_reading_for_wire('a')}")
