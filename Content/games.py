import tkinter as tk
import random



class Game:

    def __init__(self):
        with open("settings.txt", "r") as f:
            out = f.readlines()
            out = [x.split()[1] for x in out]
        self.selfsleep = int(out[0])
        self.selfup = out[2]
        self.selfdown = out[3]
        self.selfreturn = out[4]
        self.line = 1
        self.taglines = []

    def reapply_tag(self):
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

        for i, line in enumerate(self.taglines):
            color, start, end = line
            self.text.tag_add(f"colour{i}", start, end)
            self.text.tag_config(f"colour{i}", foreground=color)

    def sleep(self, t):
        self.root.after(int(t*1000), lambda: self.sleepCount.set(self.sleepCount.get()+1))
        self.root.wait_variable(self.sleepCount)
    
    def write(self, txt=""):
        self.text['state'] = 'normal'
        self.text.insert(tk.END, txt+"\n")
        self.text['state'] = 'disabled'
        self.line += 1

    def write_color(self, txt, color):
        """
        writes red to the text field in red

        the colors rely on the line tracker which only increments by 1
        for each thing you write pls pls pls do not use newline characters
        """
        self.text['state'] = 'normal'
        self.text.insert(tk.END, txt+"\n")

        self.taglines.append([color, f"{self.line}.0", f"{self.line}.end"])
        self.text['state'] = 'disabled'
        self.line += 1
        self.reapply_tag()
    
    def delete(self, keeptag=False):
        self.text['state'] = 'normal'
        self.text.delete("1.0", tk.END)
        self.text['state'] = 'disabled'
        self.line = 1

        if not keeptag:
            self.taglines = []
            for tag in self.text.tag_names():
                self.text.tag_delete(tag)
    
    def wait_for_key_press(self):
        self.write("\nPress any key to continue")
        self.root.bind('<Key>', lambda x: self.pause_var.set("done"))
        self.root.wait_variable(self.pause_var)
        self.root.unbind('<Key>')
        self.pause_var.set("")
        
    def show(self, prompt, options, deletebefore):
        data = self.text.get("1.0",'end-1c')
        self.delete(True)
        keep = ""
        if not deletebefore:
            keep = data.split(prompt)[0]
            
        """main action for user to get the list of possible actions"""
        # Displays the list of actions the user can do
        p = self.pointer.get()
        self.write(keep+prompt+"\n")
        for i, e in enumerate(options):
            arrow = " "
            if p == i: arrow = ">"
            self.write(f"{arrow} {e}")
        self.reapply_tag()
            
    def up_action(self, prompt, options, delete):
        p = self.pointer.get()
        if p != 0:
            self.pointer.set(p-1)
        else:
            self.pointer.set(len(options)-1)
    
        self.show(prompt, options, delete)
    
    def down_action(self, prompt, options, delete):
        p = self.pointer.get()
        if p != len(options)-1:
            self.pointer.set(p+1)
        else:
            self.pointer.set(0)
    
        self.show(prompt, options, delete)
    
    def get_input(self, prompt, options, displayoptions = None, deletebefore = True):
        """sub action for run() that prompts user for a main action"""
        if displayoptions is None:
            displayoptions = options
        self.show(prompt, displayoptions, deletebefore)
        self.root.bind(f'<{self.selfreturn}>', lambda x: self.pause_var.set("done"))
        self.root.bind(f"<{self.selfup}>", lambda e: self.up_action(prompt, displayoptions, deletebefore))
        self.root.bind(f"<{self.selfdown}>", lambda e: self.down_action(prompt, displayoptions, deletebefore))
        self.root.wait_variable(self.pause_var)
        self.root.unbind(f'<{self.selfreturn}>')
        self.root.unbind(f"<{self.selfup}>")
        self.root.unbind(f"<{self.selfdown}>")
        self.pause_var.set("")
        decision = options[self.pointer.get()]
        self.pointer.set(0)
        self.delete()
        return decision

    def get_bet(self):
        amount = 1
        bets = []
        while self.player.money >= amount:
            bets.append(str(amount))
            amount *= 10

        bets.append("Cancel")

        bet = self.get_input(f"How much would you like to bet? (You have {self.player.money} runes)", bets)

        return bet
    
class JanKenPon(Game):
    def __init__(self, player, root, text):
        super().__init__()
        self.root = root
        self.text = text
        self.player = player
        self.pause_var = tk.StringVar()
        self.pointer = tk.IntVar()
        self.sleepCount = tk.IntVar()

    def play(self):
        bet = self.get_bet()

        if bet == "Cancel":
            self.delete()
            
        else:
            moves = ["Rock", "Paper", "Scissors"]
            selection = self.get_input("What do you want to use?", moves)
            opponent_selection = random.choice(moves)
            if selection == opponent_selection:
                self.write(f"Your opponent also used {selection}, its a draw")
                self.sleep(self.selfsleep)
                self.write()
                self.write(f"You get back {bet} runes")

            elif (selection == "Rock" and opponent_selection == "Paper") or (selection == "Paper" and opponent_selection == "Scissors") or (selection == "Scissors" and opponent_selection == "Rock"):
                self.write(f"Your opponent used {opponent_selection}, you lost")
                self.sleep(self.selfsleep)
                self.write()
                self.write_color(f"You lost {bet} runes", "red")
                self.player.money -= int(bet)
            
            else:
                self.write(f"Your opponent used {opponent_selection}, you won")
                self.sleep(self.selfsleep)
                self.write()
                self.write_color(f"You earned {bet} runes", "green")
                self.player.money += int(bet)
            
            self.write()
            choice = self.get_input("Do you want to play again?", ["Yes", "No"], None, False)
            self.delete()
            if choice == "Yes":
                self.play()

class Blackjack(Game):

    def __init__(self, player, root, text):
        super().__init__()
        self.root = root
        self.text = text
        self.player = player
        self.pause_var = tk.StringVar()
        self.pointer = tk.IntVar()
        self.sleepCount = tk.IntVar()

    def play(self):
        bet = self.get_bet()

        if bet == "Cancel":
            self.delete()

        else:
            cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
            values = {
                "A": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 10,
                "J": 10,
                "Q": 10,
                "K": 10
            }
            card1 = random.choice(cards)
            card2 = random.choice(cards)
            opponent_card1 = random.choice(cards)
            opponent_card2 = random.choice(cards)
            value1 = values[card1]
            value2 = values[card2]
            opponent1 = values[opponent_card1]
            opponent2 = values[opponent_card2]

            player_cards = [card1, card2]
            
            if card1 == "A":
                value1 = 11
            elif card2 == "A":
                value2 = 11

            if opponent_card1 == "A":
                opponent1 = 11
            elif opponent_card2 == "A":
                opponent2 = 11
                
            total = value1 + value2
            opponent_total = opponent1 + opponent2
        
            self.write("your first 2 cards are")
            self.write()
            self.write(f"{card1} {card2}")
            self.write()
            self.write(f"your total is {total}")
            self.write()
            self.sleep(self.selfsleep)

            decision = self.get_input("Would you like to hit or stand?", ["Hit", "Stand"], None, False)
                    
            while total < 21 and decision == "Hit":
                card = random.choice(cards)
                value = values[card]
                if card == "A" and total <= 10:
                    value = 11
                total = total + value
                player_cards.append(card)
                self.write(f"you got a {card}")
                self.write()
                self.write(" ".join(player_cards))
                self.write()
                self.write(f"your total is {total}")
                if total < 21:
                    decision = self.get_input("Would you like to hit or stand?", ["Hit", "Stand"], None, False)

            if decision == "Stand":
                self.delete()
            else:
                self.wait_for_key_press()
                self.delete()
                
            while opponent_total < 17:
                opponent = random.choice(cards)
                opponent_value = values[opponent]
                if opponent == "A" and opponent_total <= 10:
                    opponent_value = 11
                opponent_total = opponent_total + opponent_value
            
            if total == opponent_total:
                self.write(f"Your opponent also got {total}, its a draw")
                self.sleep(self.selfsleep)
                self.write()
                self.write(f"You got back {bet} runes")
                
            elif total > 21:
                if opponent_total > total:
                    self.write(f"Your opponent got {opponent_total}, its a draw")
                    self.sleep(self.selfsleep)
                    self.write()
                    self.write(f"You got back {bet} runes")
    
                elif opponent_total <= 21:
                    self.write(f"Your opponent got {opponent_total}, you lost")
                    self.sleep(self.selfsleep)
                    self.write()
                    self.write_color(f"You lose {bet} runes", "red")
                    self.player.money -= int(bet)

            else: 
                if opponent_total > 21 or (total > opponent_total):
                    self.write(f"Your opponent got {opponent_total}, you won")
                    self.sleep(self.selfsleep)
                    self.write()
                    self.write_color(f"You win {bet} runes", "green")
                    self.player.money += int(bet)
    
                else:
                    self.write(f"Your opponent got {opponent_total}, you lost")
                    self.sleep(self.selfsleep)
                    self.write()
                    self.write_color(f"You lose {bet} runes", "red")
                    self.player.money -= int(bet)

            self.write()
            choice = self.get_input("Do you want to play again?", ["Yes", "No"], None, False)
            self.delete()
            if choice == "Yes":
                self.play()
                
class Slots(Game):
    def __init__(self, player, root, text):
        super().__init__()
        self.root = root
        self.text = text
        self.player = player
        self.pause_var = tk.StringVar()
        self.pointer = tk.IntVar()
        self.sleepCount = tk.IntVar()

    def play(self):
        bet = self.get_bet()

        if bet == "Cancel":
            self.delete()
            
        else:
            number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            for i in range(20):
                self.write(f"{random.choice(number)} {random.choice(number)} {random.choice(number)}")
                self.sleep(0.1)
                self.delete()
            number1 = random.choice(number)
            
            for i in range(20):
                self.write(f"{number1} {random.choice(number)} {random.choice(number)}")
                self.sleep(0.1)
                self.delete()
                
            luck1 = random.randint(1, 2)
            if luck1 == 1:
                for i in range(20):
                    self.write(f"{number1} {number1} {random.choice(number)}")
                    self.sleep(0.1)
                    self.delete()
                luck2 = random.randint(1, 3)
                if luck2 == 1:
                    self.write(f"{number1} {number1} {number1}")
                    self.write()
                    self.write_color(f"You win {int(bet)*2} runes", "green")
                    self.player.money += int(bet)*2
                else:
                    number2 = random.choice(number)
                    while number2 == number1:
                        number2 = random.choice(number)
                    self.write(f"{number1} {number1} {number2}")
                    self.write()
                    self.write_color(f"You lose {bet} runes", "red")
                    self.player.money -= int(bet)
            else:
                number2 = random.choice(number)
                while number2 == number1:
                    number2 = random.choice(number)
                for i in range(20):
                    self.write(f"{number1} {number2} {random.choice(number)}")
                    self.sleep(0.1)
                    self.delete()
                self.write(f"{number1} {number2} {random.choice(number)}")
                self.write()
                self.write_color(f"You lose {bet} runes", "red")
                self.player.money -= int(bet)
                
            self.write()
            choice = self.get_input("Do you want to play again?", ["Yes", "No"], None, False)
            self.delete()
            if choice == "Yes":
                self.play()     