
def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances.update({cls: cls(*args, **kwargs)})
        return instances[cls]

    return wrapper
