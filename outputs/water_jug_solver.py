from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass


State = tuple[int, int]


@dataclass(frozen=True)
class Move:
    description: str
    state: State


def possible_moves(state: State, capacities: State) -> list[Move]:
    three, five = state
    cap_three, cap_five = capacities

    moves = [
        Move("Fill the 3-gallon bucket from the stream", (cap_three, five)),
        Move("Fill the 5-gallon bucket from the stream", (three, cap_five)),
        Move("Empty the 3-gallon bucket", (0, five)),
        Move("Empty the 5-gallon bucket", (three, 0)),
    ]

    pour = min(three, cap_five - five)
    moves.append(
        Move("Pour the 3-gallon bucket into the 5-gallon bucket", (three - pour, five + pour))
    )

    pour = min(five, cap_three - three)
    moves.append(
        Move("Pour the 5-gallon bucket into the 3-gallon bucket", (three + pour, five - pour))
    )

    return [move for move in moves if move.state != state]


def solve(
    capacities: State,
    target: int,
    goal: str = "bucket",
    max_steps: int = 14,
) -> list[Move]:
    def reached(state: State) -> bool:
        if goal == "bucket":
            return target in state
        if goal == "total":
            return sum(state) == target
        raise ValueError(f"Unknown goal type: {goal}")

    start: State = (0, 0)
    queue = deque([(start, [])])
    seen = {start}

    while queue:
        state, path = queue.popleft()
        if reached(state):
            return path

        if len(path) >= max_steps:
            continue

        for move in possible_moves(state, capacities):
            if move.state in seen:
                continue
            seen.add(move.state)
            queue.append((move.state, path + [move]))

    raise RuntimeError(f"No solution found in fewer than {max_steps + 1} steps.")


def print_solution(path: list[Move], capacities: State, target: int, goal: str) -> None:
    print(f"Goal: measure {target} gallons using {capacities[0]}- and {capacities[1]}-gallon buckets")
    print(f"Goal mode: {'target amount in one bucket' if goal == 'bucket' else 'target total water'}")
    print(f"Solution length: {len(path)} steps")
    print()
    print("Start: 3-gallon bucket = 0, 5-gallon bucket = 0")

    for step, move in enumerate(path, start=1):
        three, five = move.state
        print(f"{step}. {move.description} -> 3-gallon = {three}, 5-gallon = {five}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Solve the 3-gallon and 5-gallon water bucket puzzle with breadth-first search."
    )
    parser.add_argument("--target", type=int, default=4, help="Amount of water to measure.")
    parser.add_argument(
        "--goal",
        choices=("bucket", "total"),
        default="bucket",
        help="Use 'bucket' for one bucket containing the target, or 'total' for target total water.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=14,
        help="Maximum number of steps allowed. The default enforces 'less than 15 steps'.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    capacities = (3, 5)
    path = solve(capacities, args.target, args.goal, args.max_steps)
    print_solution(path, capacities, args.target, args.goal)


if __name__ == "__main__":
    main()
