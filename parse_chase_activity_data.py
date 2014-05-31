
import re, datetime, json

def parse_dollar_string(s):
  DOLLAR_RE = '^(-?)\$(.*)$'
  match = re.search(DOLLAR_RE, s)
  if match:
    sign = -1.0 if match.group(1) else 1.0
    val = match.group(2)
    try:
      val = float(val)
    except ValueError:
      val = 0.0
    return sign * val
  return 0.0

def parse_merchant_address(s):
  NULL_RE = 'null.*'
  if not s or re.match(NULL_RE, s): return None
  else: return s

def parse_date_string(s):
  m, d, y = map(int, s.split('/'))
  return datetime.date(y, m, d)

def parse_activity(act):
  act['amount'] = parse_dollar_string(act['amount'])
  act['merchantAddress'] = parse_merchant_address(act['merchantAddress'])
  date_fields = ['tranDate', 'postDate']
  for f in date_fields:
    act[f] = parse_date_string(act[f])

  return act

def read_posted_activities(json_file_name):
  activities = None
  with open(json_file_name, 'r') as f:
    activities = json.loads(f.read())['Posted']

  activities = map(parse_activity, activities)
  return activities;

if __name__ == '__main__':
  acts = read_posted_activities('my-chase-activities.json')
