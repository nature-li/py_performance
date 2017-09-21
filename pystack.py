import sys
import inspect
import time
import traceback

def deeper(func, depth):
    if depth > 0:
        return deeper(func, depth-1)
    else:
        return func()

def no_stack():
    # do no inspection, measure the cost of deeper()
    return "name"

def show_stack():
   name = inspect.stack()[1][3]
   return name

def show_trace():
   frame = traceback.extract_stack()[-2]
   name = getattr(frame, 'name', frame[2])
   return name

def show_limit():
   frame = traceback.extract_stack(limit=2)[-2]
   name = getattr(frame, 'name', frame[2])
   return name

def sys_traceback():
   frame = sys._getframe().f_back
   frame_info = traceback.extract_stack(f=frame, limit=1)[0]
   name = getattr(frame_info, 'name', frame_info[2])
   return name

def sys_inspect():
   frame = sys._getframe().f_back
   name = inspect.getframeinfo(frame)[2]
   return name

def inspect_inspect():
    frame = inspect.currentframe().f_back
    name = inspect.getframeinfo(frame)[2]
    return name

def measure_time(func, repeat=1000, stack=50):
    total = 0
    for _ in range(repeat):
        start = time.time()
        deeper(func, stack)
        span = time.time() - start
        total = total + span

    print("{0:.2f} sec".format(total))

print('no measurement')
measure_time(no_stack)
measure_time(no_stack, stack=200)
print('inspect.stack (run 10% as many times, because slow)')
measure_time(show_stack, repeat=100)
measure_time(show_stack, repeat=100, stack=200)
print('traceback.extract_stack')
measure_time(show_trace)
measure_time(show_trace, stack=200)
print('traceback.extract_stack + limit')
measure_time(show_limit)
measure_time(show_limit, stack=200)
print('sys.getframe + traceback')
measure_time(sys_traceback)
measure_time(sys_traceback, stack=200)
print('sys.getframe + inspect')
measure_time(sys_inspect)
measure_time(sys_inspect, stack=200)
print('inspect.currentframe + inspect')
measure_time(inspect_inspect)
measure_time(inspect_inspect, stack=200)

# testing inspect performance suggestions from:
# - https://stackoverflow.com/questions/41481722/python-traceback-performance-problems