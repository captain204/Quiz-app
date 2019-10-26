from config import *
#Database queries functions


def insert(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()


def select(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchone()
    return data

def select_all(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data

def update(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

def delete(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close



