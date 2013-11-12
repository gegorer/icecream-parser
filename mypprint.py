import pprint
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('UTF-8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

