from typing import Callable, TypeAlias
from search.main import Strategy
from pqueue.models import PQueue
from graph.models import LabeledGraph

Heuristic: TypeAlias = Callable[[str], int]


def dfs_strategy(
    node_priority: int,
    border: PQueue[tuple[str, int]],
    new_border: list[tuple[str, int]],
    tree: LabeledGraph,
) -> None:
    for item in new_border:
        border.push((node_priority - 1, item))


def bfs_strategy(
    parent_priority: int,
    border: PQueue[tuple[str, int]],
    new_border: list[tuple[str, int]],
    tree: LabeledGraph,
) -> None:
    for item in new_border:
        border.push((parent_priority + 1, item))


def iterative_strategy(initial_node: str) -> Strategy:
    depth: int = 0

    def strategy(
        parent_priority: int,
        border: PQueue[tuple[str, int]],
        new_border: list[tuple[str, int]],
        tree: LabeledGraph,
    ) -> None:
        nonlocal depth
        nonlocal initial_node
        if depth < parent_priority:
            for item in new_border:
                border.push((parent_priority - 1, item))
        elif len(border) == 0:
            depth -= 1
            border.push((0, (initial_node, 0)))
            tree.clear()
            tree.add_node(initial_node, [])
    return strategy


def ucs_strategy(
    parent_priority: int,
    border: PQueue[tuple[str, int]],
    new_border: list[tuple[str, int]],
    tree: LabeledGraph,
) -> None:
    for item in new_border:
        cost: int = tree.get_border(item[0])[0][1] if len(
            tree.get_border(item[0])) else 0
        border.push((cost, item))


def greedy_strategy(heuristic: Heuristic) -> Strategy:
    def strategy(
        parent_priority: int,
        border: PQueue[tuple[str, int]],
        new_border: list[tuple[str, int]],
        tree: LabeledGraph,
    ) -> None:
        for item in new_border:
            border.push((
                heuristic(item[0]),
                item
            ))
    return strategy


def a_star_strategy(heuristic: Heuristic) -> Strategy:
    def strategy(
        parent_priority: int,
        border: PQueue[tuple[str, int]],
        new_border: list[tuple[str, int]],
        tree: LabeledGraph,
    ) -> None:
        for item in new_border:
            border.push((
                item[1] + heuristic(item[0]),
                item
            ))
    return strategy
