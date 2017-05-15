# _*_ coding:utf-8 _*_

import psycopg2
from if_xmldb import collection_video, collection_page

with psycopg2.connect(dbname="mydb", 
    user="darkeggler", 
    password="baoJ2015",
    host="133.81.128.199",
    port=5432) as conn:
    
    cur = conn.cursor()
    cur.execute(
        """insert into t_webdata (imsi, phonetype, nettype, pagesurftime, location) 
        values (%s,%s,%s,%s,ST_GeographyFromText('SRID=4326;POINT(%s %s)'));""",
        (460020123456789,"hw","LTE","2017-03-01 10:37:16.513",108.86549,34.23000))
    conn.commit()

#f = r"D:\工作空间_2017\90.业务感知\apps\source\陕西_20170306_group_02-01.xml"
#[i.text for i in m.iter()]

mask='001010000000110010010111111111111110111111111111111'
m1 = np.array([True if i == '1' else False for i in list(mask)])
np.array([(i.tag, i.text) for i in m.iter()])[m1]

'''
CREATE TABLE t_webdata
(
  imsi bigint,
  phonetype text,
  location geography(Point,4326),
  city text,
  nettype nettype,
  cdmasid smallint,
  cdmanid smallint,
  cdmabsid integer,
  cdmadbm numeric(5,2),
  lteci integer,
  ltepci smallint,
  ltetac smallint,
  ltersrp numeric(5,2),
  ltesinr smallint,
  innerip inet,
  outerip inet,
  ecio numeric(5,2),
  snr numeric(5,2),
  ltersrq numeric(5,2),
  websitename text,
  pageurl text,
  pageip inet,
  pagesurftime timestamp(3) without time zone,
  firstbytedelay smallint,
  pageopendelay smallint,
  rrcsetupdelay smallint,
  dnsdelay smallint,
  conndelay smallint,
  reqdelay smallint,
  resdelay smallint,
  tclass smallint,
  success smallint,
  dnsip inet,
  pagesize integer,
  pageavgspeed integer,
  filedate timestamp without time zone
)
'''

