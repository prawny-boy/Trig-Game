import threading
import queue

def input_with_timeout(prompt, timeout, q):
  inp = input(prompt)
  try:
    q.put(inp)
  except:
    pass
