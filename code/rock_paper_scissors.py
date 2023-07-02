from fpioa_manager import fm
from Maix import GPIO
import utime
import random

while(True):
        X = str(input("SCISSORS, ROCK, PAPPER 중에 하나를 선택하여 적으세요 :"))
        list = ["SCISSORS", "ROCK", "PAPPER"]
        Y = random.choice(list)
        print("내가 낸 것?", X, "\n컴퓨터가 낸 것?", Y)
        if X == "SCISSORS":
            if Y == "SCISSORS":
                print("무승부")
            elif Y == "ROCK":
                 print("나의 패배!")
            else:
                print("나의 승리!")
        if X == "ROCK":
            if Y == "ROCK":
                print("무승부")
            elif Y == "PAPPER":
                 print("나의 패배!")
            else:
                print("나의 승리!")
        if X == "PAPPER":
            if Y == "PAPPER":
                print("무승부")
            elif Y == "SCISSORS":
                 print("나의 패배!")
            else:
                print("나의 승리!")

