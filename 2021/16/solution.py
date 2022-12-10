import sys
import time
import math

def hex_to_bin(input: str):
    result = ''
    for v in input:
        result += bin(int(v, 16))[2:].zfill(4)
    return result

def bin_to_int(input: str):
    return int(input, 2)

class Packet:
    def __init__(self, input: str):
        self.input: str = input
        self.remainder: str = None
        self.subpackets: list[Packet] = []
        self.version: int = bin_to_int(input[0:3])
        self.type: int = bin_to_int(input[3:6])
        self.groups: list[str] = [] # Type 4 only
        self.length_type: int = None # All other types
        self.subpacket_length: int = None # Types with length type == 0
        self.subpacket_count: int = None # Types with length type == 1
        if self.type == 4:
            self.remainder = input[6:]
            self.identify_groups()
        else:
            self.length_type = int(input[6])
            if self.length_type == 0:
                self.subpacket_length = bin_to_int(input[7:22])
                self.remainder = input[22:]
            else:
                self.subpacket_count = bin_to_int(input[7:18])
                self.remainder = input[18:]
        self.find_children()

    def __str__(self):
        result = []
        result.append('*'*40)
        result.append(f"input={self.input}")
        result.append(f"version={self.version}")
        result.append(f"type={self.type}")
        if self.length_type is not None:
            result.append(f"length_type={self.length_type}")
        if self.subpacket_length is not None:
            result.append(f"subpacket_length={self.subpacket_length}")
        if self.subpacket_count is not None:
            result.append(f"subpacket_count={self.subpacket_count}")
        result.append(f"remainder={self.remainder}")
        result.append('*'*40)
        return '\n'.join(result)

    def find_children(self):
        if self.type == 4:
            return
        elif len(self.subpackets) == 0:
            if self.length_type == 0:
                while True:
                    subpacket = Packet(self.remainder)
                    self.subpackets.append(subpacket)
                    self.remainder = subpacket.remainder
                    if sum([c.length() for c in self.subpackets]) == self.subpacket_length:
                        break
            else:
                for _ in range(self.subpacket_count):
                    subpacket = Packet(self.remainder)
                    self.subpackets.append(subpacket)
                    self.remainder = subpacket.remainder

    def length(self):
        if self.type == 4:
            return 6 + sum(map(len, self.groups))
        else:
            if self.length_type == 0:
                return 22+self.subpacket_length
            else:
                return 18+sum([c.length() for c in self.subpackets])

    def identify_groups(self):
        if self.type == 4:
            if len(self.groups) > 0:
                return
            new_remainder = self.remainder
            while True:
                new_group = new_remainder[:5]
                new_remainder = new_remainder[5:]
                self.groups.append(new_group)
                if new_group[0] == '0':
                    break
            self.remainder = new_remainder
        else:
            raise Exception('Cannot build groups on packet with type ' + str(self.type))

    def literal_value(self):
        if self.type == 0:
            return sum([c.literal_value() for c in self.subpackets])
        elif self.type == 1:
            return math.prod([c.literal_value() for c in self.subpackets])
        elif self.type == 2:
            return min([c.literal_value() for c in self.subpackets])
        elif self.type == 3:
            return max([c.literal_value() for c in self.subpackets])
        elif self.type == 4:
            return bin_to_int(''.join(g[1:] for g in self.groups))
        elif self.type == 5:
            return 1 if self.subpackets[0].literal_value() > self.subpackets[1].literal_value() else 0
        elif self.type == 6:
            return 1 if self.subpackets[0].literal_value() < self.subpackets[1].literal_value() else 0
        elif self.type == 7:
            return 1 if self.subpackets[0].literal_value() == self.subpackets[1].literal_value() else 0

    def version_sum(self):
        return self.version + sum([c.version_sum() for c in self.subpackets])

def print_packets(P: Packet):
    print(P)
    for c in P.subpackets:
        print_packets(c)

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    packet = None
    with open(filename) as f:
        packet = f.readline()
    packet = hex_to_bin(packet)
    packet = Packet(packet)

    print(f"Part 1: {packet.version_sum()} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    print(f"Part 2: {packet.literal_value()} (took {(time.time() - start_time)}s)")