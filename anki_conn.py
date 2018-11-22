import requests
import json

def query(action, params={}, version=6):
    r = requests.post('http://127.0.0.1:8765', data = json.dumps({
            "action": action,
            "version": 6,
            "params": params
        }))
    return r.json()

def get_learn_state_words(deck="Chinese"):
    result = query("findNotes",{"query": "deck:%s is:learn" % deck})
    notes = result["result"]
    result = query("notesInfo", { "notes": notes  })
    return [x['fields']["Front"]["value"] for x in result["result"]]

def complete_all_learn_state_words(deck="Chinese"):
    query("guiDeckReview", {"name": deck})
    for i in range(len(get_learn_state_words(deck))):
        query("guiShowAnswer")
        query("guiAnswerCard", {"ease": 2}) # 2nd button

