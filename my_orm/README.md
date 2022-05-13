# MyOrm

my_orm: it is Object Relational Mapper using which we can create a db, table for that db and perform read, create, and update operations on the table.

## Steps for setting up
1. clone the repository
2. pip install -r requirements.txt
3. python3 manage.py runserver
    - hit the ep: ```http://localhost:8000/orm_testing```
    - the above LOC will create a db named my_db and a table called Author and will save an author object which is retrieved using filter and the object is edited and save() is called on that object which will save the updated object in the db.


## Functionalities supported by MyOrm
Db creation: orm.create_db(<db_name>)

Table creation: 

    - create a model in models.py (Author) and inherit orm.Model and provide the field  names and their types and also the table_name.
        - Filed Types: IntegerField, CharField, EmailField
        - validation: 
            IntegerField : the value should be int type
            CharField : provide the max_len, and it will check if the len is less than equal to max_len and if it is of type str
            EmailField :  regex is defined and the value will be validated accordingly.

Create a python object 
```a = Author(name="sadbhavana", age=25, email="sadbhavanahk@gmail.com")```
Save the object in db by calling ```a.save()```. It has an upsert query which will insert the data if it is a new entry and will update the data if it already exists using "id" as the deciding key.

Filter the data using ```author = Author.filter(name="sadbhavana")```
    - *field name validation*.
    
    - *lazy evaluation*. filter() returns an inner function which needs to be called to hit the db.  ```a = author()```. a has all the filtered db records.

    - filter() returns Queryset object on which we can call **obj_filter(email="sadbhavana@gmail.com")**. which will return a queryset object

    - if you want to access any object call ```s = a.objs[0]```

    - *update an object* access the object using ``` a.attributes['email'] = orm.EmailField("sharda@gmail.com") ```. Assign the values of types which have inherited **OrmFields**. and call save() method which will update the data in db.




# as per reuirements:
### Your simple ORM should be able to

- Create DB tables based on class definitions: **Done**
- Create table rows by instantiating a class and calling `save` method: **Done**
- Filter (SELECT) data based on exact matching: **Done**
- Update existing rows: **Done**
- Prevent users from entering wrong field names: **Done**
- Handle at least 3 field types including CharField and IntegerField: **Done**

### You will get extra points if your ORM can

- Validate field types: **Done**
- Filter the result of an already filtered data: **Done**
- Support lazy query evaluation (refer to the example below): **Done**
- Handle foreign keys. (Relational DB): **Not Done**
- Automatically detects schema changes (migrations): **Not Done**
- Be used across multiple threads without causing unnecessary blocking: **Not Done**
    - If your choice of language is Golang, use `select`