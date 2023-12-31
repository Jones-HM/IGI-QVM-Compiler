from .ops import *


OPMAP = {
    b'\x00': BRK,
    b'\x01': NOP,
    b'\x02': PUSH,
    b'\x03': PUSHB,
    b'\x04': PUSHW,
    b'\x05': PUSHF,
    b'\x06': PUSHA,
    b'\x07': PUSHS,
    b'\x08': PUSHSI,
    b'\x09': PUSHSIB,
    b'\x0a': PUSHSIW,
    b'\x0b': PUSHI,
    b'\x0c': PUSHII,
    b'\x0d': PUSHIIB,
    b'\x0e': PUSHIIW,
    b'\x0f': PUSH0,
    b'\x10': PUSH1,
    b'\x11': PUSHM,
    b'\x12': POP,
    b'\x13': RET,
    b'\x14': BRA,
    b'\x15': BF,
    b'\x16': BT,
    b'\x17': JSR,
    b'\x18': CALL,
    b'\x19': ADD,
    b'\x1a': SUB,
    b'\x1b': MUL,
    b'\x1c': DIV,
    b'\x1d': SHL,
    b'\x1e': SHR,
    b'\x1f': AND,
    b'\x20': OR,
    b'\x21': XOR,
    b'\x22': LAND,
    b'\x23': LOR,
    b'\x24': EQ,
    b'\x25': NE,
    b'\x26': LT,
    b'\x27': LE,
    b'\x28': GT,
    b'\x29': GE,
    b'\x2a': ASSIGN,
    b'\x2b': PLUS,
    b'\x2c': MINUS,
    b'\x2d': INV,
    b'\x2e': NOT,
    b'\x2f': BLK,
    b'\x30': ILLEGAL,
}