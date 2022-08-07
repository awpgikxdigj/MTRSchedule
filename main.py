from flask import Flask
from flask import request
import os
from datetime import date as day

app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name", "")
    date = request.args.get("date", "")
    out = ""
    if name and date:
        out = schedule(name, date)
    return ("""
    <style>
    table{width:fit-content;border-collapse: collapse;margin:auto;margin-top: 10px;}
    td,th{margin-left: auto;
  margin-right: auto;}
    td{height:5rem;border: 1px solid white; padding:10px; margin: 10px;}
    th{height:5rem;border: 3px solid white; padding:10px;font-size:1.2rem;font-weight:bold;}
    body{background: #000000; color:#ffffff}
    input,select{background:#444444;color:#ffffff}
    </style>
    <h1>SST MTR Schedule Fetcher</h1> Enter
        your name to get a list of all matching entries.
        For exact matches, enter as seen in class register.""" + "<br><br>" +
        """<form action="" method="get">
                <input type="text" name="name">
                <select name="date" id="date">
                  <option value="Today">Today</option>
                  <option value="11 Aug">11 Aug</option>
                  <option value="12 Aug">12 Aug</option>
                </select>
                <input type="submit" value="Enter">
              </form>""" + str(out) + """<br>Only schedules for 11 Aug and 12 Aug are implemented.<br> If you have any problems or find any bugs,
my discord is awpgikxdigj#8231<br><br>Made by Ethan Tse Chun Lam, S407 (objectively <s>better</s>worse computing class)""")

def schedule(name, date):
    directory = os.getcwd() + "/data"
    f = open(os.path.join(directory, "datelist.txt"), "r")
    dates = f.readlines()
    f.close()
    f = open(os.path.join(directory, "namelist.txt"), "r")
    fullnames = f.readlines()
    f.close()
    try:
        if date == "Today":# today is broken for me D:
            temp = str(day.today())
            temp = int(temp.split("-")[2])
            if temp not in [11, 12]:
                message = "No schedule for Aug " + temp
                return message
            else:
                date = "/" + str(int(temp)) + " Aug"
        else:
            date = "/" + date
        name = name.lower()
        picknames = []
        for b in fullnames:
            if name in b:
                picknames.append(b.strip())
        
        times = sorted(os.listdir(directory + "/dates" + date))
        if ".DS_Store" in times:
            times.remove(".DS_Store")
        out = []
        for c in picknames:
            intout = []
            for a in times:
                flag = len(intout)
                f = open(directory + "/dates" + date + "/" + a, "r")
                classes = f.readlines()
                for b in classes:
                    details = b.split("█")
                    names = details[2].strip().split("|")
                    if c in names:
                        intout.append([details[0], details[1]])
                        break
            out.append(intout)
        message = ""
        if len(out) == 0:
            message += "schedule not found"
        else:
            for b in range(len(out)):
                if len(out[b]) == 0:
                    pass
                else:
                    message += "<br><b>"
                    fragname = picknames[b].split()
                    for x in fragname:
                        message += x.capitalize()
                        if x == fragname[-1]:
                            pass
                        else:
                            message += " "
                    message += "'s schedule on " + date[1:] + "</b><br><br><table><tr><th>Timeslot</th><th>Lesson</th><th>Location</th></tr>"
                    for a in range(len(out[b])):

                        message += "<tr><td>"+str(times[a][:-4]) + "</td><td>" + str(out[b][a][0])+"</td>"
                        if out[b][a][1] != " ":
                            message += "<td>" + out[b][a][1] + "</td></tr>"
                        else:
                            message += "<td></td></tr>"
        return message
    except ValueError:
        return "schedule not found"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
