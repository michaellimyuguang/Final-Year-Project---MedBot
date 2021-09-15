# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from g2p_en import G2p

texts = ["WARD",
         "A",
         "B",
         "C",
         "BED", 
         "1",
         "2",
         "3",
         "4",
         "5"
         ]
g2p = G2p()
for text in texts:
    out = g2p(text)
    #print(out)
    print(text,' '.join(out))
