from abc import ABCMeta, abstractmethod
from django.db import models
from typing import Any
import django
from django.forms import ValidationError
from numpy import char
from pandas import DataFrame
from custom_orm.helper import orm_db
import re



regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def create_db(name):
    return orm_db.create_db(name)



class OrmFields(metaclass=ABCMeta):
    
    @abstractmethod
    def validate(self):
        pass

class IntegerField(OrmFields):
    
    def __init__(self, val=None):
        self.value = self.validate(val)


    def validate(self, val):
        if val == None:
            pass
        else:
            try:
                val = int(val)
                return val
            except Exception as e:
                raise ValidationError(e)


class CharField(OrmFields):
    
    validator_dict = dict()
    def __init__(self, val=None, max_length=None):
        self.value = self.validate(val, max_length)
        self.max_length = max_length

    def validate(self, val, max_len):
        if val == None:
            pass
        elif not isinstance(val, str):
            raise ValidationError("value should be character")
        elif len(val) > max_len:
            raise ValidationError("length should be less than or equal to {len}".format(len=max_len))
        return val

class EmailField(OrmFields):
    def __init__(self, val=None):
        self.value = self.validate(val)

    def validate(self, val):
        global regex
        if val == None:
            pass
        elif not (re.fullmatch(regex, val)) :
            raise ValidationError("value should be email")
        return val
 



class ModelBase(type): ...
    

class QuerySet:
    def __init__(self, df, cls):
        self.df = df
        self.cls = cls
        self.i = 0
    def __iter__(self):
        return self

    def __next__(self):
        if self.i > 0:
            raise StopIteration()
        self.i += 1
        return self

    def obj_filter(self, **kwargs):
        #filtered_query = self.df['age']==25
        # filtered_query = filtered_query.reset_index(drop=True)
        # print(type(filtered_query))
        query_string= ""
        for key, val in kwargs.items():
            if type(val) == str:
                query_string += key+"=='"+val+"' and "
            else:
                query_string += key+"=="+str(val) + " and "
        query_string += "True"
        df2 = self.df.query(query_string)
        return df2

class Model(metaclass=ModelBase):

    #class_attributes: to store all the Field types that belong to the base class(Model)
    class_attributes = {}
    table_name = ""
    def __init__(self, *args, **kwargs):
        self.attributes = dict()
        #for every field that belongs to the class,if it is present in the kwargs(while creating objects),
        #  then initialize that FieldType
        for key, val in self.class_attributes.items():
            if key in kwargs:
                if val[0] == CharField:
                    var_value = val[0](kwargs[key], val[1])
                else:
                    var_value = val[0](kwargs[key])
                self.attributes[key] = var_value
                kwargs.pop(key)

        #checking if incorrect field names are entered by the user
        if len(kwargs)>0:
            error_string = ""
            for key in kwargs.keys():
                error_string += key+", "
            error_string = error_string[:-2]
            raise ValidationError(error_string+ " is/ are not accepted by table")
        self.df = DataFrame()
    
    


    """
    create_table: 
        input_params: cursor
        creates a table with the provided class name, if doesn't exists
    """
    @classmethod
    def create_table(cls, cursor):
        print(" create table ")
        cls.cursor = cursor
        attributes_str = " id SERIAL PRIMARY KEY, "
        for key, val in cls.__dict__.items():
            cls.class_attributes[key] = (type(val), )
            if isinstance(val, CharField):
                cls.class_attributes[key] = (type(val), val.max_length)
                attributes_str += (key + " varchar ({len}), ".format(len=val.max_length))
            if isinstance(val, IntegerField):
                attributes_str += key + " int, "
            if isinstance(val, EmailField):
                attributes_str += key + " text, "
        attributes_str = attributes_str[:-2]
        attributes_str =  "("+attributes_str+");"
        sql = "CREATE table IF NOT EXISTS {name} ".format(name=cls.table_name)
        sql = sql + attributes_str
        #Creating a database
        cursor.execute(sql)


    """
    save: it inserts the data of the object in db on which it is called
    """
    def save(self, *args, **kwargs):
        attributes = "("
        values = ""
        for key, field_obj in self.attributes.items():
            attributes += key + ", "
            val = "'%s'"%field_obj.value
            values += str(val) + ", "
        attributes = attributes[:-2]
        values = values[:-2]
        attributes += ") values (" + values + ")"
        insert_sql = "INSERT INTO {table} ".format(table=self.__class__.table_name)
        insert_sql +=  attributes 
        print(insert_sql)
        self.cursor.execute(insert_sql)

    @classmethod
    def filter(cls, **kwargs):
        select_sql = "SELECT * FROM {table} where ".format(table=cls.table_name)
        conditional_statement = ""
        for key, val in kwargs.items():
            conditional_statement += key + "=" + "'{val}', ".format(val=val)
        conditional_statement = conditional_statement[:-2]
        conditional_statement += ";"
        select_sql += conditional_statement
        cls.cursor.execute(select_sql)
        def fetch_records():
                
            ans = cls.cursor.fetchall()
            objs = []
            # klass = globals()[cls.__name__]
            # instance = klass()
            
            fields_names = [i[0] for i in cls.cursor.description]
            data = [dict(zip(fields_names, row))  for row in ans]
            # for row in data:
            #     a = cls.__new__(cls)
            #     print(a.__init__(row))
            # print(objs)
            df = DataFrame(ans, columns=fields_names)
            q = QuerySet(df, cls.table_name)
            return q
        return fetch_records

    

    def update(self, **kwargs):
        pass

