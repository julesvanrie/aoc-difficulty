from aocdifficulty.history import first_100_history
from aocdifficulty.score import difficulty_score, difficulty_quartile
from aocdifficulty.scraper import get_leaderboard

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
from pytz import timezone

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.state.history = first_100_history()

eric_wastl_tz = timezone('US/Eastern')
today = datetime.now(eric_wastl_tz)

@app.get("/score")
def score(year: int = today.year, day: int = today.day):

    if (day > 25 or
        year < 2015 or
        year > today.year or
        year == today.year and (day > today.day or today.month != 12)
    ):
        return {'error': 'Combination of year and day is not (yet) a valid AOC day'}

    leaders = get_leaderboard(year=year, day=day)

    result = {
        'year': year,
        'day': day,
    }

    for level in [1,2]:
        # Edge case: nobody solved the level yet
        if len(leaders[level-1]) == 0:
            result[str(level)] = {
                'score': "Nobody solved it yet",
                'quartile': "Nobody solved it yet",
                'final': False,
                'level': 2,
                'pos': 0,
                'time': today.hour*60 + today.minute + today.second/60,
            }
            continue

        time = leaders[level-1][-1]
        pos = len(leaders[level-1])

        final = True if pos == 100 else False

        score = difficulty_score(time=time, pos=pos,
                                 history=app.state.history[level-1])
        quartile = difficulty_quartile(time=time, pos=pos,
                                       history=app.state.history[level-1])
        result[str(level)] = {
            'score': score,
            'quartile': quartile,
            'final': final,
            'level': level,
            'pos': pos,
            'time': time,
        }

    return result
