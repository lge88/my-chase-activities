

import re, pandas
from parse_chase_activity_data import read_posted_activities

class ChaseActivities:
  def __init__(self, df):
    self.df = df

  def get_payments(self):
    return self.df[self.df['amount'] < 0]

  def get_purchases(self):
    return self.df[self.df['amount'] > 0]

  def normalize_shop_name(self, shop_name):
    shops = [
      ('7-ELEVEN', '7-ELEVEN'),
      ('99 RANCH', '99 RANCH'),
      ('ALLSTATE', 'ALLSTATEshops COAST'),
      ('BOMBAY COAST', 'BOMBAY COAST'),
      ('BURGER KING', 'BURGER KING'),
      ('CHEF CHIN CONVOY', 'CHEF CHIN CONVOY'),
      ('CHEVRON', 'CHEVRON'),
      ('CHINA MAX', 'CHINA MAX'),
      ('DELTA AIR', 'DELTA AIR'),
      ('DENNY', 'DENNY'),
      ('DIM SUM KING', 'DIM SUM KING'),
      ('DNC TRAVEL - LAX C', 'DNC TRAVEL - LAX C'),
      ('EXXONMOBIL', 'EXXONMOBIL'),
      ('FOOD4LESS', 'FOOD4LESS'),
      ('GILBERT&#39;S FIREFISH GRI', 'GILBERT&#39;S FIREFISH GRI'),
      ('GROUPON INC', 'GROUPON INC'),
      ('LEMONADE', 'LEMONADE'),
      ('LITTLE SHEEP MONGOLIAN', 'LITTLE SHEEP MONGOLIAN'),
      ('MCDONALD', 'MCDONALD'),
      ('MOBO SUSHI', 'MOBO SUSHI'),
      ('PANDA EXPRESS', 'PANDA EXPRESS'),
      ('PEARL RESTAURANT', 'PEARL RESTAURANT'),
      ('PTICKET.COM-UC SAN DIEGO', 'PTICKET.COM-UC SAN DIEGO'),
      ('RALPHS', 'RALPHS'),
      ('RUBIO', 'RUBIO'),
      ('SANTORINI GREEK ISLAND', 'SANTORINI GREEK ISLAND'),
      ('SEARS ROEBUCK', 'SEARS ROEBUCK'),
      ('SHELL OIL', 'SHELL OIL'),
      ('SHOGUN OF LA JOLLA', 'SHOGUN OF LA JOLLA'),
      ('SOUPLANTATION', 'SOUPLANTATION'),
      ('STARBUCKS', 'STARBUCKS'),
      ('SUBWAY', 'SUBWAY'),
      ('TAPIOCA EXPRESS', 'TAPIOCA EXPRESS'),
      ('THE BOILING CRAB', 'THE BOILING CRAB'),
      ('TMC*TIME WARNER COM', 'TMC*TIME WARNER COM'),
      ('TRADER JOE', 'TRADER JOE'),
      ('UCSD HDH EARLS PLACE', 'UCSD HDH EARLS PLACE'),
      ('UCSD HDH GOODYS PLACE', 'UCSD HDH GOODYS PLACE'),
      ('UCSD POSTAL CENTER', 'UCSD POSTAL CENTER'),
      ('UCSD RECREATION', 'UCSD RECREATION'),
      ('UCSD TRITON SVCES', 'UCSD TRITON SVCES'),
      ('UCSD-BOOKSTORES', 'UCSD-BOOKSTORES'),
      ('WAL-MART', 'WAL-MART'),
      ('WHOLEFDS', 'WHOLEFDS'),
    ]

    for pattern, name in shops:
      if re.match(pattern, shop_name): return name

    return shop_name

  def get_shop_groups(self):
    shops = self.get_purchases()
    return shops.groupby(lambda i: self.normalize_shop_name(shops.ix[i].merchantName))

  def get_top_shops_by_avg_paid(self, num_shops_to_show = None):
    shops = self.get_shop_groups()
    avg_paid = shops.amount.mean()
    avg_paid.sort(ascending=False)

    if num_shops_to_show is None:
      return avg_paid
    else:
      return avg_paid[:num_shops_to_show]

  def get_top_shops_by_total_paid(self, num_shops_to_show = None):
    shops = self.get_shop_groups()
    totol_paid = shops.amount.sum()
    totol_paid.sort(ascending=False)

    if num_shops_to_show is None:
      return totol_paid
    else:
      return totol_paid[:num_shops_to_show]

  def get_top_shops_by_freq(self, num_shops_to_show = None):
    shops = self.get_shop_groups()
    by_freq = shops.amount.agg(lambda x: len(x))
    by_freq.sort(ascending=False)

    if num_shops_to_show is None:
      return by_freq
    else:
      return by_freq[:num_shops_to_show]

def read_posted_activities_to_df(fname):
  records = read_posted_activities(fname)
  return pandas.DataFrame.from_records(records)

if __name__ == '__main__':
  adf = read_posted_activities_to_df('my-chase-activities.json')
  ca = ChaseActivities(adf)
