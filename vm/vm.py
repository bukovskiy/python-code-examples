"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import dis
import types
import typing as tp
import builtins


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.6/Include/frameobject.h#L17

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """
    def __init__(self, frame_code, frame_builtins, frame_globals, frame_locals):
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack = []
        self.return_value = None

    def top(self):
        return self.data_stack[-1]

    def pop(self):
        return self.data_stack.pop()

    def push(self, *values):
        self.data_stack.extend(values)

    def popn(self, n):
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self):
        for instruction in dis.get_instructions(self.code):
            getattr(self, instruction.opname.lower() + "_op")(instruction.argval)
        return self.return_value

    def call_function_op(self, arg):
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-CALL_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L3121
        """
        arguments = self.popn(arg)
        f = self.pop()
        self.push(f(*arguments))

    def load_name_op(self, arg):
        """
        Partial realization

        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-LOAD_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L2057
        """
        # TODO: parse all scopes
        self.push(self.locals[arg])

    def load_global_op(self, arg):
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-LOAD_GLOBAL

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L2108
        """
        # TODO: parse all scopes
        self.push(self.builtins[arg])

    def load_const_op(self, arg):
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-LOAD_CONST

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1088
        """
        self.push(arg)

    def return_value_op(self, arg):
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-RETURN_VALUE

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1641
        """
        self.return_value = self.pop()

    def pop_top_op(self, arg):
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-POP_TOP

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1102
        """
        self.pop()

    def make_function_op(self, arg):
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-MAKE_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L3203

        Parse stack:
            https://github.com/python/cpython/blob/3.7/Objects/call.c#L158

        Call function in cpython:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L4554
        """
        name = self.pop()  # the qualified name of the function (at TOS)
        code = self.pop()  # the code associated with the function (at TOS1)

        # TODO: use arg to parse function defaults

        def f(*args, **kwargs):
            # TODO: parse input arguments using code attributes such as co_argcount

            parsed_args = {}
            f_locals = dict(self.locals)
            f_locals.update(parsed_args)

            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            return frame.run()

        self.push(f)

    def store_name_op(self, arg):
        """
        Operation description:
            https://docs.python.org/3/library/dis.html#opcode-STORE_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.7/Python/ceval.c#L1923
        """
        const = self.pop()
        self.locals[arg] = const


class VirtualMachine:
    def run(self, code_text_or_obj: tp.Union[str, types.CodeType]) -> None:
        """
        :param code_text_or_obj: code for interpreting
        """
        globals_context = {}
        frame = Frame(code_text_or_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()
