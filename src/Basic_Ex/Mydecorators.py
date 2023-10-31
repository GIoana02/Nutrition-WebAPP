def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called")
        func()
        print("Something is happening after the function is called")

    return wrapper

def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice


def do_twice_with_args(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return  wrapper_do_twice