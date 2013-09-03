#!/usr/bin/env python3

import cx_Oracle
import nysiis
import csv

writer = csv.writer(open('names.csv','w'))

con = cx_Oracle.connect(user='HRIT_PEOPLE', password='P30pl350ft')
cur = con.cursor()

cur.execute("""
select distinct person_id, name_display from D_PERSON
join (
	select emp_id from D_POI where poi_type = 10035
	union all
	select emp_id from D_JOB where emp_status not in ('X')
) using (emp_id)
""")
rows =[]
for i,name in cur.fetchall(): 
  f = nysiis.nysiis(name)
  if len(f) > 1:
    row = (i, f)
    rows.append( row )

writer.writerows(rows)
