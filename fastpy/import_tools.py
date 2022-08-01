import importlib

imported = {}


def import_class(path: str):
    """
    Imports Python classes

    :param path: Python classpath (separated by ".")
    :return: Python class
    """

    if path in imported.keys():
        return imported.get(path)

    components = path.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    imported.update({path: mod})
    return mod
