import numpy as np
import pandas as pd

from aocdifficulty.history import first_100_history


def difficulty_quartile(time: float, pos: int = 100, history: pd.DataFrame = None) -> int:
    """Calculates the difficulty quartile
    Compares the time it took the n-th contender
    to historical data.

    Parameters
    ----------
    time : float
        Time it took the pos-th contender
    pos : int (default: 100)
        Position of the contender to evaluate
    history : pd.DataFrame (default: None)
        History against which to check
        If None, loads history for level 2
    Returns
    -------
    int (0 to 5)
        Quartile: from 0 (faster than ever) to 5 (slower than ever)
    """
    if history is None:
        _, history = first_100_history()

    if time > history[pos].quantile(1.00):
        difficulty = 5
    if time < history[pos].quantile(1.00):
        difficulty = 4
    if time < history[pos].quantile(0.75):
        difficulty = 3
    if time < history[pos].quantile(0.5):
        difficulty = 2
    if time < history[pos].quantile(0.25):
        difficulty = 1
    if time < history[pos].quantile(0.00):
        difficulty = 0

    return difficulty

def difficulty_score(time: float, pos: int = 100, history: pd.DataFrame = None) -> float:
    """Calculates a difficulty score
    Compares the log of the time it took the n-th contender
    to historical data.

    Parameters
    ----------
    time : float
        Time it took the n-th contender
    pos : int (default: 100)
        Position of the contender to evaluate
    history : pd.DataFrame (default: None)
        History against which to check
        If None, loads history for level 2

    Returns
    -------
    float
        Score: log compared to historical data
        Goes from 0 (faster than ever) to 1 (slower than ever)
    """
    if history is None:
        _, history = first_100_history()

    log_min = np.log(history[pos].min())
    log_spread = np.log(history[pos].max()) - log_min
    score = (np.log(time) - log_min) / log_spread

    return min(max(0, score), 1)


# def get_day_score():
#     """Retrieves the time it took for the contendors for a give day

#     """


if __name__ == "__main__":
    _, history = first_100_history()
    print(difficulty_quartile(time=5, pos=100, history=history))
    print(difficulty_score(time=5, pos=100, history=history))
