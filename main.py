from flask import Flask
from flask import request
import os
import time
import datetime
current = "0"

app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name", "")
    date = request.args.get("date", "")
    mode = request.args.get("mode", "0")
    out = ""
    if name and date:
        out = schedule(name, date)
    return ("""<style>
    table{width:fit-content;border-collapse: collapse;margin:auto;margin-top: 10px;}
    td,th{margin-left: auto;
  margin-right: auto;}
    td{height:5rem;border: 1px solid white; padding:10px; margin: 10px;}
    th{height:5rem;border: 3px solid white; padding:10px;font-size:1.2rem;font-weight:bold;}""" + str(change(mode)) + 
    """</style>
<span style="font-size: 18px;">
<h1><p style="font-family: courier">SST MTR Schedule Fetcher</p></h1>
<p style="font-family: courier">Enter your name to get a list of all matching entries.
        For exact matches, enter as seen in class register.</p>""" + "<br>" +
        """<form action="" method="get">
                <input type="text" name="name"
                style="height:60px; width:500px; font-size:20px;" type="numeric">
                <select name="date" id="date"
                style="height:60px; width:200px; font-size:20px;" type="numeric">
                  <option value="Today">Today</option>
                  <option value="11 Aug">11 Aug</option>
                  <option value="12 Aug">12 Aug</option>
                </select>
                <input type="submit" value="Enter" style="height:60px; width:200px; font-size:20px;"><br><br>
                <input type="checkbox" id="mode" name="mode" value = "1" style="height:20px; width:20px">
                <label for="mode"><p style="font-family: courier">Toggle Dark mode</p></label>
              </form><p style="font-family: courier">
              """ + str(out) +
            """</p><p style="font-family: courier"><br>
Only schedules for 11 Aug and 12 Aug are implemented.<br>
github link: https://github.com/awpgikxdigj/MTRSchedule<br><br>
Made by Ethan Tse Chun Lam, S407 (objectively better computing class)<br>
Dark theme by Jerick Seng, S401 (L take)</p>""")

def change(mode):
    global current
    if mode == "0":
        return darkmode(current)
    elif mode == "1":
        if current == "0":
            current = "1"
        elif current == "1":
            current = "0"
        return darkmode(current)

def darkmode(mode):
    if mode == "0":
        return ""
    elif mode == "1":
        return """body{background: #000000; color:#ffffff}
    input,select{background:#444444;color:#ffffff}"""

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
                    message += "'s schedule on " + date[1:] + "</b><br><br>"
                    for a in range(len(out[b])):
                        message += str(times[a][:-4]) + ": " + str(out[b][a][0])
                        if out[b][a][1] != " ":
                            message += " (" + out[b][a][1] + ")<br>"
                        else:
                            message += "<br>"
                        message += "<br>"
        return message
    except ValueError:
        return "schedule not found"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
