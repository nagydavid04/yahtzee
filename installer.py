from ftplib import FTP
import os


def list_dir():
    files = server.nlst()

    files.remove(".")
    files.remove("..")

    return files


server = FTP("ftp.sci-soft.eu", "sci-soft.eu", "nagyzoliftp")
server.cwd("yahtzee")

server.cwd("versions")
files = list_dir()
new_version = float(files[-1].replace("yahtzee_", "").replace(".exe", ""))
server.retrbinary(f"RETR {files[-1]}", open(f"yahtzee_{new_version}.exe", "wb").write)

server.cwd("..")
server.cwd("datas")
server.cwd("pictures")

os.mkdir("datas")
open("datas/leaderboard.txt", "w")
open("datas/savedgame.txt", "w")

os.mkdir("datas/pictures")
filenames = list_dir()

for filename in filenames:
    server.retrbinary(f"RETR {filename}", open(f"datas/pictures/{filename}", "wb").write)

server.quit()



