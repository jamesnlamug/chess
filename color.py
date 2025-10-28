from colorama import Fore, Style

arr = []
arr.append(f"{Fore.BLACK} test")
arr.append(f"{Fore.RED} test")
arr.append(f"{Fore.GREEN} test")
arr.append(f"{Fore.YELLOW} test")
arr.append(f"{Fore.BLUE} test")
arr.append(f"{Fore.MAGENTA} test")
arr.append(f"{Fore.CYAN} test")
arr.append(f"{Fore.WHITE} test")
arr.append(f"{Fore.RESET} test")

for string in arr:
	print(string)

input()