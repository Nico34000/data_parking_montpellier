#pylint: disable=E0401
import logging
import os
from pymongo import MongoClient
from backend.function.parse_xml import create_dict
from backend.function.dict_url import dict_url

HOST = os.environ["HOST_MONGO_DB"]
PASSWORD = os.environ["PASSWORD_MONGO_DB"]
SERVER = os.environ["SERVER_MONGO_DB"]


def connect_db(host, password, server):
  """ This function connect in atlas a mongodb
  """
  client = MongoClient(f"mongodb+srv://{host}:{password}@{server}?ssl=true&"\
                       "ssl_cert_reqs=CERT_NONE")
  logging.info(" %s client : ", client)
  conn = client.test
  logging.info(" your database : %s", conn)
  database = conn["Parking"]
  return database


def insert_rows(database):
  """This function insert rows in the database
  mongodatabase
  database : is the database want to be inserted
  """
  values = create_dict(dict_url())
  logging.info("%s this is the values add in database", values)
  return database.insert(values)


def remove(database):
  """ This function remove all rows in database mongodatabase
  """
  logging.info("remove all rows in database mongodatabase")
  return database.remove({})


def result_database(database):
  """ This function return the result with all
  name in parking. They return a dict
  """
  res = {}
  for i in dict_url():
    for rows in database.find({}, {i}):
      logging.info("this is all rows in database :  %s", rows)
      parking = i
      res[parking] = rows.get(i)
  logging.info("this is your dict with the value in db %s", res)
  return dict(sorted(res.items()))


def main_db():
  """
  This is the main function to call
  all other functions
  """
  print("[*]Start of database initialization")
  my_db = connect_db(HOST, PASSWORD, SERVER)
  remove(my_db)
  insert_rows(my_db)
  result_database(my_db)
  print("[*]The initialization of the database is completed")