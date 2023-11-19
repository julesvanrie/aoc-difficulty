from aocdifficulty.history import first_100_history
from aocdifficulty.score import difficulty_score, difficulty_quartile
from aocdifficulty.scraper import get_leaderboard

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.state.history_one, app.state.history_two = first_100_history()

today = datetime.today()

@app.get("/score")
def score(year: int = today.year, day: int = today.day):

    if (day > 25 or
        year < 2015 or
        year > today.year or
        year == today.year and (day > today.day or today.month != 12)
    ):
        return {'error': 'Combination of year and day is not (yet) a valid AOC day'}

    leaders_one, leaders_two = get_leaderboard(year=year, day=day)

    level = 2 if len(leaders_two) else 1
    leaders = leaders_two if len(leaders_two) else leaders_one
    time = leaders[-1]
    pos = len(leaders)

    final = True if (level == 2 and pos == 100) else False

    history = app.state.history_one if level == 1 else app.state.history_two

    # import pdb; pdb.set_trace()

    score = difficulty_score(time=time, pos=pos, history=history)
    quartile = difficulty_quartile(time=time, pos=pos, history=history)

    return {
        'year': year,
        'day': day,
        'score': score,
        'quartile': quartile,
        'final': final,
        'based_on': {
            'level': level,
            'pos': pos,
            'time': time,
        }
    }
