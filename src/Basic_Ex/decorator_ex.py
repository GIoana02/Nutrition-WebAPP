from Mydecorators import my_decorator, do_twice, do_twice_with_args

def say_hello():
    print("Hello!")

say_hello=my_decorator(say_hello)
say_hello()


def say_whee():
    print("Helloooo!")

say_whee=do_twice(say_whee)
say_whee()
@do_twice_with_args
def jump(*args, **kwargs):
    for idx in args:
        print(idx)

    for key in kwargs:
        print(key)

jump(1,5, a=6, b=9)



