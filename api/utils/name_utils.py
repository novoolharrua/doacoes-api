#!/usr/bin/env python
# -*- coding: utf-8 -*


names_enum = {
    'CLOTHING': 'ROUPAS',
    'FOOD': 'COMIDA',
    'RELIGION': 'RELIGIÃO',
    'OTHERS': 'OUTROS',
}

def translate_name(name):
    return names_enum.get(name, name)
