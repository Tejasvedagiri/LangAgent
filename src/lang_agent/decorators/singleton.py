def singleton_with_variable(cls):
    """
    Decorator to create a singleton class with a variable.

    Args:
        cls: The class to be decorated.

    Returns:
        The decorated class.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance