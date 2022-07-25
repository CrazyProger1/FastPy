import importlib

imported = {}


def import_class(name):
    if name in imported.keys():
        return imported.get(name)

    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    imported.update({name: mod})
    return mod
