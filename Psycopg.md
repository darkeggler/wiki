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

PEP 249 -- Python Database API Specification v2.0

## Introduction
This API has been defined to encourage similarity between the Python modules that are used to access databases. By doing this, we hope to achieve a consistency leading to more easily understood modules, code that is generally more portable across databases, and a broader reach of database connectivity from Python.

This document describes the Python Database API Specification 2.0 and a set of common optional extensions. The previous version 1.0 version is still available as reference, in PEP 248 . Package writers are encouraged to use this version of the specification as basis for new interfaces.

psycopg2模块提供了PostgreSQL数据库的python接口，该接口与其它的数据库接口类似，均兼容PEP 249描述的DB-API 2.0规范，因此它们无论是看起来都还是用起来都很像。

## Module Interface
### Constructors
Access to the database is made available through connection objects. The module must provide the following constructor for these:
- - -
connect ( parameters... )
- - -
Constructor for creating a connection to the database.

Returns a Connection Object. It takes a number of parameters which are database dependent. [1]

规范要求通过connection对象访问数据库。因此模块中需提供形如`connect ( parameters... )`的构造器。构造器用于创建数据库连接，返回connection对象。这里需要注意的是构造器所需参数依赖于特定的数据库。
- - -
```python
psycopg2.connect(dsn=None, connection_factory=None, cursor_factory=None, async=False, **kwargs)
```

Create a new database session and return a new connection object.

在psycopg2中连接参数有两种形式，其即可将libpq规定的连接字符串直接赋予dsn参数，亦可把字符串拆开了赋给一组键值参数，即使混搭也是可以的。但不管怎么样，至少得有一个参数。当然提供两种形式的参数并不像看起来这样的自然。

The connection parameters can be specified as a libpq connection string using the dsn parameter:
```python
conn = psycopg2.connect("dbname=test user=postgres password=secret")`
```
or using a set of keyword arguments:
```python
conn = psycopg2.connect(dbname="test", user="postgres", password="secret")
```
or using a mix of both: if the same parameter name is specified in both sources, the kwargs value will have precedence over the dsn value. Note that either the dsn or at least one connection-related keyword argument is required.

The basic connection parameters are:

*	dbname – the database name (database is a deprecated alias)
*	user – user name used to authenticate
*	password – password used to authenticate
*	host – database host address (defaults to UNIX socket if not provided)
*	port – connection port number (defaults to 5432 if not provided)

五常以外的参数需参考PostgreSQL文档。environment variables是什么？以后再说吧。

Any other connection parameter supported by the client library/server can be passed either in the connection string or as a keyword. The PostgreSQL documentation contains the complete list of the supported parameters. Also note that the same parameters can be passed to the client library using environment variables.

connection_factory & cursor_factory 可以假装看不见。

Using the connection_factory parameter a different class or connections factory can be specified. It should be a callable object taking a dsn string argument. See Connection and cursor factories for details. If a cursor_factory is specified, the connection’s cursor_factory is set to it. If you only need customized cursors you can use this parameter instead of subclassing a connection.

最后，异步也不是说懂就能懂的东西。

Using `async=True` an asynchronous connection will be created: see Asynchronous support to know about advantages and limitations. async_ is a valid alias for the Python version where async is a keyword.

Changed in version 2.4.3: any keyword argument is passed to the connection. Previously only the basic parameters (plus sslmode) were supported as keywords.

DB API extension:  The non-connection-related keyword parameters are Psycopg extensions to the DB API 2.0.
_____________________________________

### Globals
These module globals must be defined:
- - -
apilevel
- - -
String constant stating the supported DB API level.

Currently only the strings " 1.0 " and " 2.0 " are allowed. If not given, a DB-API 1.0 level interface should be assumed.
* * *
psycopg2.apilevel

    String constant stating the supported DB API level. For psycopg2 is 2.0.
____________________________________

## Connection Objects
Connection objects should respond to the following methods.

`class connection`

    Handles the connection to a PostgreSQL database instance. It encapsulates a database session.

    Connections are created using the factory function connect().

    Connections are thread safe and can be shared among many threads. See Thread and process safety for details.

Connection methods
________________________________________
.close()

Close the connection now (rather than whenever .__del__() is called).

The connection will be unusable from this point forward; an Error (or subclass) exception will be raised if any operation is attempted with the connection. The same applies to all cursor objects trying to use the connection. Note that closing a connection without committing the changes first will cause an implicit rollback to be performed.
________________________________________
close()

Close the connection now (rather than whenever del is executed). The connection will be unusable from this point forward; an InterfaceError will be raised if any operation is attempted with the connection. The same applies to all cursor objects trying to use the connection. Note that closing a connection without committing the changes first will cause any pending change to be discarded as if a ROLLBACK was performed (unless a different isolation level has been selected: see set_isolation_level()).

    Changed in version 2.2: previously an explicit ROLLBACK was issued by Psycopg on close(). The command could have been sent to the backend at an inappropriate time, so Psycopg currently relies on the backend to implicitly discard uncommitted changes. Some middleware are known to behave incorrectly though when the connection is closed during a transaction (when status is STATUS_IN_TRANSACTION), e.g. PgBouncer reports an unclean server and discards the connection. To avoid this problem you can ensure to terminate the transaction with a commit()/rollback() before closing.
________________________________________
________________________________________
.commit ()

Commit any pending transaction to the database.

Note that if the database supports an auto-commit feature, this must be initially off. An interface method may be provided to turn it back on.

Database modules that do not support transactions should implement this method with void functionality.
________________________________________
commit()

By default, Psycopg opens a transaction before executing the first command: if commit() is not called, the effect of any data manipulation will be lost.

The connection can be also set in “autocommit” mode: no transaction is automatically open, commands have immediate effect. See Transactions control for details.

Changed in version 2.5: if the connection is used in a with statement, the method is automatically called if no exception is raised in the with block.
________________________________________
________________________________________
.rollback ()

This method is optional since not all databases provide transaction support. [3]

In case a database does provide transactions this method causes the database to roll back to the start of any pending transaction. Closing a connection without committing the changes first will cause an implicit rollback to be performed.
________________________________________
rollback()

Roll back to the start of any pending transaction. Closing a connection without committing the changes first will cause an implicit rollback to be performed.

Changed in version 2.5: if the connection is used in a with statement, the method is automatically called if an exception is raised in the with block.
________________________________________
________________________________________
.cursor ()

Return a new Cursor Object using the connection.

If the database does not provide a direct cursor concept, the module will have to emulate cursors using other means to the extent needed by this specification. [4]
________________________________________
cursor(name=None, cursor_factory=None, scrollable=None, withhold=False)

Return a new cursor object using the connection.

If name is specified, the returned cursor will be a server side cursor (also known as named cursor). Otherwise it will be a regular client side cursor. By default a named cursor is declared without SCROLL option and WITHOUT HOLD: set the argument or property scrollable to True/False and or withhold to True to change the declaration.

The name can be a string not valid as a PostgreSQL identifier: for example it may start with a digit and contain non-alphanumeric characters and quotes.

Changed in version 2.4: previously only valid PostgreSQL identifiers were accepted as cursor name.

Warning: It is unsafe to expose the name to an untrusted source, for instance you shouldn’t allow name to be read from a HTML form. Consider it as part of the query, not as a query parameter.

The cursor_factory argument can be used to create non-standard cursors. The class returned must be a subclass of psycopg2.extensions.cursor. See Connection and cursor factories for details. A default factory for the connection can also be specified using the cursor_factory attribute.

DB API extension: All the function arguments are Psycopg extensions to the DB API 2.0.
________________________________________
