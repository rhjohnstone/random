"""
Team A playing Team B in a series of 2k+1 games.
The first team to win k+1 games wins the series.
We want to place a 100 bet on Team A winning the series, with even odds.
But we can only bet on a game-by-game basis.
What betting strategy can we use to have the same result as the original plan?
"""

import operator

def compute_current_net_and_bet(current_score,nets_bets,win,target_bet):
    score_A, score_B = current_score
    score_if_A_wins = (score_A+1,score_B)
    score_if_B_wins = (score_A,score_B+1)
    if (score_A == win-1):
        net_if_B_wins, bet_if_B_wins = nets_bets[score_if_B_wins]
        current_net = 0.5*(target_bet+net_if_B_wins)
        current_bet = 0.5*(target_bet-net_if_B_wins)
    elif (score_B == win-1):
        net_if_A_wins, bet_if_A_wins = nets_bets[score_if_A_wins]
        current_net = 0.5*(net_if_A_wins-target_bet)
        current_bet = 0.5*(net_if_A_wins+target_bet)
    else:
        net_if_A_wins, bet_if_A_wins = nets_bets[score_if_A_wins]
        net_if_B_wins, bet_if_B_wins = nets_bets[score_if_B_wins]
        current_net = 0.5*(net_if_A_wins + net_if_B_wins)
        current_bet = 0.5*(net_if_A_wins - net_if_B_wins)
    return current_net, current_bet

target_bet = 100.

k = 3
N = 2*k+1  # games in series
win = k+1  # games necessary to win series

print "Series of {} games, first to {} wins.".format(N,win)
print "Betting game-by-game to recreate a single bet of {} on Team A winning the series.\n".format(target_bet)

nets_bets = {}
nets_bets[(win-1,win-1)] = (0,100)  # if tied going into final game, the bet is the same as original bet

scores = [(win-1,win-1)]

for current_score in scores:
    for i in xrange(2):
        temp_score = (current_score[0]-(1-i),current_score[1]-i)
        if (temp_score[0]<0) or (temp_score[1]<0):
            continue
        if temp_score not in scores:
            scores.append(temp_score)
            nets_bets[temp_score] = compute_current_net_and_bet(temp_score,nets_bets,win,target_bet)
        else:
            continue
        

nets_bets = sorted(nets_bets.items(), key=operator.itemgetter(0))
print "(Team A, Team B) score, bet:"
for score, net_bet in nets_bets:
    print score, net_bet[1]
