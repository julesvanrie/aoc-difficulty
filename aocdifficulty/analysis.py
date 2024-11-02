def get_evo(year: int = 2021, level: int = 2, transform: str ='identical') -> pd.DataFrame:
    """Return a dataframe with data for a given year, level,
    and a transformation applied

    Parameters
    ----------
    year : int
        Year for which to get the evolution
    level : int
        Level for which to show the evolution. One of [1, 2]
    transform : string
        Transformation to apply to the times. One of:
        - 'identical': no transformation
        - 'log': logarithmic transformation

    Returns
    -------
    pd.DataFrame
        Dataframe with for every day of the given year, for the given level,
        - 'To 100':  Time it took for the 100th contendor to solve
        - 'To 50':   Time it took for the  50th contendor to solve
        - 'Avg 100': Average time it took for the first 100 contendonrs to solve
    """
    funcs = {
        'identical': lambda x: x,
        'log': np.log
    }

    level_to_100 = [history[str(year)][str(d)][str(level)][99]
                    for d in range(1,26)]
    level_to_50 = [history[str(year)][str(d)][str(level)][49]
                   for d in range(1,26)]
    level_avg_100 = [sum(history[str(year)][str(d)][str(level)][:100])/100
                     for d in range(1,26)]

    evo_level = pd.DataFrame({
                    'To 100': level_to_100,
                    'To 50': level_to_50,
                    'Avg 100': level_avg_100
                    },
                    index=range(1,26)) / 60

    return evo_level.applymap(funcs[transform])
