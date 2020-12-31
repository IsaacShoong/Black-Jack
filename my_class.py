import random
DEBUG = False


class Boundary:
    def __init__(self, x, y, w, h, modes, buttonGap, currentMode, horizontal=True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.modes = modes
        self.buttonGap = buttonGap
        self.currentMode = currentMode
        self.horizontal = horizontal
        self.numButtons = len(self.modes)
        self.allBoundaries = []

    def clickButtons(self):
        for i in range(self.numButtons):
            upperLeft = [self.x, self.y]
            lowerRight = [self.x + self.w, self.y + self.h]
            clickBoundary = [upperLeft, lowerRight]
            self.allBoundaries.append(clickBoundary)
            if self.horizontal:
                self.x += self.w + self.buttonGap
            else:
                self.y += self.h + self.buttonGap
        if DEBUG:
            print(self.allBoundaries)

        for j in range(self.numButtons):
            validXRange = self.allBoundaries[j][0][0] <= mouseX <= self.allBoundaries[j][1][0]
            validYRange = self.allBoundaries[j][0][1] <= mouseY <= self.allBoundaries[j][1][1]
            validLocation = validXRange and validYRange
            if validLocation:
                if DEBUG:
                    print(self.modes[j])
                break
        if not validLocation:
            return (self.currentMode)

        return (self.modes[j])


class UserInterface:
    def __init__(self, x, y, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def displayImage(self, imageName):
        image(imageName, self.x, self.y, self.w, self.h)

    def hoverMenuBar(self, imageName):
        if self.x <= mouseX <= self.x + self.w and self.y <= mouseY <= self.y + self.h:
            image(imageName, self.x, self.y, self.w, self.h)

    def whiteBorder(self, imageName):
        WHITE = 255
        image(imageName, self.x, self.y, self.w, self.h)
        if self.x <= mouseX <= self.x + self.w and self.y <= mouseY <= self.y + self.h:
            fill(WHITE)
            rect(self.x-5, self.y-5, self.w+10, self.h+10)
            image(imageName, self.x, self.y, self.w, self.h)

    def enlargeImage(self, imageName):
        image(imageName, self.x, self.y, self.w, self.h)
        if self.x <= mouseX <= self.x + self.w and self.y <= mouseY <= self.y + self.h:
            image(imageName, self.x-5, self.y-5, self.w+10, self.h+10)

    def displayFont(self, fontName, colour, name):
        textAlign(CENTER)
        textFont(fontName)
        fill(colour)
        text(name, self.x, self.y)


class Deck:
    def __init__(self):
        self.deck = [[True] * 4 for i in range(13)]

    def getCardAndValue(self):
        keepGoing = True
        while keepGoing:
            c = random.randint(0, 12)
            s = random.randint(0, 3)
            if self.deck[c][s] == True:
                self.deck[c][s] = False
                keepGoing = False
        return (c, s)


class Player:
    def __init__(self):
        self.player_hand = []
        self.player_hand2 = []
        self.total_money = 1000
        self.total_bet = 0
        self.player_bet = True
        self.play_second_hand = False
        self.playerHigh = 1000
        self.firstName = ""
        self.lastName = ""
        self.studNum = ""
        self.date = str(month()) + "/" + str(day())
        self.fullName = self.firstName + self.lastName

    def dealCard(self, card):
        self.player_hand.append(card)
        return (self.player_hand)

    def dealSecondHandCards(self, card):
        self.player_hand2.append(card)
        return (self.player_hand2)

    def hit(self, card):
        self.player_hand.append(card)
        return (self.player_hand)

    def total(self):
        total = 0
        cardValues = []
        for card in self.player_hand:
            if card[0] >= 10:
                cardValues.append(10)
            else:
                cardValues.append(card[0] + 1)

        for card in cardValues:
            if card == 1:
                if sum(cardValues) > 11:
                    total += 1
                else:
                    total += 11
                    change = cardValues.index(card)
                    cardValues[change] = 11
            else:
                total += card

        if sum(cardValues) > 21:
            if 11 in cardValues:
                change = cardValues.index(11)
                cardValues[change] = 1

        return (total)

    def makeUserBet(self, chosenBet):
        if self.total_bet > 0:
            if chosenBet == "deal":
                self.player_bet = False
                return (self.total_bet)

        if self.total_money > 0:
            if chosenBet == "All":
                self.total_bet += self.total_money
                self.total_money = 0
                return (self.total_bet)

            if chosenBet != "deal":
                if self.total_money - chosenBet >= 0:
                    self.total_money -= chosenBet
                    self.total_bet += chosenBet

            return (self.total_bet)

    def getPlayerScore(self, score):
        if score > self.playerHigh:
            self.playerHigh = score
        return (self.playerHigh)

    def getFirstName(self, whichKey, acceptedChars, delete):
        if (whichKey != "") and (whichKey.upper() in acceptedChars):
            self.firstName = self.firstName + whichKey.upper()
            print(self.firstName)
            #whichKey = ""
        if (whichKey != "") and (whichKey == delete):
            self.firstName = self.firstName[:len(self.firstName) - 1]
            #whichKey = ""
            print(self.firstName)
        whichKey = ""
        return (self.firstName)

    def getLastName(self, whichKey, acceptedChars, delete):
        if (whichKey != "") and (whichKey.upper() in acceptedChars):
            self.lastName = self.lastName + whichKey.upper()
            print(self.lastName)
            #whichKey = ""
        if (whichKey != "") and (whichKey == delete):
            self.lastName = self.lastName[:len(self.lastName) - 1]
            #whichKey = ""
            print(self.lastName)
        whichKey = ""
        return (self.lastName)

    def getStudNum(self, whichKey, acceptedNums, delete):
        if (whichKey != "") and (whichKey in acceptedNums):
            self.studNum = self.studNum + whichKey
            print(self.studNum)
            #whichKey = " "
        if (whichKey != "") and (whichKey == delete):
            self.studNum = self.studNum[:len(self.studNum) - 1]
            #whichKey = ""
            print(self.studNum)
        whichKey = ""
        return (self.studNum)
