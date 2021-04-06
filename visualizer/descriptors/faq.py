import abc

from visualizer.descriptors import common


class FAQBase():
    def __init__(self, graph):
        self.graph = graph
        self.summary = graph.summarize()

    @abc.abstractmethod
    def is_active(self, roundNum):
        """ Should we display this FAQ? """

    @abc.abstractmethod
    def get_question(self, roundNum):
        """ If (and only if) is_active() is true, what question should we print? """

    @abc.abstractmethod
    def get_answer(self, roundNum):
        """ If (and only if) is_active() is true, what is the answer to that question? """


class WhatHappeningSingleWinner(FAQBase):
    def is_active(self, roundNum):
        return self.summary.numWinners <= 1

    def get_question(self, roundNum):
        return "What is happening?"

    def get_answer(self, roundNum):
        numEliminated = self.summary.numEliminated
        common = "This is a single-winner Ranked Choice Voting election, "\
                 "also known as an Instant Runoff Election. "\
                 "Voters have ranked their candidates in order of preference. "\
                 "Each voter still only had one vote, but if their top pick wasn't going to win, "\
                 "their next choices were taken into account. "
        elim = f"The {numEliminated} lowest-performing candidates were eliminated in succession"
        if self.summary.numWinners == 0:
            win = "."
        else:
            winnerName = self.summary.winnerNames[0]
            win = f" until {winnerName} received more than 50% of the votes."
        return common + elim + win


class WhatHappeningMultiWinner(FAQBase):
    def is_active(self, roundNum):
        return self.summary.numWinners > 1

    def get_question(self, roundNum):
        return "What is happening?"

    def get_answer(self, roundNum):
        numWinners = self.summary.numWinners
        return "This is a multi-winner Ranked Choice Voting election, "\
            "also known as a Single Transferable Vote Election. "\
            f"There were {numWinners} seats to be filled. "\
            "Voters have ranked their candidates in order of preference. "\
            "Each voter still only had one vote. "\
            "The lowest-performing candidates were eliminated until "\
            f"{numWinners} candidates have been elected."


class WhyEliminated(FAQBase):
    def is_active(self, roundNum):
        return len(self.summary.rounds[roundNum].eliminatedNames) > 0

    def get_question(self, roundNum):
        elims = self.summary.rounds[roundNum].eliminatedNames
        if len(elims) == 1:
            return f"Why was {elims[0]} eliminated?"
        else:
            return common.text_to_describe_list_of_names(elims, "Why were {name} eliminated?")

    def get_answer(self, roundNum):
        return "Because they had the fewest votes and could not win the election, "\
               "they were eliminated. "\
               "To ensure people who voted for them still had their voices heard, "\
               "their votes were transferred to their next choice. "\
               "If you are familiar with the concept of runoff elections, "\
               "you can think of these eliminations as holding a runoff "\
               "without going back to the voting booth."


class WhyBatchEliminated(FAQBase):
    def is_active(self, roundNum):
        return len(self.summary.rounds[roundNum].eliminatedNames) > 1

    def get_question(self, roundNum):
        numElims = len(self.summary.rounds[roundNum].eliminatedNames)
        return f"Why were {numElims} candidates eliminated?"

    def get_answer(self, roundNum):
        numElims = len(self.summary.rounds[roundNum].eliminatedNames)
        return "This is known as \"batch elimination.\" "\
               "Since the order of elimination did not affect the outcome, "\
               f"these {numElims} candidates were eliminated in the same round."


class WhySingleWinner(FAQBase):
    def is_active(self, roundNum):
        allWinners = self.summary.winnerNames
        thisRoundWinners = self.summary.rounds[roundNum].winnerNames
        return len(allWinners) == 1 and len(thisRoundWinners) == 1

    def get_question(self, roundNum):
        winner = self.summary.rounds[roundNum].winnerNames[0]
        return f"Why was {winner} elected?"

    def get_answer(self, roundNum):
        winner = self.summary.rounds[roundNum].winnerNames[0]
        return f"Because {winner} received more than 50% of the votes, they were elected."


class WhyMultiWinner(FAQBase):
    def is_active(self, roundNum):
        allWinners = self.summary.winnerNames
        thisRoundWinners = self.summary.rounds[roundNum].winnerNames
        return len(allWinners) > 1 and len(thisRoundWinners) >= 1

    def get_question(self, roundNum):
        winners = self.summary.rounds[roundNum].winnerNames
        wereOrWas = "was" if len(winners) == 1 else "were"
        nameText = common.comma_separated_names_with_and(winners)
        return f"Why {wereOrWas} {nameText} elected?"

    def get_answer(self, roundNum):
        winners = self.summary.rounds[roundNum].winnerNames
        winnerText = common.comma_separated_names_with_and(winners)
        threshold = self.graph.threshold
        supportCount = len(self.summary.winnerNames) + 1
        return f"Because {winnerText} received {threshold} votes, they were elected. "\
               f"The threshold of {threshold} votes was chosen to achieve proportional "\
               f"representation, equal to at least one out of every {supportCount} voters "\
            "supporting this candidate."


class WhyThreshold(FAQBase):
    def is_active(self, roundNum):
        allWinners = self.summary.winnerNames
        thisRoundWinners = self.summary.rounds[roundNum].winnerNames
        return len(allWinners) > 1 and len(thisRoundWinners) >= 1

    def get_question(self, roundNum):
        threshold = self.graph.threshold
        return f"Why did they need {threshold} votes to win?"

    def get_answer(self, roundNum):
        supportCount = len(self.summary.winnerNames) + 1
        return f"In a single-winner election, each elected candidate needs "\
            "one in two voters to support them. Since each voter only gets one vote, "\
            "the same requirement is not possible for this Single Transferrable Vote "\
            f"election. Instead, one in {supportCount} voters must support "\
            "each elected candidate."


class WhySurplusTransfer(FAQBase):
    def __init__(self, graph):
        super(WhySurplusTransfer, self).__init__(graph)
        self._surplus_cache = {}

    def is_active(self, roundNum):
        redistributionData = common.get_redistribution_data(self.graph, roundNum)
        self._surplus_cache[roundNum] = redistributionData

        return len(redistributionData['names']) >= 1

    def get_question(self, roundNum):
        redistributionData = self._surplus_cache[roundNum]
        lostVotes = common.intify_or_aboutify(redistributionData['sum'])
        names = common.comma_separated_names_with_and(redistributionData['names'])
        return f"Why did {names} lose {lostVotes} votes?"

    def get_answer(self, roundNum):
        redistributionData = self._surplus_cache[roundNum]
        names = common.comma_separated_names_with_and(redistributionData['names'])
        threshold = self.graph.threshold
        numWinners = len(self.summary.rounds[roundNum].winnerNames)
        return "A principle of RCV is that no vote should be wasted. "\
            f"Since {names} only needed {threshold} votes, "\
            "any vote beyond that should not be wasted, and is instead redistributed. "\
            f"This also ensures that {numWinners} candidates can reach the "\
            f"{threshold}-vote threshold."


class FAQGenerator():
    generators = (WhatHappeningSingleWinner,
                  WhatHappeningMultiWinner,
                  WhyEliminated,
                  WhyBatchEliminated,
                  WhySingleWinner,
                  WhyMultiWinner,
                  WhyThreshold,
                  WhySurplusTransfer)

    def __init__(self, graph):
        self.graph = graph
        self.generatorObjects = [g(self.graph) for g in self.generators]

    def describe_all_rounds(self):
        return [self.describe_round(r) for r in range(len(self.graph.summarize().rounds))]

    def describe_round(self, roundNum):
        description = []
        for g in self.generatorObjects:
            if g.is_active(roundNum):
                description.append({'question': g.get_question(roundNum),
                                    'answer': g.get_answer(roundNum)})
        return description
