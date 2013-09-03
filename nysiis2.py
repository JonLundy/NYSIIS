#!/usr/bin/env python3
import unicodedata

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        return cr
    return start

@coroutine
def filter_unicode(target):
  while True:
    text = (yield)
    text = unicodedata.normalize('NFKD', text ).encode('ascii','ignore')
    text = text.decode()
    text = "".join( [c for c in text if c.isalpha()] ).upper() 
    target.send(text)

@coroutine
def nysiis_process(target):
  while True:
    text = (yield)
     # Translate first characters of text: MAC → MCC, KN → N, K → C, PH, PF → FF, SCH → SSS

    tst1 = text[0:1]
    tst2 = text[0:2]
    tst3 = text[0:3] 

    if   tst3 == "MAC": text = "MCC" + text[3:]
    elif tst3 == "SCH": text = "SSS" + text[3:]
    elif tst2 == "PH":  text = "F"   + text[2:] 
    elif tst2 == "PF":  text =         text[1:] 
    elif tst2 == "KN":  text =         text[1:]
    elif tst1 == "K":   text = "C"   + text[1:]

    # Translate last characters of text: EE → Y, IE → Y, DT, RT, RD, NT, ND → D

    tst2n = text[-2:]

    if   tst2n == "EE": text = text[:-2] + "Y"
    elif tst2n == "IE": text = text[:-2] + "Y"
    elif tst2n == "RD": text = text[:-2] + "D"
    elif tst2n == "ND": text = text[:-2] + "D"
    elif tst2n == "DT": text = text[:-2] + "D"
    elif tst2n == "RT": text = text[:-2] + "D"
    elif tst2n == "NT": text = text[:-2] + "D"

    # First character of key = first character of text.

    key = text[0:1]

    # Translate remaining characters by following rules, incrementing by one character each time:

    last = text[0:1]
    text = text[1:]

    while len(text) > 0:
      text1 = text[0:1]
      text2 = text[0:2]
      text3 = text[0:3] 
      vowels = ["A","E","I","O","U"]

      # EV → AF else A, E, I, O, U → A
      if   text2 == "EV":   text = "AF" + text[2:]
      elif text1 in vowels: text = "A"  + text[1:] 
      # Q → G, Z → S, M → N
      elif text1 == "Q":    text = "G"  + text[1:]
      elif text1 == "Z":    text = "S"  + text[1:]
      elif text1 == "M":    text = "N"  + text[1:]
      # KN → N else K → C
      elif text2 == "KN":   text = "N"  + text[2:]
      elif text1 == "K":    text = "C"  + text[1:]
      # SCH → SSS, PH → FF
      elif text3 == "SCH": text = "SSS" + text[3:]
      elif text2 == "PH":  text = "FF"  + text[2:]
      # H → If previous or next is non-vowel, previous.
      elif text1 == "H": 
        if last not in vowels and text[1:1] not in vowels: 
          text = last + text[1:]
      # W → If previous is vowel, A.
      elif text1 == "W": 
        if last in vowels: 
          text = "A" + text[1:]

      # Add current to key if current is not same as the last key character.
      val = text[0:1]
      if val != key[-1:]: key = key + text[0:1]
      last = val
      text = text[1:]

    # If last character is S, remove it.
    key1n = key[-1:]
    key2n = key[-2:]

    if key1n == "S": key = key[:-1]
    # If last characters are AY, replace with Y.
    elif key2n == "AY": key = key[:-2] + "Y"
    # If last character is A, remove it.
    elif key1n == "A": key = key[:-1]

    # Append translated key to value from step 3 (removed first character)
    # If longer than 6 characters, truncate to first 6 characters. 
    #   (only needed for true NYSIIS, some versions use the full key)
    if len(key) > 6: key = key[0:6] 
    
    target.send(key)

@coroutine
def printer():
    while True:
         line = (yield)
         print(line, end=' ')

#if __name__ == '__main__':
import sys
nysiis = filter_unicode(nysiis_process(printer()))
for i in sys.argv[1:]:
    nysiis.send(i)
