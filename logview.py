import os
import json
from subprocess import call

cdir = os.path.dirname(os.path.realpath(__file__))
EDITOR = os.environ.get("EDITOR", "vim")

class miniconfig:
    def __init__(self):
        self.name = "logviewer.conf"
        self.dir = cdir
        self.table = {}

    def save(self):
        with open(os.path.join(self.dir, self.name), "w") as dosya:
            json.dump(self.table, dosya)

    def load(self):
        if not os.path.exists(os.path.join(self.dir, self.name)):
            return False

        with open(os.path.join(self.dir, self.name), "r") as dosya:
            self.table = json.load(dosya)

        return True

class viewer:
    def __init__(self):
        self.config = miniconfig()
        self.path = False
        self.recursive_results = []

    def recursive_search(self, path):
        pathlist = os.listdir(path)
        pathdirs = [c for c in pathlist if os.path.isdir(os.path.join(path, c))]
        if "AtljLog" in pathdirs:
            self.recursive_results.append(os.path.join(path, "AtljLog"))
            pathdirs.remove("AtljLog")

        if pathdirs == []:
            return 0

        else:
            for subdir in pathdirs:
                self.recursive_search(os.path.join(path, subdir))
                
            return 0


    def filechooser(self):
        print("1)Kodun Bulundugu Dizinde AtljLog dizini ara\n2)logs dizini el ile gir")
        while 1:
            inp = input(">>")
            
            if inp == "1":
                self.recursive_results = []
                self.recursive_search(cdir)
                if self.recursive_results == []:
                    print("Kodun Bulundugu Dizinde ve Altdizinlerinde Herhangi Bir AtljLog Dizinine Rastlanmadi")
                    continue

                else:
                    text = "1)Aradigim Dizin Bunlardan Biri Degil\n"
                    idx_list = ["1"]
                    self.recursive_results = sorted(self.recursive_results, key=lambda x: len(x))
                    idx = 2
                    for result in self.recursive_results:
                        idx_list.append(str(idx))
                        text += str(idx)+")" + result + "\n"
                        idx += 1

                    print(text)
                    while 1:
                        inp = input(">>")
                        if not inp in idx_list:
                            continue

                        if inp == "1":
                            print("Programdan Cikiliyor")
                            os._exit(0)

                        self.path = self.recursive_results[int(inp)-2]
                        return True

            if inp == "2":
                print("Lutfen Dizin Yolunu Giriniz")
                while 1:
                    inp = input(">>")
                    if not os.path.isdir(inp):
                        print("Bu yollu bir dizin bulunamadi")
                        continue
                    self.path = inp
                    break

                return True
                    

    def choose(self):
        case = {}
        files = [c for c in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, c))]
        files = [c for c in files if c.split(".")[-1] == "log"]
        idx = 1
        files.reverse()
        if os.path.exists(os.path.join(self.path, ".lastlog")):
            with open(os.path.join(self.path, ".lastlog"), "r") as dosya:
                last = dosya.read()

            case["1"] = last
            files.remove(last)
            idx += 1
        
        for element in files:
            case[str(idx)] = element
            idx += 1

        text = "Lutfen Bir Dosya Seciniz\n"
        for c in case:
            text += c+")"+case[c]+"\n"

        print(text)
        while 1:
            inp = input(">>")
            if not inp in case:
                continue

            self.file = os.path.join(self.path, case[inp])
            break
    
        return True

    def open_with_vim(self):
        call([EDITOR, self.file])


    def open_file(self):
        print("Log:"+self.file+"\n\n1)Vim ile ac\n2)Internal Editor\n3)Baska Bir Log Sec\n4)Cikis Yap")
        while 1:
            inp = input(">>")
            if inp == "1":
                self.open_with_vim()

            if inp == "3":
                self.choose()
                print("Log:"+self.file+"\n\n1)Vim ile ac\n2)Internal Editor\n3)Baska Bir Log Sec\n4)Cikis Yap")

            if inp == "4":
                print("Cikis Yapiliyor")
                os._exit(0)




    def startup(self):
        print("Merhaba ve Hosgeldin!")
        print("1)Log dizinini .conf dosyasindan cek\n2)Yeni bir Log dizini belirt")
        while 1:
            inp = input(">>")
            if inp == "1":
                if self.config.load():
                    self.path = self.config.table["path"]
                    break
                else:
                    print("herhangi bir conf dosyasi bulunamadi")
                    continue

            if inp == "2":
                self.filechooser()
                self.config.table["path"] = self.path
                self.config.save()
                break

        self.choose()
        self.open_file()

obj = viewer()
try:
    obj.startup()

except KeyboardInterrupt:
    print("Cikis Yapiliyor")
    os._exit(0)

except EOFError:
    print("Cikis Yapiliyor")
    os._exit(0)
        

