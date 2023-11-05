import json
import xml.etree.ElementTree as ET

import requests
from pygtrans import Translate
import time

if __name__ == '__main__':
    tree1 = ET.parse('strings.xml')
    root1 = tree1.getroot()
    client = Translate(proxies={'https': 'http://localhost:7890'})
    lan_list=["en"]
    # lan_list=["en","ar","hi","phi","ru"]
    for lanitem in lan_list:
        other_result = ET.parse('strings-%s.xml'%lanitem)
        root = ET.Element("resources")
        root2 = other_result.getroot()
        for item in root1:
            is_translate=False
            for item_result in root2:
                old_key = item_result.get("name")
                if old_key == item.get("name"):
                    root.append(item_result)
                    is_translate=True
                    break
            print(is_translate)
            time.sleep(0.3)
            if  is_translate==False:
                text = client.translate(target=lanitem, source="zh",q=item.text)
                folder = ET.SubElement(root, "string")
                item_name = item.get("name")
                folder.set("name", item_name)
                folder.text= text.translatedText
                print(text.translatedText)
        tree = ET.ElementTree(root)
        tree.write("strings-%s.xml"%lanitem, encoding="utf-8")

