Prisoner Dilemma Simulator
========

Based on [Veritasium's video](https://www.youtube.com/watch?v=mScpHTIi-kM).

The concept is fairly easy to program, so I decided to try it myself.

## How To Use

Run the `main.py` file without any arguments. The program will ask you to configure the game.

Requires Python 3.7+.

You can add as many strategies to the game as you would like. To write a strategy:
1. Inherit `IPrisoner` base class from `interface.py`
2. Override the `get_action(self)` method and return either `self.COOPERATE` or `self.DEFECT` for each round
3. `self.opponent_action_history` is a list containing your opponent's past actions

Currently, there are only 4 very basic strategies:
* `TitForTat`: Starts cooperating, then copies opponent's last action.
* `Meanie`: Always defect. The ultimate bully. Self-interested but unsophisticated.
* `PushOver`: Always cooperate. A complete pushover.
* `Rogue`: Random. Might as well name it Harvey Dent.

## Game Configurations

There are quite a few knobs you can tweak, such as number of rounds and number of players for each strategy (class).

You can also tweak the scoring rule, which is not mentioned in the video. Scoring rule can shape the nature of the game: Is it win-win possible? Is it zero-sum? Or is it negative-sum? I placed a few restrictions to scoring rule to somewhat check if it's win-win possible (which is not perfect), but you can also choose anarchy (LOL) and simulate other scenarios. Presumably, win-win possible games are the ones that're interesting to study in game theory, and the scoring rule in the video is definitely one of this kind. But even if it's win-win possible, scoring rule can still affect how quickly a player can gain advantage or recover from a "betrayal".

Currently there are two "game modes":
* Clique: Every player will interact with every other player.
* 1v1: Pitch two players against each other. This mode is mostly there for debug.

The default game mode is "clique", which is presumably how the tournament ran. But from the video it looks like the research has done some more sophisticated simulation, such as simulating geography.

## Findings

If you run the game with default configuration `TitForTat` actually cannot win...

This is expected, since strategies in `players` are extremely basic and is definitely nowhere close to the tournament.

But simply by playing around with player numbers, I made the following findings:
1. There needs to be at least two `TitForTat`s, or at least one other player with similar strategy, in order for `TitForTat` to come out on top.
2. The presence of one single complete `PushOver` will hand the W to `Meanie`s. `PushOver` is not `TitForTat`'s friend!

If you only have `TitForTat` and `Meanie` in a game, as long as there are two `TitForTat`, they'll always win even if it's "the ultimate bully environment", since `Meanie`s also don't cooperate with each other. You can even add one `Rogue` and `TitForTat`s will still win the game. But when there are more `Rogue`s than `TitForTat`s, `Meanie` gains advantage again. Nevertheless, `Rogue` still does less damage than `PushOver`.

In this light, the ecological simulation mentioned in the video is probably what resembles real-world scenarios the best.
