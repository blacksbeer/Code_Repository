# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 15:12:17 2024

@author: black
"""

import json

config = {'url':'http://rx.manysplendid.com.tw/rfd-grid',
          'output_folder': "output\\",
          'location':[[120.8375, 22.1875],
                      [120.8000, 22.1875],
                      [120.8125, 22.1500],
                      [120.7750, 22.1500]]
          }

with open(r"config.json", "w", encoding='utf-8') as outfile:
    json.dump(config, outfile, indent=3, ensure_ascii=False)
