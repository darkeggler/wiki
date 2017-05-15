```python
>>> import psycopg2

# Connect to an existing database
>>> conn = psycopg2.connect("dbname=test user=postgres")

# Open a cursor to perform database operations
>>> cur = conn.cursor()

# Execute a command: this creates a new table
>>> cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
>>> cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
...      (100, "abc'def"))

# Query the database and obtain data as Python objects
>>> cur.execute("SELECT * FROM test;")
>>> cur.fetchone()
(1, 100, "abc'def")

# Make the changes to the database persistent
>>> conn.commit()

# Close communication with the database
>>> cur.close()
>>> conn.close()
```

psycopg2模块提供了PostgreSQL数据库的python接口，该接口与其它的数据库接口类似，均兼容PEP 249描述的DB-API 2.0规范，因此它们无论是看起来都还是用起来都很像。

### Constructors
规范要求通过connection对象访问数据库。因此模块中需提供形如`connect ( parameters... )`的构造器。构造器用于创建数据库连接，返回connection对象。这里需要注意的是构造器所需参数依赖于特定的数据库。
```python
psycopg2.connect(dsn=None, connection_factory=None, cursor_factory=None, async=False, **kwargs)
```
在psycopg2中连接参数有两种形式，其即可将libpq规定的连接字符串直接赋予dsn参数，亦可把字符串拆开了赋给一组键值参数，即使混搭也是可以的。但不管怎么样，至少得有一个参数。当然提供两种形式的参数并不像看起来这样的自然。
```python
conn = psycopg2.connect("dbname=test user=postgres password=secret")`
```
```python
conn = psycopg2.connect(dbname="test", user="postgres", password="secret")
```
五常以外的参数需参考PostgreSQL文档。environment variables是什么？以后再说吧。connection_factory & cursor_factory 可以假装看不见。最后，异步也不是说懂就能懂的东西。因此我们只要知道主机地址、端口号、数据库名及其用户名、密码就行了。

### Connection Objects
连接对象最重要的方法