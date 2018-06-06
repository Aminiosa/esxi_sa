from collections import defaultdict
fixedpoint_dict = lambda: defaultdict(fixedpoint_dict)
struct = fixedpoint_dict()

struct['foo']['bar']['baz'] = 42
print(fixedpoint_dict)