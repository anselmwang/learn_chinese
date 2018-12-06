import requests

def download_image(image_url, image_path):
    import shutil
    import requests
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        with open(image_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def get_image(subscription_key, word, output_dir):
    assert subscription_key
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    search_term = "%s drawing" % word
    #print(search_term)
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "license": "public"}
    #print(params)
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:16]]

    file_list = []
    for i in range(1):
        time.sleep(0.5)
        file_name = r"english_%s_%s.jpg" % (word, i)
        file_list.append(file_name)
        download_image(thumbnail_urls[i], path.join(output_dir, "images/" + file_name))

    return file_list

import os
import os.path as path
import time
import anki_conn

OUTPUT_DIR = r"c:\temp\learn_english"

subscription_key = os.environ["BING_SUBSCRIPTION_KEY"]

result = anki_conn.query("findNotes", {"query": "deck:'C凌君英文'"})
notes = result["result"]
result = anki_conn.query("notesInfo", {"notes": notes})
with open(path.join(OUTPUT_DIR, "note.txt"), "w", encoding="utf-8") as out_f:
    for x in result["result"]:
        x = x["fields"]
        assert x["english"]["order"] == 0
        assert x["chinese"]["order"] == 1
        assert x["image"]["order"] == 2
        english = x["english"]["value"]
        chinese = x["chinese"]["value"]
        image = x["image"]["value"]
        if image.strip() == "":
            image = "<BR>".join(['<img src="%s" />' % file_name for file_name in get_image(subscription_key, english, OUTPUT_DIR)])
            out_f.write("%s\t%s\t%s\n" % (english, chinese, image))







