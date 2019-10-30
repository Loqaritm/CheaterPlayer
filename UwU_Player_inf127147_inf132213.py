### inf127147
### inf132213

class UwU_Player(Player):
    
    ### initialise possibilities for other cards
    def startGame(self, cards):
        super().startGame(cards)
        self.otherPlayerNumOfCards = 8
        self.numCardsOnTable = 0
        
        self.sureCardsOnTable = []
    
        self.cards.sort(key = lambda x : x[0])
        
    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        super().getCheckFeedback(checked, iChecked, iDrewCards, revealedCard, noTakenCards, log)
        if (checked is True):
            self.otherPlayerNumOfCards = self.otherPlayerNumOfCards + noTakenCards
            if (noTakenCards == 3): self.sureCardsOnTable = self.sureCardsOnTable[:-2]
            if (noTakenCards < 3): self.sureCardsOnTable = self.sureCardsOnTable[:-1]
        
    
    def shouldLie(self):
        if (len(self.cards) == 1): return False

        difference = len(self.cards) - self.otherPlayerNumOfCards
        if (difference < 0):
            return False
        
        # Always lie if there is no other choice
        return True

        # pTrue = min(difference * 0.7, 1.0)
        # return np.random.choice([True, False], p=[pTrue, 1.0-pTrue])
            
    
    def putCard(self, declared_card):
        if declared_card is None:
            self.sureCardsOnTable.append(self.cards[0])
            self.numCardsOnTable = self.numCardsOnTable + 1
            # return smallest card in hand
            return self.cards[0], self.cards[0]
        
        # remember to always sort - this is important if u draw cards later
        self.cards.sort(key = lambda x : x[0])

        card = [x for x in self.cards if x[0] >= declared_card[0]]
        # no actual true card that can be put
        if (len(card) == 0):
            if (not self.shouldLie()):
                return 'draw'
            
            self.sureCardsOnTable.append(card)
            self.numCardsOnTable = self.numCardsOnTable + 1

            return self.cards[0], (declared_card[0], np.random.rand(0,4))
        
        # take first that fits the criteria above
        card = card[0]
        self.sureCardsOnTable.append(card)
        
        self.numCardsOnTable = self.numCardsOnTable + 1
        return card, card
    
    def checkCard(self, opponent_declaration):
        if (opponent_declaration == 'draw'):
            potentialCardsToDraw = min(self.numCardsOnTable, 3)
            
            self.otherPlayerNumOfCards = self.otherPlayerNumOfCards + potentialCardsToDraw 
            self.numCardsOnTable = self.numCardsOnTable - potentialCardsToDraw
            if (len(self.sureCardsOnTable) < 2):
                self.sureCardsOnTable = []
            else: self.sureCardsOnTable = self.sureCardsOnTable[:-2]
        else:
            self.numCardsOnTable = self.numCardsOnTable + 1
        
        
        if (opponent_declaration is not None and opponent_declaration is  not 'draw'):
            self.otherPlayerNumOfCards = self.otherPlayerNumOfCards - 1
        # always check on last card
        if (self.otherPlayerNumOfCards == 0): return True
        
        if opponent_declaration in self.cards: return True
        if opponent_declaration in self.sureCardsOnTable: return True
        return False