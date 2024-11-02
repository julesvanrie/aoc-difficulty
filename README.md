# AOC Difficulty Assessor

Assess the difficulty of Advent of Code puzzles as they get solved by the first contenders.

This first version compares the time it took for the first 100 contender to get 1 or 2 stars to historical data.

Ideally, the times for the first 100 contenders of the day are know. In that case, the time of the 100th contender is compared to historical data.

If for the 2 stars and/or the 1 stars, there are not yet 100 contenders who solved the puzzle, the time for the last known contender is used and compared to the historical times for that rank.

The quartile gives the quartile of today's times against historical data (with 1 being the fastest quartile and 4 the slowest). If the puzzle got solved faster than any other puzzle ever, the quartile returned by 1. If the puzzle took more time than any puzzle ever, 5 is returned instead of a quartile.

The score is calculated by taking the natural logarithm of today's time and scaling it on historical times:

$$\frac{\ln{t_\textrm{today}} - \ln{t_\textrm{shortest ever}}} {\ln{t_\textrm{longest ever}} - \ln{t_\textrm{shortest ever}}}$$

If nobody solved the puzzle yet, no `score` nor `quartile` is returned, but the text _"Nobody solved it yet"_.

The `final` attribute indicates if this is a score that is no longer going to change (i.e. the time of the 100th contender is known).

```json
{
  "1": {
    "score": 0.36699021464771736,
    "quartile": 2,
    "final": true,
    "level": 1,
    "pos": 100,
    "time": 6.7
  },
  "2": {
    "score": 0.28291680798811053,
    "quartile": 1,
    "final": true,
    "level": 2,
    "pos": 100,
    "time": 7.966666666666667
  },
  "year": 2022,
  "day": 5
}
```
