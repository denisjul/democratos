# -*- coding: utf-8 -*-

""" contains classes to transform Html Table to ascii table
Printable with python print() """
try:
    from functions import remove_piece_of_text
except:
    from CreateYourLaws.dl_law_codes.functions import remove_piece_of_text

LIST_OF_CHANGE = [('<sup>', ''),
                  ('</sup>', ''),
                  ('<br clear="none"/>', ''),
                  (' align="left"', ''),
                  (' align="right"', ''),
                  (' align="center"', ''),
                  (' align="justify"', ''),
                  (' vAlign="top"', ''),
                  (' vAlign="middle"', ''),
                  (' vAlign="bottom"', ''),
                  ('<p>', ''),
                  ('<b>', ''),
                  ('</b>', ''),
                  ('<br/>', ''),
                  ('</p>', ''),
                  ('<p/>', ''),
                  (' colspan="1"', ''),
                  (' rowspan="1"', ''),
                  (' colspan=1', ''),
                  (' rowspan=1', ''),
                  ('&gt;', '>'),
                  ('&lt;', '<'),
                  ('colSpan="', 'colspan='),
                  ('rowSpan="', 'rowspan='),
                  ('colspan="', 'colspan='),
                  ('rowspan="', 'rowspan='),
                  ('colSpan=', 'colspan='),
                  ('rowSpan=', 'rowspan='),
                  ('<tbody>\n', ''),
                  ('</tbody>\n', ''),
                  ]

LIST_OF_DEL = [(' width=', '>', '/')
               ]


class Table():
    # table in ascii
    def __init__(self, html):
        self.html = self._prepare_html(html)

    def _prepare_html(self, text):
        """ remove all the text parts which bother dashtable.py
        See LIST_OF_CHANGE
        """
        buf = ""
        buf2 = ""
        i = 0
        while i < len(text):
            buf += text[i]
            if len(buf) == 9:
                if buf == 'colSpan="' or buf == 'rowSpan="':
                    while buf2 != '"':
                        i += 1
                        buf2 = text[i]
                    text = text[0:i] + text[i + 1:len(text)]
                    buf2 = ""
                buf = buf[1:9]
            i += 1
        for i in range(len(LIST_OF_DEL)):
            try:
                text = remove_piece_of_text(text,
                                            LIST_OF_DEL[i][0],
                                            LIST_OF_DEL[i][1],
                                            LIST_OF_DEL[i][2])
            except:
                text = remove_piece_of_text(text,
                                            LIST_OF_DEL[i][0],
                                            LIST_OF_DEL[i][1])
        for i in range(len(LIST_OF_CHANGE)):
            text = text.replace(LIST_OF_CHANGE[i][0], LIST_OF_CHANGE[i][1])
        return text
