#!/usr/bin/env python3

"""NYSIIS phonetic code algorithm
   Adapted from Taft, R. L. (1970), "Name Search Techniques", Albany, New York: New York State Identification and Intelligence System
"""

def nysiis(text):
  store = []
  for name in text.split(' '):
    name = "".join( [c for c in name if c.isalpha()] ).upper() # Clean the string.

    # Translate first characters of name: MAC → MCC, KN → N, K → C, PH, PF → FF, SCH → SSS

    tst1 = name[0:1]
    tst2 = name[0:2]
    tst3 = name[0:3] 

    if   tst3 == "MAC": name = "MCC" + name[3:]
    elif tst3 == "SCH": name = "SSS" + name[3:]
    elif tst2 == "PH":  name = "F"   + name[2:] 
    elif tst2 == "PF":  name =         name[1:] 
    elif tst2 == "KN":  name =         name[1:]
    elif tst1 == "K":   name = "C"   + name[1:]

    # Translate last characters of name: EE → Y, IE → Y, DT, RT, RD, NT, ND → D

    tst2n = name[-2:]

    if   tst2n == "EE": name = name[:-2] + "Y"
    elif tst2n == "IE": name = name[:-2] + "Y"
    elif tst2n == "RD": name = name[:-2] + "D"
    elif tst2n == "ND": name = name[:-2] + "D"
    elif tst2n == "DT": name = name[:-2] + "D"
    elif tst2n == "RT": name = name[:-2] + "D"
    elif tst2n == "NT": name = name[:-2] + "D"

    # First character of key = first character of name.

    key = name[0:1]

    # Translate remaining characters by following rules, incrementing by one character each time:

    last = name[0:1]
    name = name[1:]

    while len(name) > 0:
      name1 = name[0:1]
      name2 = name[0:2]
      name3 = name[0:3] 
      vowels = ["A","E","I","O","U"]

      # EV → AF else A, E, I, O, U → A
      if   name2 == "EV":   name = "AF" + name[2:]
      elif name1 in vowels: name = "A"  + name[1:] 
      # Q → G, Z → S, M → N
      elif name1 == "Q":    name = "G"  + name[1:]
      elif name1 == "Z":    name = "S"  + name[1:]
      elif name1 == "M":    name = "N"  + name[1:]
      # KN → N else K → C
      elif name2 == "KN":   name = "N"  + name[2:]
      elif name1 == "K":    name = "C"  + name[1:]
      # SCH → SSS, PH → FF
      elif name3 == "SCH": name = "SSS" + name[3:]
      elif name2 == "PH":  name = "FF"  + name[2:]
      # H → If previous or next is non-vowel, previous.
      elif name1 == "H": 
        if last not in vowels and name[1:1] not in vowels: 
          name = last + name[1:]
      # W → If previous is vowel, A.
      elif name1 == "W": 
        if last in vowels: 
          name = "A" + name[1:]

      # Add current to key if current is not same as the last key character.
      val = name[0:1]
      if val != key[-1:]: key = key + name[0:1]
      last = val
      name = name[1:]

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
    
    store.append(key)

  return ' '.join(store) 
    
if __name__ == '__main__':
        import sys
        print (nysiis(' '.join(sys.argv[1:])))
