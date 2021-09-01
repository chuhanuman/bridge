from random import shuffle
import tkinter as tk
from time import time,sleep
from copy import deepcopy
from datetime import datetime
import math
playoutdict = {}
def new_window(root,title,h=50,w=300):
    """
    Creates a window from the root window using tkinter with a label displaying the text "Your cards: ", a text field,
    and a button with that when pressed assigns the value in the textfield to the global variable entry
    and packs the window
    
    Input: root - tkinter.Tk object - root window
           title - string - title of the window
           h(optional) - integer - height of the window, defaults to 50
           w(optional) - integer - width of the window, defaults to 300

    Output: window - tkinter.Toplevel - window object the function creates
    """
    window = tk.Toplevel(root)
    canvas = tk.Canvas(window,height=h,width=w)
    canvas.pack()
    window.title(title)
    label = tk.Label(window,text="Your cards: ")
    entry = tk.Entry(window)
    button = tk.Button(window,text="Enter your action",bg='black',fg='#469A00',command=lambda:get_textfield(entry))
    label.pack()
    entry.pack()
    return window
def get_textfield(field):
    """
    Used in new_window function, changes the global variable entry to the input variable field when button is pressed,
    usually changes entry to a tkinter.Entry object
    
    Input: field - any variable - anything
    
    Output: None
    """
    global entry
    entry = field
def update_hands(root,hands):
    """
    Updates the hands of all 4 windows from root

    Input: root - tkinter.Tk object - root window
           hands - list - list of 4 hands which are lists of cards

    Output: None
    """
    for i in range(4):
        root.winfo_children()[6+i].winfo_children()[1].config(text="Your cards: "+str(hands[i]))
def notify():
    """
    Changes the global value ready to True to signal that input was recieved

    Input: None

    Output: None
    """
    global ready
    ready = True
def get_input(root,button,message):
    """
    Updates a button with a message, waits for it to be pressed,
    then returns the value that the global entry object has in its text field

    Input: root - tkinter.Tk object - root window
           button - tk.Button object - player window's button
           message - string - message that the button displays

    Output: ans - string - value in text field of the global entry object when the button is pressed
    """
    button.config(text=message)
    button.pack()
    global entry
    entry = ""
    while entry == "":
        root.update()
        sleep(0.1)
    ans = entry.get()
    button.pack_forget()
    entry.delete(0,"end")
    return ans
def update_points(pointlabel,score1,score2,trickswon=0,total=0):
    """
    Updates the point label object with the current score

    Input: pointlabel - tkinter.Label object - scoreboard
           score1 - integer - score of the player 1 and player 3 team
           score2 - integer - score of the player 2 and player 4 team
           trickswon(optional) - integer - amount of tricks the bidding player's team won, defaults to 0
           total(optional) - integer - amount of tricks played, defaults to 0

    Output: None
    """
    pointlabel.config(text="Team 13: "+str(score1)+"\nTeam 24: "+str(score2)+"\nTricks won: "+str(trickswon)+"/"+str(total))
    pointlabel.pack()
def error(errorlabel,errortext):
    """
    Updates errorlabel with errortext and stops the program until the error is acknowledged

    Input: errorlabel - tkinter.Label object - error label
           errortext - string - error text

    Output: None
    """
    errorlabel.config(text=errortext)
    errorlabel.pack()
    wait(button)
def wait(button):
    """
    Updates button with the text "Continue" and stalls the program until the button is pressed

    Input: button - tkinter.Button - main button

    Output: None
    """
    button.config(text="Continue")
    button.pack()
    global ready
    while not ready:
        root.update()
        sleep(0.1)
    ready = False
    button.pack_forget()
def auction(dealer):
    """
    Auction part of bridge card game

    Input: dealer - integer - number of the dealing player from [1,2,3,4]

    Output: bid - list of two integers - bid determined in format [trump,tricks], if no bid was determined [0,1]
            multiplier - integer - 1 if no double or redouble, 2 if double, 4 if redouble
            trumpbidder - integer - number of the player who first bid the trump of the final bid
            bidder - integer - number of the player who bid the final bid
    """
    multiplier = 1
    timetoend = 4
    player = dealer
    trumpbidder = 0
    doubler = 0
    bidder = 0
    bid = [0,1] #[trump,tricks]
    mainlabel.config(text="")
    mainlabel.pack()
    while timetoend != 0:
        pwindow = root.winfo_children()[5+player]
        choice = get_input(root,pwindow.winfo_children()[3],"Enter your action")
        errorlabel.pack_forget()
        if choice == "pass":
            timetoend-=1
            mainlabel.config(text=mainlabel.cget("text")+str(player)+":pass ")
        elif choice == "double":
            if bidder == 0:
                error(errorlabel,"Error: No bid to double")
                continue
            if (player-bidder)%2 == multiplier%2:
                error(errorlabel,"Error: Have to double/redouble enemy")
                continue
            if multiplier == 4:
                error(errorlabel,"Error: Already doubled twice")
                continue
            multiplier*=2
            mainlabel.config(text=mainlabel.cget("text")+str(player)+":double ")
        elif choice == "bid":
            suit = int(get_input(root,pwindow.winfo_children()[3],"Enter trump"))
            tricks = int(get_input(root,pwindow.winfo_children()[3],"Enter number of tricks"))
            if tricks < bid[1]:
                error(errorlabel,"Error: Too low tricks")
                continue
            elif tricks == bid[1]:
                if suit > bid[0]:
                    trumpbidder = player
                    bidder = player
                    multiplier = 1
                    bid[0] = suit
                    mainlabel.config(text=mainlabel.cget("text")+str(player)+":"+str(suit)+","+str(tricks)+" ")
                else:
                    error(errorlabel,"Error: Too low trump denomination")
                    continue
            else:
                if suit != bid[0]:
                    trumpbidder = player
                bidder = player
                multiplier = 1
                bid = [suit,tricks]
                mainlabel.config(text=mainlabel.cget("text")+str(player)+":"+str(suit)+","+str(tricks)+" ")
            timetoend = 3
        else:
            error(errorlabel,"Error: Not a valid choice")
            continue
        if player < 4:
            player+=1
        else:
            player = 1
    return bid,multiplier,trumpbidder,bidder
def findwinner(bid,bsttrump,bststarter,bidder):
    if bid[0] == 5 or bsttrump[0] == 0:
        winner = bststarter[1]
    else:
        winner = bsttrump[1]
    if winner%2 == bidder%2:
        return(winner,1)
    return(winner,0)
def playout(hands,bid,board,player,dummy,bststarter,bsttrump,depth,debug,final=0,maxdepth=2):
    #FIX Optimize
    #call = str([hands,0,bid,0,board,0,player,0,dummy,0,bststarter,0,bsttrump,0,original])
    call = str([hands,depth])
    if call in playoutdict:
        info = playoutdict[call]
        if final:
            return info[0],(info[1] if player%2 else (maxdepth+1-info[1]))
        return info
    cards = []
    costs = []
    hasstarter = False
    if len(board) != 0:
        for card in hands[player-1]:
            if card[0] < board[0][0]:
                continue
            elif card[0] == board[0][0]:
                hasstarter = True
            break
    for card in hands[player-1]:
        #If has string of cards treat the same
        if [card[0],card[1]-1] in cards:
            cards.append(card)
            costs.append(costs[cards.index([card[0],card[1]-1])])
            continue
        if len(board) != 0 and hasstarter:
            if card[0] < board[0][0]:
                continue
            elif card[0] > board[0][0]:
                break
        temphands = deepcopy(hands)
        temphands[player-1].remove(card)
        if len(board) == 3:
            if debug:
                print(board,card)
            winner,win = findwinner(bid,bsttrump,bststarter,1)
            cards.append(card)
            if depth == maxdepth:
                costs.append(0 if win else 1)
            else:
                costs.append((0 if win else 1)+playout(temphands,bid,[],winner,dummy,[0,0],[0,0],depth+1,debug)[1])
        else:
            cards.append(card)
            temp = bststarter
            if len(board) == 0 or (board[0][0] == card[0] and card[1] > bststarter[0]):
                temp = [card[1],player]
            temp2 = bsttrump
            if bid[0] == card[0] and card[1] > temp2[0]:
                temp2 = [card[1],player]
            if player < 4:
                temp3 = player + 1
            else:
                temp3 = 1
            costs.append(playout(temphands,bid,board+[card],temp3,dummy,temp,temp2,depth,debug)[1])
    if len(costs) == 0:
        return 0,0
    #if player%2 == original%2:
    if player%2:
        index = costs.index(min(costs))
    else:
        index = costs.index(max(costs))
    playoutdict[call] = [cards[index],costs[index]]
    #playoutdict[call] = [cards[index],(costs[index] if player%2 else (len(hands[player-1])-costs[index]))]
    if final == 1:
    #    print(hands,bid,board,player,dummy,bststarter,bsttrump,original)
    #    print(cards,costs)
        return cards[index],(costs[index] if player%2 else (maxdepth+1-costs[index]))
    return cards[index],costs[index]
    
def simplebridgeai(hands,board,bid,bidder,player,dummy,starter,bststarter,bsttrump,cardsplayed):
    #Basic winning detection
    winning = False
    notrumps = bid[0] == 5 or bsttrump[0] == 0
    if notrumps:
        winner = bststarter[1]
    else:
        winner = bsttrump[1]
    if winner%2 == player%2:
        winning = True
    #Find least valuable card
    lowest = [0,100]
    lowesttrump = [0,100]
    for card in hands[player-1]:
        if starter == "":
            if card[1] < lowest[1]:
                lowest = card
            continue
        if card[0] == starter:
            if lowest == [0,100]:
                lowest = card
                break
        if card[0] > starter:
            break
    if lowest == [0,100]:
        for card in hands[player-1]:
            if card[1] < lowest[1]:
                lowest = card
            if card[0] == bid[0]:
                if card[1] < lowesttrump[1]:
                    lowesttrump = card
    if not(winning):
        #If first play worst
        if starter == "":
            return lowest
        #Attempt to win
        if notrumps:
            if lowest[0] == starter:
                #Play highest starter that beats them
                for card in hands[player-1]:
                    if card[0] < starter:
                        continue
                    elif card[0] == starter:
                        if card[1] > bststarter[1]:
                            return card
                    else:
                        break
            elif lowesttrump != [0,100]:
                return lowesttrump
        elif lowesttrump != [0,100]:
            #Play highest trump that beats them
            for card in hands[player-1]:
                if card[0] < bid[0]:
                    continue
                elif card[0] == bid[0]:
                    if card[1] > bsttrump[1]:
                        return card
                else:
                    break
    return lowest
def advancedbridgeai(hands,board,bid,bidder,player,dummy,starter,bststarter,bsttrump,cardsplayed):
    starttime = time()
    #Find route with least potential losses FIX
    #Don't have perfect information FIX
    card,losses = playout(hands,bid,board,player,dummy,bststarter,bsttrump,0,False,final=1)
    #print(time()-starttime)
    #print(card,losses)
    return card

def simpleminmaxbridgeai(hands,board,bid,bidder,player,dummy,starter,bststarter,bsttrump,cardsplayed):
    score = {}
    availablecards = deck[:]
    for card in deck:
        if (card in cardsplayed) or (card in hands[player-1]) or (card in hands[dummy-1]) or (card in cardsplayed):
            availablecards.remove(card)
    notrumps = bid[0] == 5 or bsttrump[0] == 0
    winning = False
    if notrumps:
        winner = bststarter[1]
    else:
        winner = bsttrump[1]
    if winner%2 == player%2:
        winning = True
    if board != []:
        hasstarter = False
        for card in hands[player-1]:
            if card[0] > bststarter[0]:
                break
            elif card[0] == bststarter[0]:
                hasstarter = True
    for card in hands[player-1]:
        #Chance that enemy will win trick is not dependent on auction FIX
        #Chance that enemy will win trick is not dependent on whether they will want to beat card FIX
        #Chance that enemy will win trick is dependent only on whether they can beat card with the information of cards played
        #Don't need to calculate all again each time FIX
        #Implement bridge rules (guide to good playing) FIX
        if board != [] and hasstarter:
            if card[0] != bststarter[0]:
                break
        tempbststarter = bststarter[:]
        tempbsttrump = bsttrump[:]
        tempwinning = winning
        tempavailablecards = availablecards[:]
        tempnotrumps = notrumps
        if len(board) == 0:
            #FIX
            pass
        else:
            if tempnotrumps:
                if bid[0] == card[0]:
                    tempbsttrump = card[:]
                    tempnotrumps = False
                    tempwinning = True
                elif bststarter[0] == card[0] and card[1] > bststarter[1]:
                    tempbststarter = card[:]
                    tempwinning = True
            else:
                if bid[0] == card[0] and card[1] > bsttrump[1]:
                    tempbsttrump = card[:]
                    tempwinning = True
            if len(board) == 1:
                #Chance that enemy will beat our card * chance that enemy will beat our teammate's card given that they will beat our card
                #FIX
                pass
            if len(board) == 2:
                if player == 4:
                    nextplayer = 1
                else:
                    nextplayer = player + 1
                #Chance that enemy will beat our card
                if not(winning):
                    chanceofloss = 1
                else:
                    numberofcardsthatbeatours = 0
                    if nextplayer == dummy:
                        tempavailablecards = hands[dummy-1]
                    for potentialcard in tempavailablecards:
                        #Include has starter in the probability FIX
                        if tempnotrumps:
                            if bid[0] == potentialcard[0]:
                                numberofcardsthatbeatours += 1
                            elif bststarter[0] == potentialcard[0] and potentialcard[1] > bststarter[1]:
                                numberofcardsthatbeatours += 1
                        elif bid[0] == potentialcard[0] and potentialcard[1] > bsttrump[1]:
                            numberofcardsthatbeatours += 1
                    if numberofcardsthatbeatours > len(tempavailablecards) - len(hands[nextplayer-1]):
                        chanceofloss = 1
                    else:
                        handsize = len(hands[nextplayer-1])
                        totalpossibilities = math.comb(len(tempavailablecards),handsize)
                        winningpossibilities = math.comb(len(tempavailablecards)-numberofcardsthatbeatours,handsize)
                        #6 choose 3 beat = 1 chance = 1 - (5/6)*(4/5)*(3/4) = 1 - math.comb(5,3)/math.comb(6,3)
                        #6 choose 3 beat = 2 chance = 1 - (4/6)*(3/5)*(2/4) = 1 - math.comb(4,3)/math.comb(6,3)
                        #6 choose 3 beat = 3 chance = 1 - (3/6)*(2/5)*(1/4) = 1 - math.comb(3,3)/math.comb(6,3)
                        chanceofloss = 1 - winningpossibilities/totalpossibilities
                    print(numberofcardsthatbeatours)
                    print(chanceofloss)
            if len(board) == 3:
                #0 if we win otherwise 1
                chanceofloss = not(tempwinning)
            
        #Score = chance that enemy will win trick * 100 + value of card
        #Value of card if suit of card is not trumo = number of card
        #Value of card if suit of card is trump = number of card * 2
        cardvalue = card[1]
        if bid[0] == card[0]:
            cardvalue *= 2
        score[str(card)] = chanceofloss * 100 + cardvalue
    #We want to minimize score
    print(score)
    return min(score,key=score.get)

#def basicauctionai(): FIX

def log(message):
    f = open("log.txt", "a")
    f.write("\n"+datetime.now().strftime("%H:%M:%S")+": "+str(message))
    f.close()
def bridge(score1=[0,0],score2=[0,0],vul=0,debug=0):
    button.pack_forget()
    update_points(pointlabel,score1,score2)
    #Fix go once
    #while (score1[1] < 100 and score2[1] < 100):
    while score1 == [0,0] and score2 == [0,0]:
        temp = deck[:]
        shuffle(temp)
        p1hand, p2hand, p3hand, p4hand = [],[],[],[] #N,E,S,W
        for i in range(13):
            p1hand.append(temp.pop())
            p2hand.append(temp.pop())
            p3hand.append(temp.pop())
            p4hand.append(temp.pop())
        """
        p3hand = [[1,8],[1,12],[1,14],[3,7],[4,11],[4,13]]
        p2hand = [[1,2],[1,3],[1,4],[1,11],[1,13],[3,10]]
        p1hand = [[1,5],[1,9],[1,10],[3,8],[4,10],[4,12]]
        p4hand = [[1,6],[3,11],[3,12],[3,13],[4,8],[4,9]]
        """
        p1hand.sort()
        p2hand.sort()
        p3hand.sort()
        p4hand.sort()
        hands = [p1hand,p2hand,p3hand,p4hand]
        update_hands(root,hands)
        #bid,multiplier,player,bidder = auction(1)
        #FIX
        multiplier = 1
        player = PLAYER
        bidder = PLAYER
        count = [0,0,0,0,0]
        for card in hands[player-1]+hands[player+1]:
            if card[1] >= 10:
                count[0] += 1
                count[card[0]] += 1
        count[0] /= 3
        if max(count) >= 4:
            bid = [count.index(max(count)),1]
        else:
            bid = [0,1]
        #FIX
        mainlabel.pack()
        """
        bid = [3,2]
        multiplier = 1
        player = 4
        bidder = 4
        """
        if not(debug):
            wait(button)
        if bid == [0,1]:
            mainlabel.config(text="")
            continue
        else:
            log(hands)
            log(bid)
            dummy = player + 2
            if dummy > 4:
                dummy-=4
            mainlabel.config(text=str(dummy)+"'s cards: "+str(hands[dummy-1])+"\nBid: "+str(bid)+"\n")
            trickswon = 0
            update_points(pointlabel,score1,score2,trickswon)
            player+=1
            cardsplayed = []
            for i in range(13):
                """
                if i < 7:
                    player = 4
                    trickswon = 4
                    continue
                """
                starter = ""
                cards = []
                bststarter = [0,0] #[number,player]
                bsttrump = [0,0]
                cardslabel.pack()
                for j in range(4):
                    while True:
                        #implement dummy
                        errorlabel.pack_forget()
                        if player%2 == 0:
                            #FIX not always AI
                            suit,number = advancedbridgeai(hands,cards,bid,bidder,player,dummy,starter,bststarter,bsttrump,cardsplayed)
                        elif player%2 == 1:
                            suit,number = simpleminmaxbridgeai(hands,cards,bid,bidder,player,dummy,starter,bststarter,bsttrump,cardsplayed)
                        else:
                            if player == dummy:
                                if player - 2 < 1:
                                    pwindow = root.winfo_children()[7+player]
                                else:
                                    pwindow = root.winfo_children()[3+player]
                            else:
                                pwindow = root.winfo_children()[5+player]
                            suit = int(get_input(root,pwindow.winfo_children()[3],"Enter suit of card"))
                            number = int(get_input(root,pwindow.winfo_children()[3],"Enter number of card"))
                            pwindow.winfo_children()[3].pack_forget()
                        if [suit,number] not in hands[player-1]:
                            error(errorlabel,"Error: Card not in hand")
                            continue
                        if starter == "":
                            starter = suit
                        elif starter != "" and suit != starter:
                            leave = False
                            for card in hands[player-1]:
                                if card[0] == starter:
                                    error(errorlabel,"Error: Card not of proper suit")
                                    leave = True
                                    break
                            if leave:
                                continue
                        if starter == suit and number > bststarter[0]:
                            bststarter[0] = number
                            bststarter[1] = player
                        if bid[0] == suit and number > bsttrump[0]:
                            bsttrump[0] = number
                            bsttrump[1] = player
                        if j == 0:
                            cardslabel.config(text=str(player)+": "+str([suit,number])+" ")
                        else:
                            cardslabel.config(text=cardslabel.cget("text")+str(player)+": "+str([suit,number])+" ")
                        cards.append([suit,number])
                        hands[player-1].remove([suit,number])
                        update_hands(root,hands)
                        mainlabel.config(text=str(dummy)+"'s cards: "+str(hands[dummy-1])+"\nBid: "+str(bid)+"\n")
                        if player < 4:
                            player+=1
                        else:
                            player = 1
                        break
                winner,win = findwinner(bid,bsttrump,bststarter,bidder)
                trickswon+=win
                update_points(pointlabel,score1,score2,trickswon,i+1)
                player = winner
                if not(debug):
                    wait(button)
                cardsplayed+=cards
                log(cards)
            cardslabel.pack_forget()
            """trickswon = 8"""
            bidvul = 1
            if bidder%2 == 1:
                if vul == 1:
                    bidvul = 2
                scorer = score1
                nonscorer = score2
            else:
                if vul == 2:
                    bidvul = 2
                scorer = score2
                nonscorer = score2
            if trickswon < (6 + bid[1]):
                if multiplier == 1:
                    nonscorer[0]+=bidvul*50*(6+bid[1]-trickswon)
                else:
                    nonscorer[0]+=multiplier*bidvul*50
                    if bidvul == 2 and trickswon < (4 + bid[1]):
                        nonscorer[0]+=multiplier*150*(4+bid[1]-trickswon)
                    else:
                        if trickswon < (4 + bid[1]):
                            nonscorer[0]+=multiplier*100*(4+bid[1]-trickswon)
                        if trickswon < (3 + bid[1]):
                            nonscorer[0]+=multiplier*50*(3+bid[1]-trickswon)
            else:
                if bid[0] < 3:
                    scorer[1]+=multiplier*20*bid[1]
                elif bid[0] < 5:
                    scorer[1]+=multiplier*30*bid[1]
                else:
                    scorer[1]+=multiplier*40
                    scorer[1]+=multiplier*30*(bid[1]-1)
                if multiplier == 1:
                    if bid[0] < 3:
                        scorer[0]+=bidvul*20*(trickswon-6-bid[1])
                    else:
                        scorer[0]+=bidvul*30*(trickswon-6-bid[1])
                elif multiplier > 1:
                    scorer[0]+=multiplier*bidvul*50*(trickswon-6-bid[1])
                    scorer[0]+=multiplier*25
                if bid[1] > 5:
                    scorer[0]+=bidvul*500*(bid[1]-5)
            update_points(pointlabel,score1,score2)
    if not(debug):
        wait(button)
    if score1[1] >= 100:
        winner = 1
    else:
        winner = 2
    button.pack()
    score1[0]+=score1[1]
    score1[1] = 0
    score2[0]+=score2[1]
    score2[1] = 0
    update_points(pointlabel,score1[0],score2[0])
    if not(debug):
        return score1[0],score2[0],winner
    else:
        return str(trickswon)+"/13"
deck = [] #[suit,value] suit is 1-4 from this list Club, Diamond, Heart, Spade
for suit in range(1,5):
    for value in range(1,14):
        if value == 1:
            value = 14
        deck.append([suit,value])
global ready
ready = False
root = tk.Tk()
root.title("Bridge")
canvas = tk.Canvas(root)
canvas.pack()
button = tk.Button(root,text="Play",bg='black',fg='#469A00',command=lambda:notify())
mainlabel = tk.Label(root,text="")
cardslabel = tk.Label(root,text="")
pointlabel = tk.Label(root,text="Team 13: 0\nTeam 24: 0")
errorlabel = tk.Label(root,text="Error")
while True:
    button.config(text="Play")
    button.pack()
    while not ready:
        root.update()
        sleep(0.1)
    ready = False
    w1 = new_window(root,"Player 1")
    w2 = new_window(root,"Player 2")
    w3 = new_window(root,"Player 3")
    w4 = new_window(root,"Player 4")
    """wins = [0,0]
    score1,score2,winner = bridge([0,0],[0,0])
    wins[winner-1]+=1
    score1,score2,winner = bridge([score1,0],[score2,0],winner)
    wins[winner-1]+=1
    if wins[0] == 1:
        score1,score2,winner = bridge([score1,0],[score2,0],winner)
        wins[winner-1]+=1
        if winner == 1:
            score1+=500
        else:
            score2+=500
    else:
        if winner == 1:
            score1+=700
        else:
            score2+=700
    update_points(pointlabel,score1,score2)"""
    print("Simple")
    log("Simple")
    PLAYER = 1
    for i in range(10):
        playoutdict = {}
        starttime=time()
        fraction = bridge([0,0],[0,0],debug=1)
        print(fraction)
        log(fraction)
        timeelapsed = time()-starttime
        print(str(timeelapsed//3600)+" hours "+str(timeelapsed%3600//60)+" minutes "+str(timeelapsed%60)+" seconds")
        log(str(timeelapsed//3600)+" hours "+str(timeelapsed%3600//60)+" minutes "+str(timeelapsed%60)+" seconds")
        #wait(button)
    print("Advanced")
    log("Advanced")
    PLAYER = 2
    for i in range(20):
        playoutdict = {}
        starttime=time()
        fraction = bridge([0,0],[0,0],debug=1)
        print(fraction)
        log(fraction)
        timeelapsed = time()-starttime
        print(str(timeelapsed//3600)+" hours "+str(timeelapsed%3600//60)+" minutes "+str(timeelapsed%60)+" seconds")
        log(str(timeelapsed//3600)+" hours "+str(timeelapsed%3600//60)+" minutes "+str(timeelapsed%60)+" seconds")
        #wait(button)
    w1.destroy()
    w2.destroy()
    w3.destroy()
    w4.destroy()

    
    


