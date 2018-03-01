class Market(object):
    
    def __init__(self, initial_volume):
        self.volume = initial_volume


class Participant(object):

    def __init__(self, max_volume, participation, market):
        self._participation = participation  # no check on bounds yet
        initial_market_volume = market.volume
        initial_contribution = self.compute_contribution(initial_market_volume)
        self._remaining = max_volume - initial_contribution        
        self._total_contribution = initial_contribution
        self._total_volume_accounted_for = initial_market_volume + initial_contribution
        market.volume += initial_contribution
        
    def compute_contribution(self, volume):
        return (self._participation * volume) / (1. - self._participation)
        
    def update(self, market):
        current_market_volume = market.volume
        new_contribution = self.compute_contribution(current_market_volume - self._total_volume_accounted_for)
        self._total_volume_accounted_for = current_market_volume + new_contribution
        self._total_contribution += new_contribution
        self._remaining -= new_contribution
        if self._remaining <= 0:
            print "No more volume!"
        market.volume += new_contribution

if __name__ == "__main__":
    initial_market_volume = 10000.
    max_participant_volume = 100000000.
    participation = 0.24

    num_participants = 4
    num_iterations = 10000

    market = Market(initial_market_volume)
    participants = [Participant(max_participant_volume, participation, market) for p in xrange(num_participants)]

    for i in xrange(num_iterations-1):
        for p in xrange(num_participants):
            participants[p].update(market)

    for p in xrange(num_participants):
        participants[p].update(market)
        print "{} : {}".format(p, participants[p]._total_contribution)
        
