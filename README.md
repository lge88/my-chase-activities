
## Acquire Data ##
Requirement: Google Chrome, cUrl, gzip

- Login to chase online bank.
- Credit Card -> See activity.
- In Google Chrome menu, Tools -> Developer Tools.
- In Developer Tool panel, select 'network' tab.
- In Chase online bank activity page, find 'Posted Activity' section,
  select 'All Transactions' in the dropdown menu.
- In Developer Tool Network tab, find the 'Get' request just sent,
  the endpoint should be '/cc/Account'.
- Right click the '/cc/Account' row, select 'Copy as Curl'.
- Open terminal, paste the curl commands just copied into terminal,
  then append some commands:

  `[curl commands from Chrome] | gzip -d > my-chase-activities.json`
- The above will create a file named 'my-chase-activities.json'.

## Parse Data ##
Requirement: python

- parse_chase_activity_data.py

  `records = read_posted_activities('my-chase-activities.json')`

## Analysis & Visualize Data ##
Requirement: python, pandas

- analyze_chase_activity_data.py

  ```python

     cas = ChaseActivities(records)
     cas.get_top_shops_by_freq()
     cas.get_top_shops_by_total_paid()
     cas.get_top_shops_by_avg_paid()
     
  ```
