import duckdb, sys
con = duckdb.connect()
con.execute("set memory_limit='6GB'; set threads=4; install httpfs; load httpfs; install spatial; load spatial; set s3_region='us-west-2';")
q = """
copy (
select id, names.primary as name, brand.wikidata as brand_wikidata, brand.names.primary as brand_name,
       basic_category as category, taxonomy.primary as tax, operating_status, confidence, sources[1].dataset as src, sources[1].license as lic,
       st_x(geometry) as lon, st_y(geometry) as lat
from read_parquet('s3://overturemaps-us-west-2/release/2026-10-21.0/theme=places/type=place/*', hive_partitioning=1)
where bbox.xmin between 139.55 and 139.95 and bbox.ymin between 35.50 and 35.83
  and (brand.wikidata = 'Q259340'
       or regexp_matches(coalesce(names.primary,'') || ' ' || coalesce(brand.names.primary,''), '(?i)セブン.?イレブン|7.?eleven|seven.?eleven'))
) to 'overture_seven.csv' (header)
"""
con.execute(q)
print(con.execute("select count(*), count(*) filter (where brand_wikidata='Q259340') from 'overture_seven.csv'").fetchall())
print(con.execute("select category, count(*) from 'overture_seven.csv' group by 1 order by 2 desc limit 10").fetchall())
print(con.execute("select src, lic, operating_status, count(*) from 'overture_seven.csv' group by all order by 4 desc").fetchall())
