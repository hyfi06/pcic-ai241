import copy
import sys

from typing import List
from algorithms.models import State
from algorithms.backtracking import backtracking
from elapsed_time.decorators import execution_time
from queens import nQueens


def nQueens_goal(state: nQueens) -> bool:
    return state.is_valid and max([len(domain) for domain in state.domain_per_variable]) == 0 and min(state.variables) != 0


def nQueens_next_states(state: nQueens) -> List[nQueens]:
    list_of_idx: List[int] = state.variable_order()
    new_states: List[nQueens] = list()
    for idx in list_of_idx:
        new_state = copy.deepcopy(state)
        new_state.variables[idx] = new_state.domain_per_variable[idx].pop(0)
        new_state.domain_per_variable[idx] = []
        for i in range(len(state.domain_per_variable)):
            try:
                new_state.domain_per_variable[i].remove(
                    new_state.variables[idx])
            except ValueError:
                pass
            try:
                new_state.domain_per_variable[i].remove(
                    new_state.variables[idx]+abs(i-idx))
            except ValueError:
                pass
            try:
                new_state.domain_per_variable[i].remove(
                    new_state.variables[idx]-abs(i-idx))
            except ValueError:
                pass
        new_states.append(new_state)
    return new_states


@execution_time
def main(n: int):
    initial_state = nQueens(
        [0]*n,
        [list(range(1, n+1)) for i in range(n)]
    )
    solution = backtracking(
        initial_state,
        nQueens_next_states,
        nQueens_goal
    )
    print(solution)


if __name__ == "__main__":
    n: int = int(sys.argv[1])
    main(n)
