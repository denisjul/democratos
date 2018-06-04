from difflib import SequenceMatcher  # , HtmlDiff
from html.parser import HTMLParser
from html.entities import name2codepoint
# from bs4 import BeautifulSoup

text = """
<p class="title">
    <b>
        The Dormouse's <br> story
    </b>
</p>
<p class="story">
    Once upon a time there were three little sisters; and their names were
    <a class="sister" href="http://example.com/elsie" id="link1">
        Elsie
    </a>
    ,
    <a class="sister" href="http://example.com/lacie" id="link2">
        Lacie
    </a>
    and
    <a class="sister" href="http://example.com/tillie" id="link2">
        Tillie
    </a>
    ; and they lived at the bottom of a well.
</p>
<p class="story">
 ...
</p>
"""

text2  = """
<p class="title">
    <b>
        The Dormouse's <br> story
    </b>
</p>
<p class="story">
    Once upon a time there were three little sisters; and their names were
    <a class="sister" href="http://example.com/elsie" id="link1">
        Elsie
    </a>
    ,
    <a class="sister" href="http://example.com/lacie" id="link2">
        Lacie
    </a>
    and
    <a class="sister" href="http://example.com/tillie" id="link2">
        Tillie
    </a>
    ; and they lived at the bottom of a well.
</p>
<p class="story">
 ...
</p>
"""
"""
soup = BeautifulSoup(text, "html5lib")
for p in soup.find_all('a'):
    print(p)
"""


class SavedHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = []
        self.Data = ""

    def handle_starttag(self, tag, attrs):
        data = "<" + tag
        for attr in attrs:
            data += ' ' + attr[0] + '="' + attr[1] + '"'
        data += ">"
        self.content.append(("start", data))

    def handle_endtag(self, tag):
        self.content.append(("end", "</" + tag + ">"))
        # print("End tag  :", tag)

    def handle_data(self, data):
        data = data.split(" ")
        for el in data:
            self.content.append(("data", el))
        # print("Data     :", data)

    def handle_comment(self, data):
        self.content.append(data)
        print("Comment  :", data)

    def unknow_decl(self, data):
        print("Decl     :", data)


TestParser = SavedHTMLParser()
TestParser.feed(text)
print(TestParser.content)

data1 = ["Once","upon","a","time","there","were","three","little", "cochon", "sisters", "maison", "vertes", "mais", "pas", "red", "&blue"]
data2 = ["Once","upon","an", "time", "very", "long","there","were","three","very", "pretty", "little", "cochonnes", "sisters", "maisons", "sans","vitres", "red"]


def DataCompare(data1, data2):
    SeqMatch = SequenceMatcher()
    SeqMatch.set_seqs(data1, data2)
    Commit = []
    for el in SeqMatch.get_opcodes():
        comlist = list(el)
        if el[0] == "equal":
            comlist.extend(["", ""])
        else:
            joiner = " "
            old = joiner.join(data1[el[1]:el[2]])
            new = joiner.join(data2[el[3]:el[4]])
            comlist.extend([old, new])
        if comlist[0] == "replace":
            s = SequenceMatcher()
            s.set_seqs(comlist[5], comlist[6])
            if s.ratio() >= 0.8:
                comlist[0] = "close"
                subcommit = []
                for el2 in s.get_opcodes():
                    subcomlist = list(el2)
                    if el2[0] == "equal":
                        subcomlist.extend([comlist[5][el2[1]:el2[2]],
                                           comlist[6][el2[3]:el2[4]]])
                    else:
                        subold = comlist[5][el2[1]:el2[2]]
                        subnew = comlist[6][el2[3]:el2[4]]
                        subcomlist.extend([subold, subnew])
                    subcommit.append(subcomlist)
                comlist[5] = subcommit
                comlist[6] = ""
        Commit.append(comlist)
    return Commit


Commit = DataCompare(data1, data2)
# print(Commit)
