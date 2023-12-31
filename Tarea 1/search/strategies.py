from typing import Callable, TypeAlias
from search.algorithms import Strategy
from pqueue.models import PQueue
from graph.models import LabeledGraph

Heuristic: TypeAlias = Callable[[str], int]


def dfs_strategy(
    node: str,
    parent_priority: int,
    border: PQueue[tuple[str, int]],
    new_border: list[tuple[str, int]],
    tree: LabeledGraph,
) -> None:
    for item in new_border:
        border.push((parent_priority - 1, item))


def bfs_strategy(
    node: str,
    parent_priority: int,
    border: PQueue[tuple[str, int]],
    new_border: list[tuple[str, int]],
    tree: LabeledGraph,
) -> None:
    for item in new_border:
        border.push((parent_priority + 1, item))


def iterative_strategy(
    initial_node: str,
    graph: LabeledGraph
) -> Strategy:
    depth: int = 0

    def strategy(
        node: str,
        parent_priority: int,
        border: PQueue[tuple[str, int]],
        new_border: list[tuple[str, int]],
        tree: LabeledGraph,
    ) -> None:
        nonlocal depth
        nonlocal graph
        nonlocal initial_node

        if depth < parent_priority:
            for item in new_border:
                border.push((parent_priority - 1, item))

        if len(border) == 0 and len(
            graph.get_nodes().difference(tree.get_nodes())
        ):
            depth -= 1
            border.push((0, (initial_node, 0)))
            tree.clear()
            tree.add_node(initial_node, [])
    return strategy


def ucs_strategy(
    node: str,
    parent_priority: int,
    border: PQueue[tuple[str, int]],
    new_border: list[tuple[str, int]],
    tree: LabeledGraph,
) -> None:
    for item in new_border:
        cost = parent_priority + item[1]
        border.push((cost, item))


def greedy_strategy(heuristic: Heuristic) -> Strategy:
    def strategy(
        node: str,
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
        node: str,
        parent_priority: int,
        border: PQueue[tuple[str, int]],
        new_border: list[tuple[str, int]],
        tree: LabeledGraph,
    ) -> None:
        for item in new_border:
            cost = (parent_priority - heuristic(node) if parent_priority else 0) + \
                item[1] + heuristic(item[0])
            border.push((
                cost,
                item
            ))

    return strategy
