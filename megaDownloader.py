from mega import Mega
import time
import subprocess
import os

def folderExtractor(link):
    try:
        if os.path.exists('mega-account.txt'):
            file = open('mega-account.txt', 'r')
            lines=file.readlines()
            lines = lines[0].split(":")

            email = lines[0]
            password = lines[1]
        else:
            email = input("Enter your Mega Email:\t")
            password = input("Enter your password:\t")
            file = open('mega-account.txt', 'w')
            file.write(email+":"+password)
        file.close()

        result = subprocess.run("MEGAcmd\\mega-login.bat {0} {1}".format(email,password))
        folderName = subprocess.run("MEGAcmd\\mega-import.bat "+str(link), capture_output=True, text=True)
        folderName = folderName.stdout.strip()
        subprocess.run("MEGAcmd\\mega-logout.bat")
        output = folderName.split("/")
        print(output[1])
        folderName = output[1]


        print("Extracting Links.... ")
        time.sleep(5)

        mega = Mega()

        m = mega.login(email, password)

        folder = m.find(folderName)[0]
        files = m.get_files_in_node(folder)

        print("There are " + str(len(files)) + " files")
        index = 1
        links = []
        for file in list(files.items()):
            links.append(m.get_link(file))
            print(str(index) + " links has been retrieved.")
            index+=1
            time.sleep(5)

        file = open('mega.txt', 'w')
        for link in links:
            file.write(link+"\n")
        file.close()


    except IndexError:
        print("Probably your Mega Storage is full. Empty it to import files and extract their links")
    except:
        print("Something went wrong with downloading a mega folder")
