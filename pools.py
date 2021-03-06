from enum import Enum


class ItemType(Enum):
    Active = 1
    Passive = 2
    Familiar = 3
    Forbidden = -1


pill_colors_number = 0xD
pill_effects_number = 0x32

isaac_items = {
    1: ItemType.Passive,
    2: ItemType.Passive,
    3: ItemType.Passive,
    4: ItemType.Passive,
    5: ItemType.Passive,
    6: ItemType.Passive,
    7: ItemType.Passive,
    8: ItemType.Familiar,
    9: ItemType.Passive,
    10: ItemType.Familiar,
    11: ItemType.Familiar,
    12: ItemType.Passive,
    13: ItemType.Passive,
    14: ItemType.Passive,
    15: ItemType.Passive,
    16: ItemType.Passive,
    17: ItemType.Passive,
    18: ItemType.Passive,
    19: ItemType.Passive,
    20: ItemType.Passive,
    21: ItemType.Passive,
    22: ItemType.Passive,
    23: ItemType.Passive,
    24: ItemType.Passive,
    25: ItemType.Passive,
    26: ItemType.Passive,
    27: ItemType.Passive,
    28: ItemType.Passive,
    29: ItemType.Passive,
    30: ItemType.Passive,
    31: ItemType.Passive,
    32: ItemType.Passive,
    33: ItemType.Active,
    34: ItemType.Active,
    35: ItemType.Active,
    36: ItemType.Active,
    37: ItemType.Active,
    38: ItemType.Active,
    39: ItemType.Active,
    40: ItemType.Active,
    41: ItemType.Active,
    42: ItemType.Active,
    44: ItemType.Active,
    45: ItemType.Active,
    46: ItemType.Passive,
    47: ItemType.Active,
    48: ItemType.Passive,
    49: ItemType.Active,
    50: ItemType.Passive,
    51: ItemType.Passive,
    52: ItemType.Passive,
    53: ItemType.Passive,
    54: ItemType.Passive,
    55: ItemType.Passive,
    56: ItemType.Active,
    57: ItemType.Familiar,
    58: ItemType.Active,
    60: ItemType.Passive,
    62: ItemType.Passive,
    63: ItemType.Passive,
    64: ItemType.Passive,
    65: ItemType.Active,
    66: ItemType.Active,
    67: ItemType.Familiar,
    68: ItemType.Passive,
    69: ItemType.Passive,
    70: ItemType.Passive,
    71: ItemType.Passive,
    72: ItemType.Passive,
    73: ItemType.Familiar,
    74: ItemType.Passive,
    75: ItemType.Passive,
    76: ItemType.Passive,
    77: ItemType.Active,
    78: ItemType.Active,
    79: ItemType.Passive,
    80: ItemType.Passive,
    81: ItemType.Familiar,
    82: ItemType.Passive,
    83: ItemType.Active,
    84: ItemType.Active,
    85: ItemType.Active,
    86: ItemType.Active,
    87: ItemType.Passive,
    88: ItemType.Familiar,
    89: ItemType.Passive,
    90: ItemType.Passive,
    91: ItemType.Passive,
    92: ItemType.Passive,
    93: ItemType.Active,
    94: ItemType.Familiar,
    95: ItemType.Familiar,
    96: ItemType.Familiar,
    97: ItemType.Active,
    98: ItemType.Familiar,
    99: ItemType.Familiar,
    100: ItemType.Familiar,
    101: ItemType.Passive,
    102: ItemType.Active,
    103: ItemType.Passive,
    104: ItemType.Passive,
    105: ItemType.Active,
    106: ItemType.Passive,
    107: ItemType.Active,
    108: ItemType.Passive,
    109: ItemType.Passive,
    110: ItemType.Passive,
    111: ItemType.Active,
    112: ItemType.Familiar,
    113: ItemType.Familiar,
    114: ItemType.Passive,
    115: ItemType.Passive,
    116: ItemType.Passive,
    117: ItemType.Passive,
    118: ItemType.Passive,
    119: ItemType.Passive,
    120: ItemType.Passive,
    121: ItemType.Passive,
    122: ItemType.Passive,
    123: ItemType.Active,
    124: ItemType.Active,
    125: ItemType.Passive,
    126: ItemType.Active,
    127: ItemType.Active,
    128: ItemType.Familiar,
    129: ItemType.Passive,
    130: ItemType.Active,
    131: ItemType.Familiar,
    132: ItemType.Passive,
    133: ItemType.Active,
    134: ItemType.Passive,
    135: ItemType.Active,
    136: ItemType.Active,
    137: ItemType.Active,
    138: ItemType.Passive,
    139: ItemType.Passive,
    140: ItemType.Passive,
    141: ItemType.Passive,
    142: ItemType.Passive,
    143: ItemType.Passive,
    144: ItemType.Familiar,
    145: ItemType.Active,
    146: ItemType.Active,
    147: ItemType.Active,
    148: ItemType.Passive,
    149: ItemType.Passive,
    150: ItemType.Passive,
    151: ItemType.Passive,
    152: ItemType.Passive,
    153: ItemType.Passive,
    154: ItemType.Passive,
    155: ItemType.Familiar,
    156: ItemType.Passive,
    157: ItemType.Passive,
    158: ItemType.Active,
    159: ItemType.Passive,
    160: ItemType.Active,
    161: ItemType.Passive,
    162: ItemType.Passive,
    163: ItemType.Familiar,
    164: ItemType.Active,
    165: ItemType.Passive,
    166: ItemType.Active,
    167: ItemType.Familiar,
    168: ItemType.Passive,
    169: ItemType.Passive,
    170: ItemType.Familiar,
    171: ItemType.Active,
    172: ItemType.Familiar,
    173: ItemType.Passive,
    174: ItemType.Familiar,
    175: ItemType.Active,
    176: ItemType.Passive,
    177: ItemType.Active,
    178: ItemType.Familiar,
    179: ItemType.Passive,
    180: ItemType.Passive,
    181: ItemType.Active,
    182: ItemType.Passive,
    183: ItemType.Passive,
    184: ItemType.Passive,
    185: ItemType.Passive,
    186: ItemType.Active,
    187: ItemType.Familiar,
    188: ItemType.Familiar,
    189: ItemType.Passive,
    190: ItemType.Passive,
    191: ItemType.Passive,
    192: ItemType.Active,
    193: ItemType.Passive,
    194: ItemType.Passive,
    195: ItemType.Passive,
    196: ItemType.Passive,
    197: ItemType.Passive,
    198: ItemType.Passive,
    199: ItemType.Passive,
    200: ItemType.Passive,
    201: ItemType.Passive,
    202: ItemType.Passive,
    203: ItemType.Passive,
    204: ItemType.Passive,
    205: ItemType.Passive,
    206: ItemType.Familiar,
    207: ItemType.Familiar,
    208: ItemType.Passive,
    209: ItemType.Passive,
    210: ItemType.Passive,
    211: ItemType.Passive,
    212: ItemType.Passive,
    213: ItemType.Passive,
    214: ItemType.Passive,
    215: ItemType.Passive,
    216: ItemType.Passive,
    217: ItemType.Passive,
    218: ItemType.Passive,
    219: ItemType.Passive,
    220: ItemType.Passive,
    221: ItemType.Passive,
    222: ItemType.Passive,
    223: ItemType.Passive,
    224: ItemType.Passive,
    225: ItemType.Passive,
    226: ItemType.Passive,
    227: ItemType.Passive,
    228: ItemType.Passive,
    229: ItemType.Passive,
    230: ItemType.Passive,
    231: ItemType.Passive,
    232: ItemType.Passive,
    233: ItemType.Passive,
    234: ItemType.Passive,
    236: ItemType.Passive,
    237: ItemType.Passive,
    238: ItemType.Familiar,
    239: ItemType.Familiar,
    240: ItemType.Passive,
    241: ItemType.Passive,
    242: ItemType.Passive,
    243: ItemType.Passive,
    244: ItemType.Passive,
    245: ItemType.Passive,
    246: ItemType.Passive,
    247: ItemType.Passive,
    248: ItemType.Passive,
    249: ItemType.Passive,
    250: ItemType.Passive,
    251: ItemType.Passive,
    252: ItemType.Passive,
    253: ItemType.Passive,
    254: ItemType.Passive,
    255: ItemType.Passive,
    256: ItemType.Passive,
    257: ItemType.Passive,
    258: ItemType.Passive,
    259: ItemType.Passive,
    260: ItemType.Passive,
    261: ItemType.Passive,
    262: ItemType.Passive,
    263: ItemType.Active,
    264: ItemType.Familiar,
    265: ItemType.Familiar,
    266: ItemType.Familiar,
    267: ItemType.Familiar,
    268: ItemType.Familiar,
    269: ItemType.Familiar,
    270: ItemType.Familiar,
    271: ItemType.Familiar,
    272: ItemType.Familiar,
    273: ItemType.Familiar,
    274: ItemType.Familiar,
    275: ItemType.Familiar,
    276: ItemType.Familiar,
    277: ItemType.Familiar,
    278: ItemType.Familiar,
    279: ItemType.Familiar,
    280: ItemType.Familiar,
    281: ItemType.Familiar,
    282: ItemType.Active,
    283: ItemType.Active,
    284: ItemType.Active,
    285: ItemType.Active,
    286: ItemType.Active,
    287: ItemType.Active,
    288: ItemType.Active,
    289: ItemType.Active,
    290: ItemType.Active,
    291: ItemType.Active,
    292: ItemType.Active,
    293: ItemType.Active,
    294: ItemType.Active,
    295: ItemType.Active,
    296: ItemType.Active,
    297: ItemType.Active,
    298: ItemType.Active,
    299: ItemType.Passive,
    300: ItemType.Passive,
    301: ItemType.Passive,
    302: ItemType.Passive,
    303: ItemType.Passive,
    304: ItemType.Passive,
    305: ItemType.Passive,
    306: ItemType.Passive,
    307: ItemType.Passive,
    308: ItemType.Passive,
    309: ItemType.Passive,
    310: ItemType.Passive,
    311: ItemType.Passive,
    312: ItemType.Passive,
    313: ItemType.Passive,
    314: ItemType.Passive,
    315: ItemType.Passive,
    316: ItemType.Passive,
    317: ItemType.Passive,
    318: ItemType.Familiar,
    319: ItemType.Familiar,
    320: ItemType.Familiar,
    321: ItemType.Familiar,
    322: ItemType.Familiar,
    323: ItemType.Active,
    324: ItemType.Active,
    325: ItemType.Active,
    326: ItemType.Active,
    327: ItemType.Passive,
    328: ItemType.Passive,
    329: ItemType.Passive,
    330: ItemType.Passive,
    331: ItemType.Passive,
    332: ItemType.Passive,
    333: ItemType.Passive,
    334: ItemType.Passive,
    335: ItemType.Passive,
    336: ItemType.Passive,
    337: ItemType.Passive,
    338: ItemType.Active,
    339: ItemType.Passive,
    340: ItemType.Passive,
    341: ItemType.Passive,
    342: ItemType.Passive,
    343: ItemType.Passive,
    344: ItemType.Passive,
    345: ItemType.Passive,
    346: ItemType.Passive,
    347: ItemType.Active,
    348: ItemType.Active,
    349: ItemType.Active,
    350: ItemType.Passive,
    351: ItemType.Active,
    352: ItemType.Active,
    353: ItemType.Passive,
    354: ItemType.Passive,
    355: ItemType.Passive,
    356: ItemType.Passive,
    357: ItemType.Active,
    358: ItemType.Passive,
    359: ItemType.Passive,
    360: ItemType.Familiar,
    361: ItemType.Familiar,
    362: ItemType.Familiar,
    363: ItemType.Familiar,
    364: ItemType.Familiar,
    365: ItemType.Familiar,
    366: ItemType.Passive,
    367: ItemType.Passive,
    368: ItemType.Passive,
    369: ItemType.Passive,
    370: ItemType.Passive,
    371: ItemType.Passive,
    372: ItemType.Familiar,
    373: ItemType.Passive,
    374: ItemType.Passive,
    375: ItemType.Passive,
    376: ItemType.Passive,
    377: ItemType.Passive,
    378: ItemType.Passive,
    379: ItemType.Passive,
    380: ItemType.Passive,
    381: ItemType.Passive,
    382: ItemType.Active,
    383: ItemType.Active,
    384: ItemType.Familiar,
    385: ItemType.Familiar,
    386: ItemType.Active,
    387: ItemType.Familiar,
    388: ItemType.Familiar,
    389: ItemType.Familiar,
    390: ItemType.Familiar,
    391: ItemType.Passive,
    392: ItemType.Passive,
    393: ItemType.Passive,
    394: ItemType.Passive,
    395: ItemType.Passive,
    396: ItemType.Active,
    397: ItemType.Passive,
    398: ItemType.Passive,
    399: ItemType.Passive,
    400: ItemType.Passive,
    401: ItemType.Passive,
    402: ItemType.Passive,
    403: ItemType.Familiar,
    404: ItemType.Familiar,
    405: ItemType.Familiar,
    406: ItemType.Active,
    407: ItemType.Passive,
    408: ItemType.Passive,
    409: ItemType.Passive,
    410: ItemType.Passive,
    411: ItemType.Passive,
    412: ItemType.Passive,
    413: ItemType.Passive,
    414: ItemType.Passive,
    415: ItemType.Passive,
    416: ItemType.Passive,
    417: ItemType.Familiar,
    418: ItemType.Passive,
    419: ItemType.Active,
    420: ItemType.Passive,
    421: ItemType.Active,
    422: ItemType.Active,
    423: ItemType.Passive,
    424: ItemType.Passive,
    425: ItemType.Passive,
    426: ItemType.Familiar,
    427: ItemType.Active,
    428: ItemType.Passive,
    429: ItemType.Passive,
    430: ItemType.Familiar,
    431: ItemType.Familiar,
    432: ItemType.Passive,
    433: ItemType.Passive,
    434: ItemType.Active,
    435: ItemType.Familiar,
    436: ItemType.Familiar,
    437: ItemType.Active,
    438: ItemType.Passive,
    439: ItemType.Active,
    440: ItemType.Passive,
    441: ItemType.Active,
    442: ItemType.Passive,
    443: ItemType.Passive,
    444: ItemType.Passive,
    445: ItemType.Passive,
    446: ItemType.Passive,
    447: ItemType.Passive,
    448: ItemType.Passive,
    449: ItemType.Passive,
    450: ItemType.Passive,
    451: ItemType.Passive,
    452: ItemType.Passive,
    453: ItemType.Passive,
    454: ItemType.Passive,
    455: ItemType.Passive,
    456: ItemType.Passive,
    457: ItemType.Passive,
    458: ItemType.Passive,
    459: ItemType.Passive,
    460: ItemType.Passive,
    461: ItemType.Passive,
    462: ItemType.Passive,
    463: ItemType.Passive,
    464: ItemType.Passive,
    465: ItemType.Passive,
    466: ItemType.Passive,
    467: ItemType.Familiar,
    468: ItemType.Familiar,
    469: ItemType.Familiar,
    470: ItemType.Familiar,
    471: ItemType.Familiar,
    472: ItemType.Familiar,
    473: ItemType.Familiar,
    474: ItemType.Familiar,
    475: ItemType.Active,
    476: ItemType.Active,
    477: ItemType.Active,
    478: ItemType.Active,
    479: ItemType.Active,
    480: ItemType.Active,
    481: ItemType.Active,
    482: ItemType.Active,
    483: ItemType.Active,
    484: ItemType.Active,
    485: ItemType.Active,
    486: ItemType.Active,
    487: ItemType.Active,
    488: ItemType.Active,
    489: ItemType.Active,
    490: ItemType.Active,
    491: ItemType.Familiar,
    492: ItemType.Familiar,
    493: ItemType.Passive,
    494: ItemType.Passive,
    495: ItemType.Passive,
    496: ItemType.Passive,
    497: ItemType.Passive,
    498: ItemType.Passive,
    499: ItemType.Passive,
    500: ItemType.Familiar,
    501: ItemType.Passive,
    502: ItemType.Passive,
    503: ItemType.Passive,
    504: ItemType.Active,
    505: ItemType.Passive,
    506: ItemType.Passive,
    507: ItemType.Active,
    508: ItemType.Familiar,
    509: ItemType.Familiar,
    510: ItemType.Active,
    511: ItemType.Familiar,
    512: ItemType.Active,
    513: ItemType.Passive,
    514: ItemType.Passive,
    515: ItemType.Active,
    516: ItemType.Active,
    517: ItemType.Passive,
    518: ItemType.Familiar,
    519: ItemType.Familiar,
    520: ItemType.Passive,
    521: ItemType.Active,
    522: ItemType.Active,
    523: ItemType.Active,
    524: ItemType.Passive,
    525: ItemType.Familiar,
    526: ItemType.Familiar,
    527: ItemType.Active,
    528: ItemType.Familiar,
    529: ItemType.Passive,
    530: ItemType.Passive,
    531: ItemType.Passive,
    532: ItemType.Passive,
    533: ItemType.Passive,
    534: ItemType.Passive,
    535: ItemType.Passive,
    536: ItemType.Active,
    537: ItemType.Familiar,
    538: ItemType.Passive,
    539: ItemType.Familiar,
    540: ItemType.Passive,
    541: ItemType.Passive,
    542: ItemType.Familiar,
    543: ItemType.Familiar,
    544: ItemType.Familiar,
    545: ItemType.Active,
    546: ItemType.Passive,
    547: ItemType.Passive,
    548: ItemType.Familiar,
    549: ItemType.Passive,
    550: ItemType.Active,
    551: ItemType.Passive,
    552: ItemType.Active,
    553: ItemType.Passive,
    554: ItemType.Passive,
    555: ItemType.Active,
    556: ItemType.Active,
    557: ItemType.Active,
    558: ItemType.Passive,
    559: ItemType.Passive,
    560: ItemType.Passive,
    561: ItemType.Passive,
    562: ItemType.Passive,
    563: ItemType.Passive,
    564: ItemType.Passive,
    565: ItemType.Familiar,
    566: ItemType.Passive,
    567: ItemType.Passive,
    568: ItemType.Passive,
    569: ItemType.Passive,
    570: ItemType.Passive,
    571: ItemType.Passive,
    572: ItemType.Passive,
    573: ItemType.Passive,
    574: ItemType.Passive,
    575: ItemType.Familiar,
    576: ItemType.Passive,
    577: ItemType.Active,
    578: ItemType.Active,
    579: ItemType.Passive,
    580: ItemType.Active,
    581: ItemType.Familiar,
    582: ItemType.Active,
    583: ItemType.Passive,
    584: ItemType.Active,
    585: ItemType.Active,
    586: ItemType.Passive,
    588: ItemType.Passive,
    589: ItemType.Passive,
    590: ItemType.Passive,
    591: ItemType.Passive,
    592: ItemType.Passive,
    593: ItemType.Passive,
    594: ItemType.Passive,
    595: ItemType.Passive,
    596: ItemType.Passive,
    597: ItemType.Passive,
    598: ItemType.Passive,
    599: ItemType.Passive,
    600: ItemType.Passive,
    601: ItemType.Passive,
    602: ItemType.Passive,
    603: ItemType.Passive,
    604: ItemType.Active,
    605: ItemType.Active,
    606: ItemType.Passive,
    607: ItemType.Familiar,
    608: ItemType.Familiar,
    609: ItemType.Active,
    610: ItemType.Familiar,
    611: ItemType.Active,
    612: ItemType.Familiar,
    614: ItemType.Passive,
    615: ItemType.Familiar,
    616: ItemType.Passive,
    617: ItemType.Passive,
    618: ItemType.Passive,
    619: ItemType.Passive,
    621: ItemType.Passive,
    622: ItemType.Active,
    623: ItemType.Active,
    624: ItemType.Passive,
    625: ItemType.Active,
    626: ItemType.Familiar,
    627: ItemType.Familiar,
    628: ItemType.Active,
    629: ItemType.Familiar,
    631: ItemType.Active,
    632: ItemType.Passive,
    633: ItemType.Passive,
    634: ItemType.Passive,
    635: ItemType.Active,
    636: ItemType.Active,
    637: ItemType.Passive,
    638: ItemType.Active,
    639: ItemType.Active,
    640: ItemType.Active,
    641: ItemType.Passive,
    642: ItemType.Active,
    643: ItemType.Passive,
    644: ItemType.Passive,
    645: ItemType.Passive,
    646: ItemType.Passive,
    647: ItemType.Passive,
    649: ItemType.Familiar,
    650: ItemType.Active,
    651: ItemType.Familiar,
    652: ItemType.Familiar,
    653: ItemType.Active,
    654: ItemType.Passive,
    655: ItemType.Active,
    657: ItemType.Passive,
    658: ItemType.Passive,
    659: ItemType.Passive,
    660: ItemType.Passive,
    661: ItemType.Familiar,
    663: ItemType.Passive,
    664: ItemType.Passive,
    665: ItemType.Passive,
    667: ItemType.Passive,
    668: ItemType.Passive,
    669: ItemType.Passive,
    670: ItemType.Passive,
    671: ItemType.Passive,
    672: ItemType.Passive,
    673: ItemType.Passive,
    674: ItemType.Passive,
    675: ItemType.Passive,
    676: ItemType.Passive,
    677: ItemType.Passive,
    678: ItemType.Passive,
    679: ItemType.Familiar,
    680: ItemType.Passive,
    681: ItemType.Familiar,
    682: ItemType.Familiar,
    683: ItemType.Passive,
    684: ItemType.Passive,
    685: ItemType.Active,
    686: ItemType.Passive,
    687: ItemType.Active,
    688: ItemType.Passive,
    689: ItemType.Passive,
    690: ItemType.Passive,
    691: ItemType.Passive,
    692: ItemType.Passive,
    693: ItemType.Passive,
    694: ItemType.Passive,
    695: ItemType.Passive,
    696: ItemType.Passive,
    697: ItemType.Familiar,
    698: ItemType.Familiar,
    699: ItemType.Passive,
    700: ItemType.Passive,
    701: ItemType.Passive,
    702: ItemType.Passive,
    703: ItemType.Active,
    704: ItemType.Active,
    705: ItemType.Active,
    706: ItemType.Active,
    707: ItemType.Passive,
    708: ItemType.Passive,
    709: ItemType.Active,
    710: ItemType.Active,
    711: ItemType.Active,
    712: ItemType.Active,
    713: ItemType.Active,
    714: ItemType.Active,
    715: ItemType.Active,
    716: ItemType.Passive,
    717: ItemType.Passive,
    719: ItemType.Active,
    720: ItemType.Active,
    721: ItemType.Passive,
    722: ItemType.Active,
    723: ItemType.Active,
    724: ItemType.Passive,
    725: ItemType.Passive,
    726: ItemType.Passive,
    727: ItemType.Passive,
    728: ItemType.Active,
    729: ItemType.Active,
}

items_blacklist = [
    0x3B,
    0xEB,
    0x2B,
    0x3D,
    0xEE,
    0xEF,
    0x226,
    0x227,
    0x228,
    0x272,
    0x273,
    0x2C6,
    0x2C7,
    0x2CA,
    0x2CB,
]
