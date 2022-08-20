from flask import Flask, render_template
from flask import request
from difflib import SequenceMatcher
import os
import time
import datetime
mode = "light"

app = Flask(__name__)

@app.route("/")
def index():
    req = request.full_path
    name = ""
    date = ""
    global mode
    if "&" in req:
        req = req.split("&")
        name = req[0].split("=")[1]
        date = req[1].split("=")[1].replace("+", " ")
        mode = req[2].split("=")[1]
    out = ""
    if name and date:
        out = schedule(name, date)
    return render_template("index.html", out = out, mode = mode, date = date)

@app.route("/lesson<lesson>")
def shownames(lesson):
    global mode
    lesson = lesson.replace("|", "/")
    directory = os.getcwd() + "/data"
    lesson = lesson.replace("%20", " ")
    lesson= [lesson[:lesson.index(":")], lesson[lesson.index(":")+1:]]
    lesson[1] = lesson[1].split("█")
    date = lesson[1][1]
    if date == "Today":
        temp = int(str(datetime.datetime.fromtimestamp(int(time.time()+28800))).split()[0].split("-")[2])
        if temp not in [11, 12, 15, 16, 17, 18, 19]:
            message = [["No schedule for Aug " + str(temp)]]
            return message
        else:
            date = str(int(temp)) + " Aug"
    f = open(directory + "/dates" + "/" + date + "/" + lesson[0] + ".txt", "r")
    classes = f.readlines()
    f.close()
    lesson[1][0] = lesson[1][0].strip()
    inter = []
    for a in classes:
        details = a.split("█")
        if lesson[1][0] == (details[0] + " (" + details[1] + ")"):
            inter = details[2].strip().split("|")
    for a in range(1, 9):
        inter.append("S40" + str(a))
    f = open(directory + "/namelist.txt", "r")
    out = f.readlines()
    f.close()
    removel = []
    for a in out:
        if a.strip() not in inter:
            removel.append(a)
    for a in removel:
        out.remove(a)
    for a in range(len(out)):
        temp = out[a].strip().split()
        new = ""
        for b in temp:
            new += b.capitalize()
            if b == temp[-1]:
                pass
            else:
                new += " "
        out[a] = new
    return render_template("names.html", out = out, lesson = lesson, mode = mode)

def schedule(name, date):
    directory = os.getcwd() + "/data"
    f = open(os.path.join(directory, "datelist.txt"), "r")
    dates = f.readlines()
    f.close()
    f = open(os.path.join(directory, "namelist.txt"), "r")
    fullnames = f.readlines()
    f.close()
    try:
        if date == "Today":
            temp = int(str(datetime.datetime.fromtimestamp(int(time.time()+28800))).split()[0].split("-")[2])
            if temp not in [11, 12, 15, 16, 17, 18, 19]:
                message = [["No schedule for Aug " + str(temp)]]
                return message
            else:
                date = "/" + str(int(temp)) + " Aug"
        else:
            date = "/" + date
        name = name.lower().replace("+", " ").replace("%2c", ",")
        picknames = []
        for b in fullnames:
            if len(b) == 4:
                pass
            elif name in b:
                picknames.append(b.strip())
        name = name.split()
        for b in fullnames:
            c = b.split()
            for a in name:
                if a not in c:
                    break
            else:
                if b.strip() not in picknames:
                    picknames.append(b.strip())
        
        times = sorted(os.listdir(directory + "/dates" + date))
        if ".DS_Store" in times:
            times.remove(".DS_Store")
        out = []
        for c in picknames:
            intout = []
            for a in times:
                f = open(directory + "/dates" + date + "/" + a, "r")
                classes = f.readlines()
                for b in classes:
                    details = b.split("█")
                    names = details[2].strip().split("|")
                    if c in names:
                        intout.append([details[0], details[1]])
                        break
                else:
                    intout.append(["no class found", "sorry"])
            out.append(intout)
        schedules = []
        if len(out) == 0:
            return [["Schedule not found"]]
        else:
            for b in range(len(out)):
                current = []
                line = ""
                if len(out[b]) == 0:
                    pass
                else:
                    fragname = picknames[b].split()
                    for x in fragname:
                        line += x.capitalize()
                        if x == fragname[-1]:
                            pass
                        else:
                            line += " "
                    line += "'s schedule on " + date[1:]
                    current.append(line)
                    for a in range(len(out[b])):
                        line = ""
                        line += str(times[a][:-4]) + ": " + str(out[b][a][0])
                        if out[b][a][1] != " ":
                            line += " (" + out[b][a][1] + ")"
                        current.append(line)
                schedules.append(current)
        return schedules
    except ValueError:
        return [["Schedule not found"]]

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
