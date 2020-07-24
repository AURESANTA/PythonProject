#!/usr/bin/env python3

from string import ascii_letters, digits
from itertools import chain
from random import choice
import sqlite3
import os

def create_uid(n=9):
   '''Génère une chaîne de caractères alétoires de longueur n
   en évitant 0, O, I, l pour être sympa.'''
   chrs = [ c for c in chain(ascii_letters,digits)
                        if c not in '0OIl'  ]
   return ''.join( ( choice(chrs) for i in range(n) ) )

def save_code_as_file(uid=None,code=None, language=None):
    ''' Enregistrement en BDD
    '''
    if uid is None:
        uid = create_uid()
        print('test')
        print(uid)
        with sqlite3.connect("sharecode.db") as conn:
            curs = conn.cursor()
            curs.execute('INSERT INTO code (content,language) VALUES(?,?)',
                         (code, language))
            conn.commit()

def read_code_as_file(uid):
    '''Lit le document data/langage/uid'''
    with sqlite3.connect("sharecode.db") as conn:
        curs = conn.cursor()
        curs.execute('SELECT content, language FROM code WHERE uid= ?', (uid,))

    result = curs.fetchone()
    return result

def read_all_codes():
    with sqlite3.connect("sharecode.db") as conn:
        curs = conn.cursor()
        curs.execute('SELECT uid, content,language FROM code')

    result = curs.fetchall()
    return result