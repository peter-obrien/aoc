import sys
import time
import math
from types import FunctionType

explode_tests: dict = {
    '[[[[[9,8],1],2],3],4]': '[[[[0,9],2],3],4]',
    '[7,[6,[5,[4,[3,2]]]]]': '[7,[6,[5,[7,0]]]]',
    '[[6,[5,[4,[3,2]]]],1]': '[[6,[5,[7,0]]],3]',
    '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]': '[[3,[2,[8,0]]],[9,[5,[7,0]]]]',
    '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]': '[[3,[2,[8,0]]],[9,[5,[7,0]]]]',
    '[[[[[1,1],[2,2]],[3,3]],[4,4]],[5,5]]': '[[[[3,0],[5,3]],[4,4]],[5,5]]'
}

split_tests: dict = {
    '[10,11]': '[[5,5],[5,6]]',
    '[[[[0,7],4],[15,1]],[1,1]]': '[[[[0,7],4],[[7,8],1]],[1,1]]'
}

combined_tests: dict = {
    '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]': '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]',
    '[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]': '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
    '[[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]]': '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]',
    '[[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]]': '[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]',
    '[[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]': '[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]',
    '[[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],[[2,[2,2]],[8,[8,1]]]]': '[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]',
    '[[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],[2,9]]': '[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]',
    '[[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],[1,[[[9,3],9],[[9,0],[0,7]]]]]': '[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]',
    '[[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],[[[5,[7,4]],7],1]]': '[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]',
    '[[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],[[[[4,2],2],6],[8,7]]]': '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
}

magnitude_tests: dict = {
    '[9,1]': 29,
    '[1,9]': 21,
    '[[9,1],[1,9]]': 129,
    '[[1,2],[[3,4],5]]': 143,
    '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]': 1384,
    '[[[[1,1],[2,2]],[3,3]],[4,4]]': 445,
    '[[[[3,0],[5,3]],[4,4]],[5,5]]': 791,
    '[[[[5,0],[7,4]],[5,5]],[6,6]]': 1137,
    '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]': 3488,
}

class SnailfishNumber:

    def __init__(self, input: str) -> None:
        self.input = input
        self.left = None
        self.right = None
        self.parse()

    def __str__(self) -> str:
        return f"[{str(self.left)},{str(self.right)}]"

    def parse(self):
        contents = self.input[1:len(self.input)-1]
        # find left
        if contents.startswith('['):
            # find the comma that separates left and right
            index = 0
            num_open = 0
            num_close = 0
            while True:
                num_open += 1 if contents[index] == '[' else 0
                num_close += 1 if contents[index] == ']' else 0
                index += 1
                if num_open == num_close:
                    break
            self.left = SnailfishNumber(contents[:index])
            contents = contents[index+1:]
        else:
            self.left = int(contents[:contents.find(',')])
            contents = contents[contents.find(',')+1:]
        self.right = int(contents) if contents.isdigit() else SnailfishNumber(contents)

    def reduce(self):
        while self.explode() or self.split():
            pass
        return self

    def explode(self, depth: int = 0):
        if depth == 4:
            # [instruction_code, zeroed_out, added_left, left_val, added_right, right_val]
            return ['e', False, False, self.left, False, self.right]
        instruction = self.left.explode(depth + 1) if isinstance(self.left, SnailfishNumber) else None
        if instruction:
            # Order is important so that we don't override the zero that replaced the exploded number
            if instruction[1] and not instruction[2] and isinstance(self.left, int):
                self.left += instruction[3]
                instruction[2] = True
            if not instruction[1]:
                self.left = 0
                instruction[1] = True
            if not instruction[4]:
                if isinstance(self.right, int):
                    self.right += instruction[5]
                    instruction[4] = True
                else:
                    self.right.apply_to_leftmost(lambda x: x + instruction[5])
                    instruction[4] = True
            return instruction
        instruction = self.right.explode(depth + 1) if isinstance(self.right, SnailfishNumber) else None
        if instruction:
            if instruction[1] and not instruction[4] and isinstance(self.right, int):
                self.right += instruction[5]
                instruction[4] = True
            if not instruction[1]:
                self.right = 0
                instruction[1] = True
            if not instruction[2]:
                if isinstance(self.left, int):
                    self.left += instruction[3]
                    instruction[2] = True
                else:
                    self.left.apply_to_rightmost(lambda x: x + instruction[3])
                    instruction[2] = True
            return instruction
        return instruction

    def split(self):
        if isinstance(self.left, int) and self.left > 9:
            self.left = SnailfishNumber(f"[{math.floor(self.left/2)},{math.ceil(self.left/2)}]")
            return True
        if isinstance(self.left, SnailfishNumber):
            if self.left.split():
                return True
        if isinstance(self.right, int) and self.right > 9:
            self.right = SnailfishNumber(f"[{math.floor(self.right/2)},{math.ceil(self.right/2)}]")
            return True
        else:
            return isinstance(self.right, SnailfishNumber) and self.right.split()

    def apply_to_leftmost(self, f: FunctionType):
        if isinstance(self.left, SnailfishNumber):
            self.left.apply_to_leftmost(f)
        else:
            self.left = f(self.left)

    def apply_to_rightmost(self, f: FunctionType):
        if isinstance(self.right, SnailfishNumber):
            self.right.apply_to_rightmost(f)
        else:
            self.right = f(self.right)

    def magnitude(self):
        left_magnitude = 3 * (self.left if isinstance(self.left, int) else self.left.magnitude())
        right_magnitude = 2 * (self.right if isinstance(self.right, int) else self.right.magnitude())
        return left_magnitude + right_magnitude


if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    if '-t' in sys.argv:
        for test in explode_tests:
            num = SnailfishNumber(test)
            assert test == str(num)
            num.reduce()
            if explode_tests[test] != str(num):
                raise Exception(f'Explode test failed for input {test}:\nExpected: {explode_tests[test]}\n     Got: {str(num)}')
        print('Completed explode tests!')

        for test in split_tests:
            num = SnailfishNumber(test)
            num.reduce()
            if split_tests[test] != str(num):
                raise Exception(f'Split test failed for input {test}:\nExpected: {split_tests[test]}\n     Got: {str(num)}')
        print('Completed split tests!')

        for test in combined_tests:
            num = SnailfishNumber(test)
            num.reduce()
            if combined_tests[test] != str(num):
                raise Exception(f'Combined test failed for input {test}:\nExpected: {combined_tests[test]}\n     Got: {str(num)}')
        print('Completed combined tests!')

        for test in magnitude_tests:
            num = SnailfishNumber(test)
            m = num.magnitude()
            if magnitude_tests[test] != m:
                raise Exception(f'Magnitude test failed for input {test}:\nExpected: {magnitude_tests[test]}\n     Got: {m}')
        print('Completed magnitude tests!')
    else:
        with open(filename) as f:
            lines = f.read().splitlines()

        prior = None
        for line in lines:
            current = SnailfishNumber(line)
            if prior is not None:
                current = SnailfishNumber(f"[{str(prior)},{str(current)}]")
                current.reduce()
            prior = current
        result = prior.magnitude()
        print(f"Part 1: {result} (took {(time.time() - start_time)}s)")

        start_time = time.time()
        result = 0
        for i in range(len(lines)):
            for j in range(len(lines)):
                if i == j:
                    continue
                else:
                    result = max(result, SnailfishNumber(f"[{lines[i]},{lines[j]}]").reduce().magnitude())
        print(f"Part 2: {result} (took {(time.time() - start_time)}s)")