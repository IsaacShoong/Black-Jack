from my_class import Boundary, UserInterface, Deck, Player
import pickle
DEBUG = True
SCREEN_W = 1000
SCREEN_H = 667

#Load image names from a file into a list
def loadImageNames(fileName):
    try:
        file = open(fileName)
        text = file.readline()
        file.close()
        return (text.strip().split(','))
    except IOError:
        print(fileName + " does not exist.")


def loadImages(imageListNames):
    imageList = []
    imageList = [loadImage(i.lstrip()) for i in imageListNames]
    return (imageList)

#Load variable values from a file
def loadIntegerValues(fileName, isInt=True):
    fileValues = []
    try:
        readFile = open(fileName, "r")
        for line in readFile.readlines():
            line = line.strip().split(",")
            if isInt:
                line = [int(value) for value in line]
            fileValues.append(line)
        return (fileValues)

    except IOError:
        print(fileName + " does not exist.")


def dealPlayerDeck():
    global player1, dealer
    for i in range(2):
        player1.dealCard(deckOfCards.getCardAndValue())
        dealer.dealCard(deckOfCards.getCardAndValue())


def playGame(chosenMove):
    global player1, dealer, player1Turn

    if gameOver:
        player1Turn = False

    if player1Turn:
        if chosenMove == "hit":
            player1.hit(deckOfCards.getCardAndValue())

        if player1.total_money - player1.total_bet >= 0:
            if chosenMove == "double":
                player1.total_money -= player1.total_bet
                player1.total_bet += player1.total_bet
                player1.hit(deckOfCards.getCardAndValue())
                player1Turn = False
                while dealer.total() < 17:
                    dealer.hit(deckOfCards.getCardAndValue())

            if player1.player_hand[0][0] == player1.player_hand[1][0]:
                if chosenMove == "split":
                    player1.total_money -= player1.total_bet
                    player1.player_hand2.append(player1.player_hand[1])
                    player1.player_hand.pop(1)
                    player1.dealCard(deckOfCards.getCardAndValue())
                    player1.dealSecondHandCards(deckOfCards.getCardAndValue())

        if chosenMove == "stand":
            player1Turn = False
            while dealer.total() < 17:
                dealer.hit(deckOfCards.getCardAndValue())
    return

# Calculate score of player and dealer and determine if somebody won
def score(playerHand, dealerHand):
    global gameOver, player1Turn
    if playerHand == 21 and dealerHand == 21:
        gameOver = True
        player1.total_money += player1.total_bet

    if len(player1.player_hand) >= 5:
        gameOver = True
        if len(player1.player_hand) == 5:
            if player1.total() <= 21:
                player1.total_money += player1.total_bet * 2
                if len(player1.player_hand2) == 0:
                    player1.total_money += player1.total_bet * 2
                    player1.total_bet = 0
                    player1.getPlayerScore(player1.total_money)

    if dealerHand > 21 or playerHand == 21:
        gameOver = True
        player1.total_money += player1.total_bet * 2
        if len(player1.player_hand2) == 0:
            player1.total_bet = 0
            player1.getPlayerScore(player1.total_money)

    if playerHand > 21 or dealerHand == 21:
        gameOver = True
        if len(player1.player_hand2) == 0:
            player1.total_bet = 0

    if playerHand < 21 and dealerHand < 21:
        if not player1Turn:
            gameOver = True
            if dealerHand >= 17 and playerHand > dealerHand:
                player1.total_money += player1.total_bet * 2
                if len(player1.player_hand2) == 0:
                    player1.total_bet = 0
                    player1.getPlayerScore(player1.total_money)

            elif dealerHand >= 17 and dealerHand > playerHand:
                if len(player1.player_hand2) == 0:
                    player1.total_bet = 0

            elif dealerHand == playerHand:
                player1.total_money += player1.total_bet

            else:
                pass

    return (gameOver)


def displayWhoWon(playerTotal, dealerTotal):
    global imageValues, textColour
    textX = imageValues[21][0]
    textY = imageValues[21][1]

    if playerTotal == 21 and dealerTotal == 21:
        UserInterface(textX, textY).displayFont(gameFont, textColour, "Push")
        return

    if playerTotal == 21:
        if len(player1.player_hand) == 2:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Blackjack! Player Wins!")
        else:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Player Wins!")
        return

    if dealerTotal == 21:
        if len(dealer.player_hand) == 2:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Dealer Blackjack!")
        else:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Dealer Wins!")

    if len(player1.player_hand) == 5:
        if player1.total() <= 21:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Player Wins!")
        else:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Player Bust!")
        return

    if playerTotal > 21:
        UserInterface(textX, textY).displayFont(
            gameFont, textColour, "Player Bust {0}".format(player1.total()))
        return

    if dealerTotal > 21:
        UserInterface(textX, textY).displayFont(
            gameFont, textColour, "Dealer Bust {0}".format(dealer.total()))
        return

    if playerTotal < 21 and dealerTotal < 21:
        if dealerTotal >= 17 and playerTotal > dealerTotal:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Player Wins!")
            return
        elif dealerTotal >= 17 and dealerTotal > playerTotal:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Dealer Wins!")
            return
        elif dealerTotal == playerTotal:
            UserInterface(textX, textY).displayFont(
                gameFont, textColour, "Push")
            return
        else:
            pass
    return

# Set mode based off where the user clicks
def setMode():
    global mode, gameStarted, imageList, buttonBoundaries, boundaryValues, deckOfCards, player1, playerBoundaries, gameOver, stringValues, nameMode
    if DEBUG:
        print("===========================", mode)
    if mode == "home":
        buttonBoundaries = Boundary(boundaryValues[0][0], boundaryValues[0][1], boundaryValues[0]
                                    [2], boundaryValues[0][3], stringValues[7], boundaryValues[0][4], "home", False)
    if mode == "name":
        buttonBoundaries = Boundary(boundaryValues[6][0],boundaryValues[6][1],boundaryValues[6][2],boundaryValues[6][3], stringValues[15],boundaryValues[6][4], "name", False)
        nameMode = buttonBoundaries.clickButtons()
        return
    if mode == "play":
        gameStarted = True

        buttonBoundaries = Boundary(boundaryValues[1][0], boundaryValues[1][1], boundaryValues[1]
                                    [2], boundaryValues[1][3], stringValues[8], boundaryValues[1][4], "play")
        playerMoves = Boundary(boundaryValues[4][0], boundaryValues[4][1], boundaryValues[4]
                               [2], boundaryValues[4][3], stringValues[9], boundaryValues[4][4], "play")
        moneyChoices = Boundary(boundaryValues[5][0], boundaryValues[5][1], boundaryValues[5][2], boundaryValues[5][3], [
                                "deal", "All", boundaryValues[5][7], boundaryValues[5][6], boundaryValues[5][5]], boundaryValues[5][4], 0, False)

        if player1.player_bet:
            chosenBet = moneyChoices.clickButtons()
            totalBet = player1.makeUserBet(chosenBet)

        else:
            chosenMove = playerMoves.clickButtons()
            playGame(chosenMove)

        if not player1.player_bet:
            gameOver = score(player1.total(), dealer.total())

    if gameStarted:
        if mode == "name":
            mode = "play"

    if mode == "help1":
        if gameStarted:
            buttonBoundaries = Boundary(boundaryValues[2][0], boundaryValues[2][1], boundaryValues[2]
                                        [2], boundaryValues[2][3], stringValues[10], boundaryValues[2][4], "help1")
        else:
            buttonBoundaries = Boundary(boundaryValues[2][0], boundaryValues[2][1], boundaryValues[2]
                                        [2], boundaryValues[2][3], stringValues[11], boundaryValues[2][4], "help1")

    if mode == "help2":
        buttonBoundaries = Boundary(boundaryValues[3][0], boundaryValues[3][1], boundaryValues[3]
                                    [2], boundaryValues[3][3], stringValues[12], boundaryValues[3][4], "help2")

    if mode == "scores":
        if gameStarted:
            buttonBoundaries = Boundary(boundaryValues[3][0], boundaryValues[3][1], boundaryValues[3]
                                        [2], boundaryValues[3][3], stringValues[13], boundaryValues[3][4], "scores")
        else:
            buttonBoundaries = Boundary(boundaryValues[3][0], boundaryValues[3][1], boundaryValues[3]
                                        [2], boundaryValues[3][3], stringValues[14], boundaryValues[3][4], "scores")

    mode = buttonBoundaries.clickButtons()


def setNameMode():
    global nameMode, terminateInput, charLimit, numLimit, mode, gameStarted, whichKey, deckOfCards, player1Turn, gameOver, stringValues, fieldsFilled,playerDict,users,userArray,userExist,highScores
    #Determine what part of user information the user is clicking
    if mode == "name":
        if nameMode == "number":
            if fieldsFilled[0]:
                if (whichKey == terminateInput) or (len(player1.studNum) == numLimit):
                    if player1.studNum != "":
                        fieldsFilled[0] = False
                        if (player1.firstName != "") and (player1.lastName != ""):
                            nameMode = "continue"
                            whichKey = ""
                            print ("continue")
                            users.append([player1.firstName + " " + player1.lastName,player1.studNum])
                            userArray = indirectSort(users)
                        else:
                            if len(users) != 0:
                                for i in range (len(users)):
                                    if users[i][1] == str(player1.studNum):
                                        player1.firstName = playerDict[int(player1.studNum)][0]
                                        player1.lastName = playerDict[int(player1.studNum)][1]
                                        userExist = True
                                        whichKey = ""
                                        nameMode = "continue"
                                if not(userExist):
                                    userExist = False
                                    nameMode = "first"
                                    whichKey = ""
                            
        if nameMode == "first":
            if fieldsFilled[1]:
                if (whichKey == terminateInput) or (len(player1.firstName) == charLimit):
                    if player1.firstName != "":
                        fieldsFilled[1] = False
                        if player1.lastName == "":
                            nameMode = "last"
                            whichKey = ""
                        elif (player1.studNum != "") and (player1.lastName != ""):
                            nameMode = "continue"
                            whichKey = ""
                            users.append([player1.firstName + " " + player1.lastName,player1.studNum])
                            userArray = indirectSort(users)
                        else: 
                            for i in range (len(users)):
                                if users[i][0] == player1.firstName + player1.lastName:
                                    player1.studNum = users[i][1]
                                    userExist = True
                                    whichKey = ""
                                    nameMode = "continue"
                            if not(userExist):
                                userExist = False
                                whichKey = ""
                                nameMode = "number"

        if nameMode == "last":
            if fieldsFilled[2]:
                if whichKey == terminateInput or (len(player1.lastName) == charLimit):
                    if player1.lastName != "":
                        fieldsFilled[2] = False
                        if player1.firstName == "":
                            nameMode = "first"
                            whichKey = ""
                        elif (player1.studNum != "") and (player1.firstName != ""):
                            nameMode = "continue"
                            whichKey = ""
                            users.append([player1.firstName + " " + player1.lastName,player1.studNum])
                            userArray = indirectSort(users)
                        else: 
                            if len(users) != 0:
                                for i in range (len(users)):
                                    if users[i][0] == player1.firstName + player1.lastName:
                                        player1.studNum = users[i][1]
                                        userExist = True
                                        whichKey = ""
                                        nameMode = "continue"
                            if not(userExist):
                                userExist = False
                                whichKey = ""
                                nameMode = "number"
        
        if nameMode == "continue":
            print (users)
            print (userArray)
            if whichKey == terminateInput:
                mode = "play"
                whichKey = ""

    if (gameOver == True) and (player1.total_money == 0):
        if whichKey == terminateInput:
            for i in range (len(highScores)):
                if int(player1.playerHigh) > int(highScores[i][1]):
                    highScores.insert(i,[player1.firstName + player1.lastName,int(player1.playerHigh)])
                    highScores.pop()
                    break
            print(highScores)
            mode = "end"
            gameStarted = False
            whichKey = ""
        gameOver = False
    
    #Continue game and allow user to play next hand
    if (gameOver == True) and (player1.total_money > 0):
        if whichKey == terminateInput:
            player1Turn = True
            gameOver = False
            if len(player1.player_hand2) > 0:
                player1.player_hand = player1.player_hand2
                player1.player_hand2 = []
                return

            else:
                mode = "play"
                player1.player_bet = True
                player1.total_bet = 0
                deckOfCards = Deck()
                player1.player_hand = []
                dealer.player_hand = []
                dealPlayerDeck()
                whichKey = ""

    if mode == "end":
        #restart the whole game so a new user can play
        if whichKey == terminateInput:
            mode = "home"
            player1.player_bet = True
            player1.total_bet = 0
            player1.total_money = 1000
            deckOfCards = Deck()
            player1.player_hand = []
            dealer.player_hand = []
            dealPlayerDeck()
            player1Turn = True
            gameOver = False
            player1.firstName = ""
            player1.studNum = ""
            player1.lastName = ""
            player1.playerHigh = 1000
            for i in range (len(fieldsFilled)):
                fieldsFilled[i] = True
            userExist = False

            gameStarted = False
            whichKey = ""


#Loading images based off the mode
def loadImagesForMode(mode):
    global imageList, menu, imageValues, whichKey, deckOfCards, player1, gameOver, nameMode, acceptedNums, acceptedChars, delete, scoresInfo, textColour, fieldsFilled,playerDict,playerInfo,users,highScoreInfo,highScores,newUpdateInfo

    if mode == "home":
        UserInterface(imageValues[0][1], imageValues[0][2], imageValues[0]
                      [3], imageValues[0][4]).displayImage(imageList[imageValues[0][0]])
        for i in range(1, 5):
            UserInterface(imageValues[i][1], imageValues[i][2], imageValues[i]
                          [3], imageValues[i][4]).whiteBorder(imageList[imageValues[i][0]])


    if mode == "name":
        textColour = 0
        UserInterface(imageValues[17][1], imageValues[17][2], imageValues[17]
                      [3], imageValues[17][4]).displayImage(imageList[imageValues[17][0]])
        if nameMode == "number":
            if fieldsFilled[0]:
                UserInterface(imageValues[33][1], imageValues[33][2], imageValues[33]
                        [3], imageValues[33][4]).displayImage(imageList[imageValues[33][0]])
                UserInterface(imageValues[29][0], imageValues[29][1]).displayFont(
                    gameFont, textColour, player1.getStudNum(whichKey, acceptedNums, delete))
                whichKey = " "

        UserInterface(imageValues[29][0], imageValues[29][1]).displayFont(
            gameFont, textColour, player1.studNum)
        if nameMode == "first":
            if fieldsFilled[1]:
                UserInterface(imageValues[34][1], imageValues[34][2], imageValues[34]
                        [3], imageValues[34][4]).displayImage(imageList[imageValues[34][0]])
                UserInterface(imageValues[30][0], imageValues[30][1]).displayFont(
                    gameFont, textColour, player1.getFirstName(whichKey, acceptedChars, delete))
                whichKey = ""
        UserInterface(imageValues[30][0], imageValues[30][1]).displayFont(
            gameFont, textColour, player1.firstName)
        if nameMode == "last":
            if fieldsFilled[2]:
                UserInterface(imageValues[35][1], imageValues[35][2], imageValues[35]
                        [3], imageValues[35][4]).displayImage(imageList[imageValues[35][0]])
                UserInterface(imageValues[31][0], imageValues[31][1]).displayFont(
                    gameFont, textColour, player1.getLastName(whichKey, acceptedChars, delete))
                whichKey = ""
        UserInterface(imageValues[31][0], imageValues[31][1]).displayFont(
            gameFont, textColour, player1.lastName)
        textColour = 255
    if mode == "play":
        UserInterface(imageValues[5][1], imageValues[5][2], imageValues[5]
                      [3], imageValues[5][4]).displayImage(imageList[imageValues[5][0]])
        UserInterface(imageValues[27][0], imageValues[27][1]).displayFont(
            gameFont, textColour, "Bet: ${0}".format(player1.total_bet))
        UserInterface(imageValues[28][0], imageValues[28][1]).displayFont(
            gameFont, textColour, "Bank: ${0}".format(player1.total_money))

        for i in range(6, 10):
            UserInterface(imageValues[i][1], imageValues[i][2], imageValues[i]
                          [3], imageValues[i][4]).hoverMenuBar(imageList[imageValues[i][0]])

        for i in range(len(player1.player_hand)):
            copy(imageList[imageValues[19][0]], 73 * player1.player_hand[i][0]-1, 98 * player1.player_hand[i][1]-1, imageValues[19]
                [1], imageValues[19][2], imageValues[19][3] + i * 62, imageValues[19][4], imageValues[19][5], imageValues[19][6])
        UserInterface(imageValues[25][0], imageValues[25][1]).displayFont(
            gameFont, textColour, "{0} Player".format(player1.total()))
        
        # if the game is over show all of the dealers cards.
        if gameOver:
            for i in range(len(dealer.player_hand)):
                copy(imageList[imageValues[19][0]], 73 * dealer.player_hand[i][0]-1, 98 * dealer.player_hand[i][1]-1, imageValues[19]
                     [1], imageValues[19][2], imageValues[19][3] + i * 62, imageValues[19][4] - 290, imageValues[19][5], imageValues[19][6])

            UserInterface(imageValues[26][0], imageValues[26][1]).displayFont(
                gameFont, textColour, "{0} Dealer".format(dealer.total()))
            displayWhoWon(player1.total(), dealer.total())

            if player1.total_money == 0:
                UserInterface(imageValues[23][0], imageValues[23][1]).displayFont(
                    gameFont, textColour, "Press ENTER to Play Again")
            if player1.total_money > 0:
                UserInterface(imageValues[23][0], imageValues[23][1]).displayFont(
                    gameFont, textColour, "Press ENTER to Continue")

        else:
            if not (player1.player_bet):
                for i in range(len(dealer.player_hand)-1):
                    copy(imageList[imageValues[19][0]], 73 * dealer.player_hand[i][0]-1, 98 * dealer.player_hand[i][1]-1, imageValues[19]
                         [1], imageValues[19][2], imageValues[19][3] + i * 62, imageValues[19][4] - 290, imageValues[19][5], imageValues[19][6])
                    UserInterface(imageValues[19][3]-62 + len(dealer.player_hand) * 62, imageValues[20][2],
                                  imageValues[20][3], imageValues[20][4]).displayImage(imageList[imageValues[20][0]])
    
    if mode == "end":
        imageValues[36][1]+=imageValues[36][5]
        imageValues[36][2]+=imageValues[36][6]
        imageValues[37][1]+=imageValues[37][5]
        imageValues[37][2]+=imageValues[37][6]
        UserInterface(imageValues[22][1], imageValues[22][2], imageValues[22]
                      [3], imageValues[22][4]).displayImage(imageList[imageValues[22][0]])
        UserInterface(imageValues[24][0], imageValues[24][1]).displayFont(
            gameFont, imageValues[24][2], "Highest Bank: $ {0}" .format(player1.getPlayerScore(player1.total_money)))
        playerDict = saveScore(player1.studNum, player1.firstName,
                           player1.lastName, player1.playerHigh, player1.date, scoresInfo,playerInfo,users,userExist,highScores,highScoreInfo, newUpdateInfo)
        UserInterface(imageValues[36][1], imageValues[36][2],imageValues[36][3],imageValues[36][4]).displayImage(imageList[imageValues[36][0]])
        UserInterface(imageValues[37][1], imageValues[37][2],imageValues[37][3],imageValues[37][4]).displayImage(imageList[imageValues[37][0]])
        if (abs(imageValues[36][1]-imageValues[37][1]) <= 100) and (abs(imageValues[36][2]-imageValues[37][2]) <= 100):
            if (imageValues[36][5] > 0) and (imageValues[37][5] > 0):
                pass
            elif (imageValues[36][5] < 0) and (imageValues[37][5] < 0):
                pass
            else:
                imageValues[36][5] = -imageValues[36][5]
                imageValues[37][5] = -imageValues[37][5]
            if (imageValues[36][6] > 0) and (imageValues[37][6] > 0):
                pass
            elif (imageValues[36][6] < 0) and (imageValues[37][6] < 0):
                pass
            else:
                imageValues[36][6] = -imageValues[36][6]
                imageValues[37][6] = -imageValues[37][6]
        for i in range(36,38):
            if (imageValues[i][1] >= boundaryValues[7][2]) or (imageValues[i][1] <= boundaryValues[7][0]):
                imageValues[i][5] = -imageValues[i][5]
            if (imageValues[i][2] >= boundaryValues[7][3]) or (imageValues[i][2] <= boundaryValues[7][1]):
                imageValues[i][6] = -imageValues[i][6]

    if mode == "help1":
        UserInterface(imageValues[10][1], imageValues[10][2], imageValues[10]
                      [3], imageValues[10][4]).displayImage(imageList[imageValues[10][0]])
        for i in range(11, 13):
            UserInterface(imageValues[i][1], imageValues[i][2], imageValues[i]
                          [3], imageValues[i][4]).enlargeImage(imageList[imageValues[i][0]])

    if mode == "help2":
        UserInterface(imageValues[13][1], imageValues[13][2], imageValues[13]
                      [3], imageValues[13][4]).displayImage(imageList[imageValues[13][0]])
        UserInterface(imageValues[14][1], imageValues[14][2], imageValues[14]
                      [3], imageValues[14][4]).enlargeImage(imageList[imageValues[14][0]])

    if mode == "scores":
        UserInterface(imageValues[15][1], imageValues[15][2], imageValues[15]
                      [3], imageValues[15][4]).displayImage(imageList[imageValues[15][0]])
        UserInterface(imageValues[16][1], imageValues[16][2], imageValues[16]
                      [3], imageValues[16][4]).enlargeImage(imageList[imageValues[16][0]])

        scoreY = imageValues[32][1]
        # Display top 5 high scores
        for i in range(len(highScores)):
            scoreY += 80
            UserInterface(imageValues[32][0], scoreY).displayFont(gameFont, textColour, str(i+1) + ".  " + str(highScores[i][0]) + ",  " + "$" + str(highScores[i][1]))
    
    if mode == "exit":
        exit()

#identify which key is pressed
def keyPressed():
    global acceptedChars, whichKey, acceptedNums, terminateInput, delete
    # print(ord(key))
    if key != CODED:
        if key.upper() in acceptedChars:
            whichKey = key
        elif key in acceptedNums:
            whichKey = key
        else:
            print("Key unavailable")

    #recognizing specific coded keys (ENTER, BACKSPACE, ESC)
    if keyCode == 10:
        whichKey = terminateInput
    elif keyCode == 8:
        whichKey = delete
    else:
        print("Key unavailable")
    if keyCode == 27:
        this.key = "0"
    else:
        print("Not a character")

    setNameMode()


def saveScore(studNum, firstName, lastName, score, date,scoresInfo,playerInfo,playerArray,inDict,highscore,highScoreInfo,newUpdateInfo):
    inFile = open(scoresInfo, "rb")
    data = pickle.load(inFile)
    inFile.close()
    if inDict == True:
        if score > data[int(studNum)][2]:
            data[int(studNum)] = str(firstName),str(lastName),int(score),str(date)
            outFile = open(newUpdateInfo,"wb")
            addIn = "New high score for " + str(firstName) + str(lastName) + ": " + str(score) + str(date)
            pickle.dump(addIn,outFile)
            outFile.close()
    if inDict == False:
        data[int(studNum)] = str(firstName), str(lastName), int(score), str(date)
        outFile = open(newUpdateInfo,"wb")
        addIn = "New User:" + str(firstName) + str(lastName) + " " + str(studNum) + " " + str(date)
        pickle.dump(addIn,outFile)
        outFile.close()

    outFile = open(scoresInfo, "wb")
    pickle.dump(data, outFile)
    outFile.close()
    print (data)
    outFile = open(playerInfo,"wb")
    pickle.dump(playerArray,outFile)
    outFile.close()
    outFile = open(highScoreInfo,"wb")
    pickle.dump(highscore,outFile)
    outFile.close()
    return(data)

# def bubbleSort(array):
#     for i in range(1, len(array)):
#         sorted = True
#         for j in range(len(array)-i):
#             if (array[j][1]) < (array[j+1][1]):
#                 array[j], array[j+1] = array[j+1], array[j]
#                 sorted = False
#         if sorted:
#             break
#     return(array)

def indirectSort(array):
    sortArray = [i for i in range (len(array))]
    for i in range (1, len(array)):
        sorted = True
        for j in range(len(array)-i):
         if (array[sortArray[j]]) < (array[sortArray[j+1]]):
          sortArray[j], sortArray[j+1] = sortArray[j+1], sortArray[j]
          sorted = False
        if sorted:
         break
    return(sortArray)

def loadScore(scoresInfo,playerInfo,highScoreInfo):
    scoreFile = open(scoresInfo, "rb")
    scores = pickle.load(scoreFile)
    scoreFile.close()
    playerFile = open(playerInfo,"rb")
    users = pickle.load(playerFile)
    playerFile.close()
    highScoreFile = open(highScoreInfo,"rb")
    highScores = pickle.load(highScoreFile)
    highScoreFile.close()
    sortedUsers = indirectSort(users)
    for i in range (len(users)):
        users[i][1] = str(users[i][1])
    #print(scores)
    #print (users)
    #print(sortedUsers)
    #print(highScores)
    return (scores,users,sortedUsers,highScores)


def setup():
    global mode, buttonBoundaries, gameStarted, gameOver, player1Turn, player1, dealer, deckOfCards,playerDict,users,userArray,userExist,highScores
    global imageListNames, imageList, imageValues, boundaryValues, stringValues, scoresInfo, playerInfo,highScoreInfo
    global acceptedChars, whichKey, gameFont, acceptedNums, nameMode, charLimit, numLimit, terminateInput, delete, textColour, fieldsFilled, newUpdateInfo

    size(SCREEN_W, SCREEN_H)
    mode = "home"
    gameOver = False
    gameStarted = False

    imageListNames = loadImageNames("images.txt")
    imageList = loadImages(imageListNames)
    imageValues = loadIntegerValues("imageValues.txt")
    boundaryValues = loadIntegerValues("boundaryValues.txt")
    stringValues = loadIntegerValues("stringValues.txt", False)

    deckOfCards = Deck()
    player1Turn = True
    player1 = Player()
    dealer = Player()
    dealPlayerDeck()

    buttonBoundaries = Boundary(boundaryValues[0][0], boundaryValues[0][1], boundaryValues[0]
                                [2], boundaryValues[0][3], stringValues[7], boundaryValues[0][4], "home")

    #if DEBUG:
        #print (imageListNames)
        #print(imageValues)
        #print (boundaryValues)

    acceptedChars = stringValues[2][0]
    acceptedNums = stringValues[3][0]
    whichKey = stringValues[4][0]
    gameFont = createFont(stringValues[5][0], 32, False)
    textColour = imageValues[21][2]
    nameMode = stringValues[6][0]
    terminateInput = ENTER
    delete = BACKSPACE
    charLimit = 15
    numLimit = 6
    
    scoresInfo = "scores.txt"
    playerInfo = "users.txt"
    highScoreInfo = "highscores.txt"
    newUpdateInfo = "report.txt"
    
    fieldsFilled = [True for i in range (3)]
    
    playerDict,users,userArray,highScores = loadScore(scoresInfo,playerInfo,highScoreInfo)
    userExist = False

def mouseReleased():
    global allBoundaries, mode, buttonBoundaries, imageList, deckOfCards, player1, gameOver, player1Turn
    setMode()
    if DEBUG:
        print("X", mouseX)
        print("Y", mouseY)


def draw():
    global mode, buttonBoundaries, gameStarted, gameOver, player1Turn, player1, dealer, deckOfCards
    global imageListNames, imageList, imageValues, boundaryValues, stringValues, scoresInfo
    global acceptedChars, whichKey, gameFont, acceptedNums, nameMode, charLimit, numLimit, terminateInput, delete, textColour

    clear()
    loadImagesForMode(mode)
