# Changelog

Each round of changes is developed on its own branch. Newest first.

## `feat/player-model-realism`

**The player model against real football.** Every number in `app/core/realism.py` now names its source: REAL (measured),
GAME (EA's FIFA 23 ratings) or DESIGN (our choice). The FIFA 23 figures were counted from Hugging Face `jsulz/FIFA23`,
`male_players (legacy).csv` (FIFA 23 rows, top divisions, 13,682 players; 11,500 first-team players for the ages).
Measured on 3,000 generated players a level and 300 squads, before -> after:

| | before | after | reference |
|---|---|---|---|
| decisions: weak / normal / excellent (mean) | 49 / 48 / 49, sd 23 | 41 / 49 / 56, sd 17 | intelligence, loosely tied to the level (DESIGN) |
| excellent centre-backs' tackling at the 99 ceiling | 27.8% | 0.4% (21% reach 90+) | FIFA 78+: about 83 |
| heading v jumping (centre-backs, correlation) | 0.88 | 0.06 | separate: heading is a skill (FIFA 23) |
| weak foot 4-5 stars, excellent players | 12% | 37% | FIFA 23 78+: 38% |
| squad aged 21 or under / 34+ | 11% / 3% | 18% / 6% | FIFA 23 first teams: 18% / 6% |
| left-footed: LB / LCB / LW / GK | 80 / 40 / 35 / 20% | 86 / 49 / 20 / 12% | StatsBomb / FIFA 23: 85 / 50 / 20 / 13% |
| winger / striker height | 175 / 182 cm | 177 / 183 cm | FIFA 23: 176.7 / 183.3 |
| stamina at 17 against 27 | 5 points lower | 52.7 against 69.5 | FIFA 23: 0.76 |

- **Decisions** are intelligence: a little better at a higher level (42 / 50 / 58), with a wide spread (sd 18, 5-97) - good players with
  poor decisions and ordinary players with fine ones are common, and weak players decide poorly more often. **Aggression** and
  teamwork stay as they were: character, 10-90 at random for every position and level (a 90-aggression striker is fine).
- **Excellent level**: config means above 75 are pulled half way down to 75 (95 -> 85) in `player_config.py`; the spread and the
  role bonuses still take the best to 90+, rarely. (An excellent winger's crossing reaches 90+ in about 40% of players - the
  traditional role adds 8.)
- **Heading** is a skill with its own level by position (FIFA 23); jumping is athletic; height changes neither. **Height** makes a
  player stronger (+1.25 a cm) and slower to get going (acceleration -0.9, speed -0.4), within 12 cm of the position's average
  (FIFA 23: 12 cm apart in a position, strength +12 to +19, acceleration -8 to -14). No more dribbling bonus for short players.
  The height bounds are wider (a winger 156-198 cm, a striker 160-205): a tall winger is rarer (about 3% at 188+), not ruled out;
  heading has a spread of 9, so a winger who heads well is rare, not impossible.
- **Weak foot**: stars by level (FIFA 23 bands); the bonus it gave to finishing, long shots and dribbling (-3 to +5, no source)
  is gone - a match engine handles the weaker foot itself, and the bonus counted it twice.
- **Ages**: the `realistic` profile draws from the real age spread of first-team squads (16-40). **Age curves**: young players are
  faster and weaker than before (pace at 17: 0.94 of the peak, strength 0.75), strength grows to about 29; stamina follows FIFA 23
  by age instead of -5 under 19 and -1.5 a year over 30.
- **Weaker goalkeepers**: reflexes 42 -> 57 (the other skills of the level are 55-60; FIFA 23 keepers under 60: 57).
- `.DS_Store` files are no longer tracked (`.gitignore` already listed them).
- **Tests**: `tests/test_realism.py` (11): decisions loosely by level with poor and fine deciders at every level, no pile-up at 99 and
  some 90+, heading v jumping, a tall / good-heading winger rare but possible, height, weak foot by level, ages, feet by slot,
  stamina by age, aggression random for every position, no weak-foot bonus. 117 tests pass.
