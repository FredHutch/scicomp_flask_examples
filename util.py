

class OnlyOne:
    class __OnlyOne:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne(arg)
        else:
            OnlyOne.instance.val = arg
    def get_val(self):
        return OnlyOne.instance.val
    def __getattr__(self, name):
        return getattr(self.instance, name)


def set_db(db):
    if OnlyOne.instance is None:
        OnlyOne(db)

def get_db():
    return OnlyOne.instance


# set_db("foo")
# print(get_db())
# set_db("bar")
# print(get_db())
