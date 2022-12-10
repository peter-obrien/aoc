from __future__ import annotations
import sys
import time
import re

class Beacon:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x},{self.y},{self.z})"
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Beacon):
            return self.x == __o.x and self.y == __o.y and self.z == __o.z
    
    def __hash__(self) -> int:
        result = 1
        result = 31 * result + self.x
        result = 31 * result + self.y
        result = 31 * result + self.z
        return result

    def roll(self) -> Beacon:
        return Beacon(self.x, self.z, -self.y)

    def turn(self) -> Beacon:
        return Beacon(-self.y, self.x, self.z)


class Scanner:
    def __init__(self, id: int, input: list) -> None:
        self.id = id
        self.input = input
        self.beacons: list[Beacon] = []
        self.x = 0
        self.y = 0
        self.z = 0
        for i in input:
            tokens = i.split(',')
            self.beacons.append(Beacon(int(tokens[0]), int(tokens[1]), int(tokens[2])))

    def __str__(self) -> str:
        return "\n".join([str(b) for b in self.beacons])

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id if isinstance(__o, Scanner) else False
    
    def copy(self) -> Scanner:
        result = Scanner(self.id, [])
        for b in self.beacons:
            result.beacons.append(Beacon(b.x, b.y, b.z))
        return result
    
    def transform_location(self, x: int, y: int, z: int):
        self.x += x
        self.y += y
        self.z += z
    
    # https://stackoverflow.com/a/16467849
    def compute_transformations(self) -> list[Scanner]:
        next_scanner = self
        for _ in range(2):
            for _ in range(3):
                next_scanner = next_scanner.roll_beacons()
                yield next_scanner
                for _ in range(3):
                    next_scanner = next_scanner.turn_beacons()
                    yield next_scanner
            next_scanner = next_scanner.roll_beacons().turn_beacons().roll_beacons()
    
    def roll_beacons(self) -> Scanner:
        result = self.copy()
        result.beacons = [b.roll() for b in result.beacons]
        return result

    def turn_beacons(self) -> Scanner:
        result = self.copy()
        result.beacons = [b.turn() for b in result.beacons]
        return result
    
    def max_overlaps(self, other: Scanner):
        # Assume other scanner is facing same direction (reorientation will occur elsewhere)
        # Pick a beacon from other scanner
        # Compute transformation from beacons in scanner 1 to beacon in scanner 2
        # Apply transformation to all beacons from scanner 2
        # Count matches
        result_num_overlaps = 0
        result_transformation: tuple = None
        result_transformed_beacons = []
        for b in self.beacons:
            for e in other.beacons:
                tranformation = (b.x-e.x, b.y-e.y, b.z-e.z)
                our_beacons = set(self.beacons)
                transformed = [Beacon(c.x + tranformation[0], c.y + tranformation[1], c.z + tranformation[2]) for c in other.beacons]
                if len(our_beacons.intersection(transformed)) > result_num_overlaps:
                    result_num_overlaps = len(our_beacons.intersection(transformed))
                    result_transformation = tranformation
                    result_transformed_beacons = transformed
        return (result_num_overlaps, result_transformation, result_transformed_beacons)
    
    def manhatten_distance(self, other: Scanner):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    # List of scanners with unknown orientation
    scanners: list[Scanner] = []
    # List of scanners all with the same orientation
    normalized_scanners: list[Scanner] = []

    with open(filename) as f:
        tokens = re.split(r'--- scanner \d+ ---', f.read())
        counter = 0
        for s in tokens:
            if len(s) > 0:
                scanners.append(Scanner(counter, s.strip().splitlines()))
                counter += 1

    # Let the first scanner be our center for which all others will be reorientated
    normalized_scanners.append(scanners[0])
    total_beacons = set(scanners[0].beacons)
    scanners.remove(scanners[0])
    # Track the transformation of a scanner to the scanner it overlaps with
    transformation_graph = dict()

    while len(scanners) > 0:
        new_scanners = []
        for s in scanners:
            scanner_normalized = False
            for transformed_scanner in s.compute_transformations():
                for ns in normalized_scanners:
                    overlaps = ns.max_overlaps(transformed_scanner)
                    if overlaps[0] >= 12:
                        scanner_normalized = True
                        normalized_scanners.append(transformed_scanner)
                        transformation_graph[transformed_scanner.id] = (ns.id, overlaps)
                        transformed_scanner.transform_location(overlaps[1][0], overlaps[1][1], overlaps[1][2])
                        normalized_beacons = overlaps[2]
                        if ns.id != 0:
                            # Need to normalize this scanner's beacons to scanner 0
                            next_scanner_id = ns.id
                            while True:
                                transform_rules = transformation_graph[next_scanner_id][1][1]
                                transformed_scanner.transform_location(transform_rules[0], transform_rules[1], transform_rules[2])
                                normalized_beacons = [Beacon(b.x + transform_rules[0], b.y + transform_rules[1], b.z + transform_rules[2]) for b in normalized_beacons]
                                next_scanner_id = transformation_graph[next_scanner_id][0]
                                if next_scanner_id == 0:
                                    break
                        total_beacons.update(normalized_beacons)
                        print(f'Normalized scanner {transformed_scanner.id} to {ns.id}. We now have {len(normalized_scanners)} normalized scanners.')
                        break
                if scanner_normalized:
                    break
            if not scanner_normalized:
                new_scanners.append(s)
        scanners = new_scanners
    assert len(scanners) == 0

    print(f"Part 1: {len(total_beacons)} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    largest_distance = 0
    for s in normalized_scanners:
        for os in normalized_scanners:
            if s != os:
                largest_distance = max(largest_distance, s.manhatten_distance(os))
    print(f"Part 2: {largest_distance} (took {(time.time() - start_time)}s)")
