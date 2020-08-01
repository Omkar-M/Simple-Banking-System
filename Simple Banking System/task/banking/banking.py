from random import randint
import sqlite3


class Bank:
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0);''')
        self.conn.commit()

    def create(self):
        print()
        card = self.create_card()
        pin = str.zfill(str(randint(0000, 9999)), 4)
        print(f'Your card has been created\nYour card number:\n{int(card)}\nYour card PIN:\n{pin}\n')
        bal = 0
        self.cur.execute(f'INSERT INTO card (number,pin,balance) VALUES ({card},{pin},{bal})')
        self.conn.commit()
        return self.menu()

    def login(self):
        print('\nEnter your card number:')
        card = input()
        print('Enter your PIN:')
        pin = input()
        list_cards = [x[0] for x in self.cur.execute('SELECT number FROM card')]
        if Bank.check_account(card, list_cards):
            print('Bank.check_account(card, list_cards)')
            if self.check_pin(pin, card):
                print('self.check_pin(pin,card)')
                print('\nYou have successfully logged in!\n')
                return self.account_menu(card)
                pass
        print('\nWrong card number or Pin!\n')
        return self.menu()

    @staticmethod
    def create_card():
        test_card = '400000' + str.zfill(str(randint(000000000, 999999999)), 9)
        test_card += str(Bank.check_sum(test_card))
        return test_card

    @staticmethod
    def check_sum(test_card1):
        sum_of_digits1 = 0
        for x in range(len(test_card1)):
            if x == len(test_card1):
                continue
            digit = int(test_card1[x])
            if x % 2 == 0:
                digit *= 2
            if digit > 9:
                digit -= 9
            sum_of_digits1 += digit
        return 10 - sum_of_digits1 % 10 if sum_of_digits1 % 10 > 0 else 0

    @staticmethod
    def check_luhn(card_number):
        last_digital = card_number[-1]
        card_number = card_number[:-1]
        sum_odd = 0
        for x in range(0, 15, 2):
            k = int(card_number[x]) * 2
            if k > 9:
                sum_odd += (k // 10 + k % 10)
            else:
                sum_odd += k
        sum_even = 0
        for y in range(1, 14, 2):
            sum_even += int(card_number[y])
        if last_digital == str((sum_odd + sum_even) % 10) == "0":
            return True
        elif last_digital == str(10 - (sum_odd + sum_even) % 10):
            return True
        return False

    @staticmethod
    def check_account(card1, list_cards1):
        print(card1 in list_cards1)
        if card1 in list_cards1:
            return True
        return False

    def check_pin(self, pin1, card):
        self.cur.execute(f'SELECT pin FROM card WHERE number ={card}')
        pin = ''.join(self.cur.fetchone())
        if pin == pin1:
            print(pin1)
            return True
        return False

    def balance(self, card):
        self.cur.execute(F'SELECT balance FROM card WHERE number = {card}')
        money = self.cur.fetchone()
        print(f'\nBalance: {money[0]}\n')
        return self.account_menu(card)

    def add_income(self, card):
        print('\nEnter income:')
        value = int(input())
        self.cur.execute(f'UPDATE card SET balance = balance + {value} WHERE number = {card}')
        self.conn.commit()
        print('Income was added!')
        self.balance(card)
        return self.account_menu(card)

    def card_in_db(self, transfer_card):
        list_cards = [x[0] for x in self.cur.execute("SELECT number FROM card")]
        if transfer_card in list_cards:
            return True
        return False

    def transfer(self, card):
        print('\nTransfer\nEnter card number:')
        transfer_card = input()
        self.cur.execute('SELECT number FROM card ')
        if card == transfer_card:
            print("You can't transfer money to the same account!")
            return self.account_menu(card)
        if not Bank.check_luhn(transfer_card):
            print('Probably you made mistake in the card number. Please try again!')
            return self.account_menu(card)
        elif not self.card_in_db(transfer_card):
            print('Such a card does not exist.')
            return self.account_menu(card)
        else:
            money = int(input('Enter how much money you want to transfer:'))
            self.cur.execute(f'SELECT balance FROM card WHERE number = {card}')
            money_from_card = [int(i[0]) for i in self.cur.fetchall()]
            if money > money_from_card[0]:
                print('Not enough money!')
                self.account_menu(card)
            self.cur.execute(f"UPDATE card SET balance=balance+{money} WHERE number={transfer_card}")
            self.cur.execute(f"UPDATE card SET balance=balance-{money} WHERE number={card}")
            self.conn.commit()
            print('Success!')
            self.account_menu(card)

    def close_acc(self, card_number):
        self.cur.execute(f'DELETE FROM card WHERE number={card_number}')
        self.conn.commit()
        return self.menu()

    def menu(self):
        print('1. Create an account\n2. Log into account\n0. Exit')
        choice = input()
        if choice == '1':
            self.create()
        elif choice == '2':
            self.login()
        elif choice == '0':
            print('\nBye!')
            quit()

    def account_menu(self, card):
        print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
        choice = input()
        if choice == '1':
            self.balance(card)
        elif choice == '2':
            self.add_income(card)
        elif choice == '3':
            self.transfer(card)
        elif choice == '4':
            self.close_acc(card)
        elif choice == '5':
            print('\nYou have successfully logged out!\n')
            return self.menu()
        elif choice == '0':
            print('\nBye!')
            exit()


if __name__ == '__main__':
    stage_1 = Bank()
    while True:
        stage_1.menu()
