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
    
    def __init__(self, val=None, max_length=None):
        self.max_length = max_length
        self.value = self.validate(val, max_length)
        self.max_length = max_length

    def validate(self, val, max_len):
        if val == None:
            pass
        elif val != None and (not isinstance(val, str) or not isinstance(val, str or len(val) > max_len)):
            raise ValidationError("value should be character")
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
    


class Model(metaclass=ModelBase):

    class_attributes = {}
    def __init__(self, *args, **kwargs):
        self.attributes = dict()
        
        for key, val in self.class_attributes.items():
            if key in kwargs:
                var_value = val(kwargs[key], )
                self.attributes[key] = var_value
                kwargs.pop(key)

        if len(kwargs)>0:
            error_string = ""
            for key in kwargs.keys():
                error_string += key+" "
            raise ValidationError(error_string+ " is/ are not accepted by {table}".format(self.__class__.table_name))
        self.df = DataFrame()


    table_name = ""
    # manager_class = BaseManager
    
    # def _get_manager(cls):
    #     return cls.manager_class(model_class=cls)

    # @property
    # def objects(cls):
    #     return cls._get_manager()

    

    @classmethod
    def create_table(cls, cursor):
        print(" create table ")
        cls.cursor = cursor
        attributes_str = " id SERIAL PRIMARY KEY, "
        for key, val in cls.__dict__.items():
            cls.class_attributes[key] = type(val)
            if isinstance(val, CharField):
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
        cls.cursor.execute(sql)

    def save(self, *args, **kwargs):
        print(self.__dict__)
        attributes = "("
        values = ""
        print("*************")
        for key, field_obj in self.attributes.items():
            print(field_obj.value)
            #value = "'%s'"%value
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
        ans = cls.cursor.fetchall()
        objs = []
        # klass = globals()[cls.__name__]
        # instance = klass()
        
        fields_names = [i[0] for i in cls.cursor.description]
        data = [dict(zip(fields_names, row))  for row in ans]
       
        return data

    

    def update(self, **kwargs):
        pass

class BaseManager:

    def __init__(self, model_class):
        self.model_class = model_class
        self.cursor = orm_db.create_db

    def select(self, *field_names):
        query = f"SELECT * FROM {self.model_class.table_name}"

        # Execute query
        self.model_class.table_name
        self.cursor.execute(query)

    def bulk_insert(self, rows: list):
        pass

    def update(self, new_data: dict):
        pass

    def delete(self):
        pass

