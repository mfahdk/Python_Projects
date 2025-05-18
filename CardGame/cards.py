import random

def make_card(rank, suit):                          #function used to make a card containing rank,suit,name and shorthand
    ranked = rank
    if rank >= 2 and rank <= 14:
        if suit == "Clubs" or suit == "Diamonds" or suit == "Hearts" or suit == "Spades":
            if rank == 11:
                rank = "Jack"
                shorthand = "J"
            elif rank == 12:
                rank = "Queen"
                shorthand = "Q"
            elif rank == 13:
                rank = "King"
                shorthand = "K"
            elif rank == 14:
                rank = "Ace"
                shorthand = "A"
            else:
                shorthand = str(rank)
            name = str(rank) +" Of " + suit
            shorthand = " " + shorthand + suit[:1]
            if suit == "Hearts" or suit == "Diamonds":
                color = "\033[31m "+shorthand+"\033[37m"
            else:
                color = "\033[34m "+shorthand+"\033[37m"
            print(color)
            tuple1 = (ranked,suit,name,shorthand)
            return tuple1

def test_make_card():                                   #test for make_card function
    assert make_card(2,"Clubs") == (2,"Clubs", "2 Of Clubs", " 2C")
    assert make_card(10,"Diamonds") == (10,"Diamonds", "10 Of Diamonds", " 10D")
    assert make_card(11,"Hearts") == (11,"Hearts","Jack Of Hearts", " JH")
    assert make_card(12,"Spades") == (12,"Spades", "Queen Of Spades"," QS")
    assert make_card(13,"Clubs") == (13,"Clubs","King Of Clubs", " KC")
    assert make_card(14,"Diamonds") == (14,"Diamonds", "Ace Of Diamonds", " AD")

def make_deck():                                        #test for making deck of 52 cards
    Deck=[]
    i=2
    z="Diamonds"
    for x in range(52):
        Deck.append(make_card(i,z))
        if i==14:
            i=2
        else:
            i+=1
    
        if x==12:
            z="Clubs"
        elif x==25:
            z="Hearts"
        elif x==38:
            z="Spades"    
    return(Deck)           


def test_make_deck():                               #test for the make_deck function
    deck = make_deck()
    assert deck[13]==(2, 'Clubs', '2 Of Clubs', ' 2C')
    assert deck[0]==(2, 'Diamonds', '2 Of Diamonds', ' 2D')
    assert deck[26]==(2, 'Hearts', '2 Of Hearts', ' 2H')
    assert deck[39]==(2, 'Spades', '2 Of Spades', ' 2S')

    
def shuffle(deck):                                  #function to shuffle the deck to random arrangements
    for i in range(len(deck)):
        if 0<=i<len(deck)-1:
            j=random.randint(i,len(deck)-1)
            temp=deck[i]
            deck[i]=deck[j]
            deck[j]=temp
    return deck

def test_shuffle_deck():                            #test for shuffle function
    random.seed(0)
    deck = make_deck()
    shuffle(deck)
    assert deck[0]==(13, 'Clubs', 'King Of Clubs', ' KC')


def draw(handnumber,deck):                          #function to draw hand of cards  
    if len(deck)>0:
        a=deck.pop()
        handnumber.append(a)
        return(handnumber,deck)
    else:
        return None

def deal(deck,number,hand1,hand2):                  #function to distrubute cards to player
    while number>0:
        draw(deck,hand1)
        draw(deck,hand2)
        number-=1
    return hand1,hand2

def print_card(Card):                               #function for printing out the cards
    x=0
    for y in Card:
        if x==3:
            if Card[3][-1] == "D" or Card[3][-1] == "H":
                print("\033[31m",y,"\033[37m",sep = "",end = "")
            else:
                print("\033[34m",y,"\033[37m",sep = "",end = "")
        else:
            print(y," | ",sep = "",end = "")
        x=x+1
    print("")

def play_round(hand,deck):                          #function for playing a round of cards
    if len(hand)>=4:
        if hand[-4][-1][-1]==hand[-1][-1][-1]:
            for _ in range(4):
                del hand[-1]
            if len(hand)>4:
                if hand[-4][-1][-1]==hand[-1][-1][-1]:
                    play_round(hand,deck)
        elif hand[-3][-1][-1]==hand[-2][-1][-1]:
            for _ in range(2):
                del hand[-2]
            if len(hand)>4:
                if hand[-3][-1][-1] == hand[-2][-1][-1]:
                    play_round(hand,deck)

    if len(hand)==0:
        if len(deck)==0:
            print("\033[30m---------------\n\033[37mHere, Both the Deck and the Hand have '0' Cards!\n\033[33mCongrats! You won!\033[37m")
            return(hand,deck,False)
    elif len(hand)>0:
        if len(deck)==0:
            print("\033[30m---------------\n\033[37mHere, The deck is Empty but you are still in possession of Cards in your Hand!.\n\033[31mSorry! You Lost!\033[37m")
            return(hand,deck,False)
    else:
        print("\033[30m---------------\n\033[31m[ERROR!]\033[37m")
        return(hand,deck,False)
    
    hand,deck=draw(hand,deck)
    return(hand,deck,True)

test_make_card()
test_make_deck()
test_shuffle_deck()
