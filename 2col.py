from sys import argv;
from functools import reduce;
from collections import deque;
import os.path;
import operator;
import itertools;
import random;
import math;
import re;

class cellHolder:
  value = 0;
  lineNum = 0;
  def __init__(self, cellData, line):
    self.value = cellData;
    self.lineNum = line;

cell = cellHolder(0, 0);

def isint(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

def parse_args(args):
  res = [];
  res.append(sdeque());
  for x in args:
    if isint(x):
      res[0].append(x);
    elif re.match('^\[.*\]$', x):
      arrInput = eval(x);
      res.append(sdeque());
      for i in arrInput:
        if isint(i):
          res[-1].append(int(i));
        elif len(i) == 1:
          res[-1].append(ord(i));
        else:
          for c in i:
            res[-1].append(ord(c));
    else:
      for c in x:
        res[0].append(ord(c));
  return res;

def parse_line(lines, cell):
  l = lines[cell.lineNum];
  if ' ' in l:
    l = l.strip();
  if l.startswith('+'):
    if len(l) > 1:
      if l[-1] == 'v':
        cell.lineNum += 1;
        val = parse_line(lines, cellHolder(cell.value, cell.lineNum));
        cell.value += int(val) if isint(val) else ord(val[0]);
      else:
        cell.value += int(l[-1]) if isint(l[-1]) else ord(l[-1]);
    else:
      cell.value += cell.value;
  elif l.startswith('-'):
    if len(l) > 1:
      if l[-1] == 'v':
        cell.lineNum += 1;
        val = parse_line(lines, cellHolder(cell.value, cell.lineNum));
        cell.value -= int(val) if isint(val) else ord(val[0]);
      else:
        cell.value -= int(l[-1]) if isint(l[-1]) else ord(l[-1]);
    else:
      cell.value -= cell.value;
  elif l.startswith('*'):
    if len(l) > 1:
      if l[-1] == 'v':
        cell.lineNum += 1;
        val = parse_line(lines, cellHolder(cell.value, cell.lineNum));
        cell.value *= int(val) if isint(val) else ord(val[0]);
      else:
        cell.value *= int(l[-1]) if isint(l[-1]) else ord(l[-1]);
    else:
      cell.value *= cell.value;
  elif l.startswith('/'):
    if len(l) > 1:
      if l[-1] == 'v':
        cell.lineNum += 1;
        val = parse_line(lines, cellHolder(cell.value, cell.lineNum));
        cell.value /= int(val) if isint(val) else ord(val[0]);
      else:
        cell.value /= int(l[-1]) if isint(l[-1]) else ord(l[-1]);
    else:
      cell.value /= cell.value;
  elif isint(l):
    return int(l);
  elif l.startswith('?'):
    if l[-1] == '^':
      if not parse_line(lines, cellHolder(cell.value, cell.lineNum - 1)):
        cell.lineNum += 1;
  elif l.startswith('!'):
    if l[-1] == '^':
      if parse_line(lines, cellHolder(cell.value, cell.lineNum - 1)):
        cell.lineNum += 1;
  elif l.startswith('$'):
    if l[-1] == '^':
      val = parse_line(lines, cellHolder(cell.value, cell.lineNum - 1));
      return cell.value in val;
  elif l.startswith('#'):
    if l[-1] == '#':
      print(cell.value);
    elif l[-1] == 'v':
      cell.lineNum += 1;
      val = parse_line(lines, cell);
      print(val);
      return val;
    elif l[-1] == '^':
      val = parse_line(lines, cellHolder(cell.value, cell.lineNum - 1));
      print(val);
      return val;
  elif l.startswith('^'):
    val = parse_line(lines, cellHolder(cell.value, cell.lineNum - 1));
    return val;
  elif l.startswith('v'):
    cell.lineNum += 1;
    val = parse_line(lines, cell);
    return val;
  elif l == "Sq":
    return not (cell.value**.5%1);
  elif l == "F!":
    val = [];
    for i in range(0, cell.value + 1):
      val.append(math.factorial(i));
    return val;
  else:
    return int(l) if isint(l) else ord(l[0]);

  return cell.value;

def parse(code):
  #print('Parsing %s' % code);
  source = code.split('\n');
  for l in source:
    if len(l) != 2:
      print('Invalid code!');
      print("The following line is not valid 2Col: '%s'" % l);
      return;
  global cell;
  if len(argv) > 3:
    cell.value = int(argv[3]) if isint(argv[3]) else ord(argv[3][0]);
  while cell.lineNum < len(source):
    parse_line(source, cell);
    cell.lineNum += 1;
  #print(cell.value);

if len(argv) < 3:
  print('Invalid args!');
  print('Correct usage: %s <flag> <source> [source args]\n    <flag> : Either -f or -c. -f indicates that <source> is a file to be read from, while -c indicates that <source> is braingolf code to be run.' % argv[0]);
  exit();

mode = argv[1];
source = argv[2];

if mode == '-f':
  filename = source;
  if os.path.isfile(filename):
    with open(source) as f:
      source = f.read();
    parse(source);
  else:
    print('File %s not found!' % filename);
    exit();

elif mode == '-c':
  parse(source);
else:
  print('Invalid flag!');
  exit();
