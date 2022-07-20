# import time
#
#
# def speed_calc_decorator(function):
#     def calculate_time():
#         time_start = time.time()
#         function()
#         time_end = time.time()
#         durration = time_end - time_start
#         print(f"{function.__name__} speed is {durration}")
#     return calculate_time
#
#
# def slow_function():
#     for i in range(100000000):
#         i * i
#
# @speed_calc_decorator
# def fast_function():
#     for i in range(1000000):
#         i * i
#
#
#
# first_function = speed_calc_decorator(slow_function)
#
# fast_function()
#
#
# first_function()


# Create the logging_decorator() function 👇
def logging_decorator(function):
    def use_function(*args):
        function(args[0])
        print(args[0])
        return f"Function args: {args[0]}, function name {function.__name__}"
    return use_function


# Use the decorator 👇
@logging_decorator
def print_name(name):
    print(f"your name is: {name}")


print_name("Asta")

def make_bold(function):
    def use_function():
        return f"<b> {function()}</b>"
    return use_function


def make_italic(function):
    def use_function():
        return f"<em> {function()}</em>"
    return  use_function