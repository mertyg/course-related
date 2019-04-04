import sys
import struct
import os
from ddl import create_type, delete_type, list_type
from dml import create_record, search_record, update_record, delete_record, list_record
MAX_FIELDS = 8
PAGESIZE = 1024
FILEPAGES = 8


def handle_operation(op, params):
    if op == "create_type":
        create_type(params)

    elif op == "delete_type":
        delete_type(params)

    elif op == "list_type":
        list_type(params)

    elif op == "create_record":
        create_record(params)

    elif op == "delete_record":
        delete_record(params)

    elif op == "update_record":
        update_record(params)

    elif op == "search_record":
        search_record(params)

    elif op == "list_record":
        list_record(params)

    else:
        print("Invalid operation", op.split("_"))


def init_db():
    files = os.listdir()
    if "syscat" in files:
        return
    f = open("syscat", "a+b")
    #DatabaseID
    f.write(struct.pack("i", 5))
    #Number of types
    f.write(struct.pack("i", 0))
    f.close()


def check_syscat():
    file = open("syscat", "r+b")
    print("DB ID:", struct.unpack("i", file.read(4))[0])
    print("Type Count ", struct.unpack("i", file.read(4))[0])
    file.close()


if __name__ == '__main__':
    init_db()
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    outf = open(out_file, "wb")
    outf.close()
    inp = open(in_file, "r")
    for line in inp:
        tokens = line.strip().split()
        operation = "_".join(tokens[:2])
        tokens.append(out_file)
        handle_operation(operation, tokens[2:])
    # DONT FORGET TO REMOVE THIS
    #os.remove("syscat")
