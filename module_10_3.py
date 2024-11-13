from threading import Thread
from threading import Lock
from random import randint
from time import sleep


class Bank:

    def __init__(self, balance=0):

        self.balance = balance
        self.lock = Lock()

    def deposit(self):

        self.lock.acquire()

        for i_elem in range(100):

            sum_deposit = randint(50, 500)
            self.balance += sum_deposit
            print(f'Пополнение: {sum_deposit}. Баланс: {self.balance}')

            if self.balance >= 500 and self.lock.locked():
                self.lock.release()

            sleep(0.001)

        if self.lock.locked():
            self.lock.release()

    def take(self):

        for i_elem in range(100):

            sum_take = randint(50, 500)
            print(f'Запрос на {sum_take}')

            if sum_take > self.balance:
                print(f'Запрос отклонен, недостаточно средств')
                self.lock.acquire()
            else:
                self.balance -= sum_take
                print(f'Снятие: {sum_take}. Баланс: {self.balance}')

        if self.lock.locked():
            self.lock.release()


bk = Bank()

thread1 = Thread(target=bk.deposit)
thread2 = Thread(target=bk.take)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

print(f'Итоговый баланс: {bk.balance}')