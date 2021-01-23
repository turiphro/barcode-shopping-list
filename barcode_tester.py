#/usr/bin/env python3
import pprint

from src.api.resolvers.albert_heijn import AlbertHeijnResolver
from src.api.resolvers.commands import CommandResolver

resolvers = [AlbertHeijnResolver(), CommandResolver()]

while True:
    barcode = input("> ")
    title = info = None
    for resolver in resolvers:
        try:
            title, info = resolver.resolve(barcode)
            break
        except Exception as e:
            print("! cannot resolve barcode:", str(e))
    print(title)
    #pprint.pprint(info)
