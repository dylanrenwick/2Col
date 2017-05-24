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

cell  = cellHolder(0, 0);
loops = dict();

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

def get_val(valCode, lines, cell):
  if valCode == 'v':
    cell.lineNum += 1;
    return(parse_line(lines, cellHolder(cell.value, cell.lineNum)));
  elif valCode == '^':
    return(parse_line(lines, cellHolder(cell.value, cell.lineNum - 1)));
  elif isint(valCode):
    return int(valCode);
  else:
    return ord(valCode);

def find_end(lines):
  forCount = 0;
  for x in range(0, len(lines)):
    if lines[x] == 'Ed':
      if forCount > 0:
        forCount -= 1;
      else:
        return (lines[:-x], x + 1);
    elif lines[x].startswith('F') and lines[x] != 'F!':
      forCount += 1;

def parse_line(lines, cell):
  global loops;
  if cell.lineNum < 0 or cell.lineNum >= len(lines):
    return 0;
  l = lines[cell.lineNum];
  if ' ' in l:
    l = l.strip();
  if l == "Sq":
    return not (cell.value**.5%1);
  elif l == "F!":
    val = [];
    for i in range(0, cell.value):
      val.append(math.factorial(i + 1));
    return val;
  elif l == "HW":
    return "Hello, World!";
  elif l == "In":
    return input();
  elif l == "Ed":
    return 0;
  elif l.startswith('+'):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
      cell.value += int(val) if isint(val) else (sum(val) if type(val) is list else ord(val[0]));
    else:
      cell.value += cell.value;
  elif l.startswith('-'):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
      cell.value -= int(val) if isint(val) else (sum(val) if type(val) is list else ord(val[0]));
    else:
      cell.value -= cell.value;
  elif l.startswith('*'):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
      cell.value *= int(val) if isint(val) else (sum(val) if type(val) is list else ord(val[0]));
    else:
      cell.value *= cell.value;
  elif l.startswith('/'):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
      cell.value /= int(val) if isint(val) else (sum(val) if type(val) is list else ord(val[0]));
    else:
      cell.value /= cell.value;
  elif l.startswith('='):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
      cell.value = int(val) if isint(val) else (sum(val) if type(val) is list else ord(val[0]));
  elif isint(l):
    return int(l);
  elif l.startswith('?'):
    val = get_val(l[-1], lines, cell);
    if not val:
      cell.lineNum += 1;
  elif l.startswith('!'):
    val = get_val(l[-1], lines, cell);
    if val:
      cell.lineNum += 1;
  elif l.startswith('$'):
    val = get_val(l[-1], lines, cell);
    return cell.value in val;
  elif l.startswith('#'):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
      print(val);
      return val;
    else:
      print(cell.value);
  elif l.startswith('d'):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
    else:
      val = cell.value;
    rand = random.randint(1, val);
    print(rand);
    return rand;
  elif l.startswith('D'):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
    else:
      val = cell.value;
    ret = [];
    for i in range(val, 0):
      ret.append(i);
    return ret;
  elif l.startswith('F'):
    if len(l) > 1:
      val = get_val(l[-1], lines, cell);
    else:
      val = cell.value;
    end = find_end(lines[cell.lineNum+1:]);
    if type(val) is list:
      for x in val:
        parse('\n'.join(end[0]), cellHolder(x, 0));
    else:
      for x in range(0, val):
        parse('\n'.join(end[0]), cellHolder(x, 0));
    cell.lineNum += end[1];
  elif l.startswith('^'):
    val = parse_line(lines, cellHolder(cell.value, cell.lineNum - 1));
    return val;
  elif l.startswith('v'):
    cell.lineNum += 1;
    val = parse_line(lines, cell);
    return val;
  else:
    return int(l) if isint(l) else ord(l[0]);

  return cell.value;

def parse(code, cell):
  #print('Parsing %s' % code);
  source = code.split('\n');
  for l in source:
    if len(l) != 2:
      print('Invalid code!');
      print("The following line is not valid 2Col: '%s'" % l);
      return;
  if len(argv) > 3:
    cell.value = int(argv[3]) if isint(argv[3]) else ord(argv[3][0]);
  retval = 0;
  while cell.lineNum < len(source):
    retval = parse_line(source, cell);
    cell.lineNum += 1;
  print(retval);

if len(argv) < 3:
  print('Invalid args!');
  print('Correct usage: %s <flag> <source> [source args]\n    <flag> : Either -f or -c. -f indicates that <source> is a file to be read from, while -c indicates that <source> is braingolf code to be run.' % argv[0]);
  exit();

mode = argv[1];
source = argv[2];

if mode == '-f':
  filename = source;
  global cell;
  if os.path.isfile(filename):
    with open(source) as f:
      source = f.read();
    parse(source, cell);
  else:
    print('File %s not found!' % filename);
    exit();
elif mode == '-c':
  parse(source, cell);
else:
  print('Invalid flag!');
  exit();
