from colorama import Fore, Style

class Logger():
    def info(self, string):
        print(Style.DIM+string+Style.RESET_ALL)
    def message(self, string):
        print(Fore.CYAN+string+Fore.RESET)
    def error(self, string):
        print(Fore.RED+string+Style.RESET_ALL)
    def success(self, string):
        print(Fore.GREEN+string+Fore.RESET)
