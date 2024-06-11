from calls import *
import sys
from termcolor import colored
banner = '''

██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗      
██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝      
██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗        
██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝        
╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗      
 ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝      
                                                                    
██╗   ██╗███╗   ██╗██╗      ██████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║   ██║████╗  ██║██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║██║     ██║   ██║██║     █████╔╝ █████╗  ██████╔╝
██║   ██║██║╚██╗██║██║     ██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚██████╔╝██║ ╚████║███████╗╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                     '''

def help():
        print(colored("\n================================HELP! HELP! HELP!=============================================\n","green"))
        print(colored("1)  list-supported           lists all supported hosts/streams/redirectors\n","green"))
        print(colored("2)  is-supported             checks by domain. if the website you're trying to download from is supported or not. e.g. youtube.com turbobit.cc\n","green"))
        print(colored("3)  single                   unlocks a single link and downloads the file in the current working directory. use this command for YouTube playlists","green"))
        print(colored("4)  multi                    unlocks multiple links and downloads their file(s) to the current working directory \n","green"))
        print(colored("\t\t\t\t NOTE:Before using the multi command, put all links in the links.txt file, a link in each line to proceed without errors.","green"))
        print(colored("5)  exit                     close the program\n","green"))


print(colored(banner,"red"))
print(colored("Developed by PirateOfEast\n", "light_magenta"))
help()

try:
        while True:
                prompt = input(colored(">>> ","light_yellow"))
                if prompt == '2':
                        checksupport()
                elif prompt == '1':
                        siteslist = supported()
                        siteslist.sort()
                        for site in siteslist:
                                print(site)
                        print("\n")
                        print("supports "+str(len(siteslist))+" websites")
                        print("\n")
                elif prompt == '3':
                        singlelink()
                elif prompt == '4':
                        multilink()
                elif prompt == '5':
                        print(colored("GOOD BYE!!","light_yellow"))
                        sys.exit()
                else:
                        help()

except KeyboardInterrupt:
        print(colored("Exit","red"))