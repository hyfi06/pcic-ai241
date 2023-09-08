from typing import TypeVar, Callable, Generic, List, Optional, Set


T = TypeVar('T')


class State(Generic[T]):
    def __init__(self, values: List[T], domain_per_variable: List[List[T]]) -> None:
        self.variables: List[T] = values
        self.domain_per_variable: List[List[T]] = domain_per_variable

    def __str__(self) -> str:
        return self.variables.__str__()


U = TypeVar('U', bound=State)


def taboo_search(
    initial_state: U,
    height: Callable[[U], int | float],
    neighborhood: Callable[[U], List[U]],
    goal_test: Callable[[U], bool],
    time: Callable[[], bool],
    fist_solution: Optional[bool] = True
):
    taboo_list: Set[str] = set()
    solutions: Set[str] = set()
    state: U = initial_state
    max_height = height(state)
    while time():
        taboo_list.add(str(state))
        # print(f"{height(state)} - {state}")
        if goal_test(state) and max_height < height(state):
            max_height = height(state)
            solutions.add(str(state))
            if fist_solution:
                break
        else:
            neighborhood_of_state = [
                new_state
                for new_state in neighborhood(state)
                if str(new_state) not in taboo_list
            ]

            if len(neighborhood_of_state) == 0:
                break

            new_state = neighborhood_of_state[0]
            for s in neighborhood_of_state:
                if height(s) > height(new_state):
                    new_state = s
            state = new_state

    return solutions
