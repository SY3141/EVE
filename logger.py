#logs messages - Currently unused

import pandas as pd  #removable if content logging is removed
from replit import db  #removable if content logging is removed
import schedule


def export():
  DBcolumns = [
    db["Channel"], db["ID"], db["Author"], db["Time"], db["Content"]
  ]
  print([len(x) for x in DBcolumns])
  maximum = max([len(x) for x in DBcolumns])
  for category in DBcolumns:
    while len(category) < maximum:
      category.append("NA")
  df = pd.DataFrame(data=DBcolumns).T
  df.to_csv("export.csv", encoding='utf-8', index=False)


def initDB():
  db["Channel"] = []
  db["ID"] = []
  db["Author"] = []
  db["Time"] = []
  db["Content"] = []


def contentLog(resp):
  msgContent = resp["content"]
  if not msgContent:  #ignores empty strings- including images
    return
  flags = ["https://", '<@']  #unwanted keywords
  for flag in flags:
    if flag in msgContent:
      return
  if "Content" not in db.keys():  #checks if database content is empty
    initDB()  #initializes database
  DBcolumns = [
    db["Channel"], db["ID"], db["Author"], db["Time"], db["Content"]
  ]
  lengths = list(map(len, DBcolumns))
  maxLen = max(lengths)
  for i in DBcolumns:
    while len(i) < maxLen:
      i.append("NA")
  db["Channel"].append(resp['channel_id'])
  db["ID"].append(resp['author']['id'])
  db["Author"].append(resp['author']['username'])
  db["Time"].append(resp['timestamp'])
  db["Content"].append(resp['content'])
  lengths = list(map(len, DBcolumns))


schedule.every(3).minutes.do(export)