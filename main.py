from itertools import combinations
from collections import defaultdict

import utils
from interface import IPrisoner
from players import *    # load all submodules from players

cooperate_score = 3
defect_win_score = 5
defect_lose_score = 0
both_deflect_score = 1
abide_by_scoring_sanity = True

# Configure game rules
# ------------------------

mode = utils.get_user_input('Choose a game mode: {clique, 1v1} (default clique) ',
                            choices=['clique', '1v1'], default='clique')
n_rounds = utils.get_user_input('How many rounds to play for each match? (default 200) ', parse=int, default=200)
assert n_rounds > 1

yes = utils.get_user_input('Configure the scoring rule? (y/n, default no) ', default='n', parse=utils.yes_or_no)
if yes:
    print('''Default scoring rule:
* If both sides cooperate: 3
* If one side deflects:
  - Winner: 5
  - Loser: 0
* If both sides deflect: 1
You can reconfigure the scoring rule but for the game to make sense I think it needs to satisfy a few conditions...:
1. score of both sides deflect x 2 < deflect winner score + deflect loser score < score of both sides cooperate x 2
2. deflect loser score < both sides deflect score < score of both sides cooperate
Scoring rule is also preferably "sane" so that no action in a single round will lead to an insurmountable score for
the whole match. But this is kind of hard to check and depends on how many rounds there are. So we'll just leave it
to you.''')
    abide_by_scoring_sanity = utils.get_user_input('Abide by these rules? (y/n, default yes) ',
                                                   default='y', parse=utils.yes_or_no)
    cooperate_score = utils.get_user_input('Score if both sides cooperate: ', parse=int)
    defect_win_score = utils.get_user_input('If one side deflects, winner scores: ', parse=int)
    defect_lose_score = utils.get_user_input('If one side deflects, loser scores: ', parse=int)
    both_deflect_score = utils.get_user_input('Score if both sides deflect: ', parse=int)

if abide_by_scoring_sanity:
    if not both_deflect_score * 2 < defect_win_score + defect_lose_score < cooperate_score * 2:
        raise ValueError("Scoring rule doesn't meet the first condition above.")
    if not defect_lose_score < both_deflect_score < cooperate_score:
        raise ValueError("Scoring rule doesn't meet the second condition above.")

# Instantiate players
# ------------------------

classes = {kls.__name__: kls for kls in IPrisoner.__subclasses__()}
if len(classes) != len(IPrisoner.__subclasses__()):
    raise ValueError('There are classes with duplicate names!')

# prisoners = list of instantiated classes
if mode == '1v1':
    print('Available classes:')
    print('\n'.join(sorted(classes)))
    prisoners = utils.get_user_input('Pick two classes above, separated using whitespace: ')
    prisoners = [classes[name]() for name in prisoners.split()[:2]]
    assert len(prisoners) == 2
else:
    yes = utils.get_user_input('Spawn one player of each class? (y/n, default yes) ', default='y',
                               parse=utils.yes_or_no)
    if yes:
        prisoners = [classes[name]() for name in sorted(classes)]
    else:
        prisoners = []
        for name in sorted(classes):
            kls = classes[name]
            num = utils.get_user_input(f'How many "{name}" to spawn? (default 1) ', parse=int, default=1)
            for _ in range(num):
                prisoners.append(kls())

# Run game
# ------------------------

scores = defaultdict(int)
for prisoner_a, prisoner_b in combinations(prisoners, 2):
    print(f'[Round] {prisoner_a.__class__.__name__} vs {prisoner_b.__class__.__name__}')
    round_score_a = []
    round_score_b = []
    for i in range(n_rounds):
        # run one round
        action_a = prisoner_a.get_action()
        action_b = prisoner_b.get_action()
        print(f'- {prisoner_a.__class__.__name__}, {prisoner_b.__class__.__name__}: {action_a}, {action_b}')
        if action_a == IPrisoner.COOPERATE and action_b == IPrisoner.COOPERATE:
            score_a, score_b = cooperate_score, cooperate_score
        elif action_a == IPrisoner.COOPERATE and action_b == IPrisoner.DEFECT:
            score_a, score_b = defect_lose_score, defect_win_score
        elif action_a == IPrisoner.DEFECT and action_b == IPrisoner.COOPERATE:
            score_a, score_b = defect_win_score, defect_lose_score
        elif action_a == IPrisoner.DEFECT and action_b == IPrisoner.DEFECT:
            score_a, score_b = both_deflect_score, both_deflect_score
        else:
            raise ValueError()

        prisoner_a.opponent_action_history.append(action_b)
        prisoner_b.opponent_action_history.append(action_a)

        round_score_a.append(score_a)
        round_score_b.append(score_b)
        scores[prisoner_a] += score_a
        scores[prisoner_b] += score_b
    
    # round summary
    print('>', prisoner_a.__class__.__name__, round_score_a, '->', sum(round_score_a))
    print('>', prisoner_b.__class__.__name__, round_score_b, '->', sum(round_score_b))

    prisoner_a.opponent_action_history.clear()
    prisoner_b.opponent_action_history.clear()

# final score
print('-------- Final score --------')
for prisoner in sorted(scores, key=lambda team: scores[team], reverse=True):
    print(prisoner.__class__.__name__, scores[prisoner])
