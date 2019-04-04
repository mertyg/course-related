import struct
import os
MAX_FIELDS = 8
PAGESIZE = 1024
FILEPAGES = 8


def create_type(params):
    filename = params[-1]
    syscat = open("syscat", "r+b")
    syscat.read(4)
    types = struct.unpack("i", syscat.read(4))[0]
    syscat.seek(4, 0)
    syscat.write(struct.pack("i", types + 1))
    syscat.seek(8, 0)
    name = syscat.read(8)
    while name != b'':
        name = struct.unpack("8s", name)[0].strip().decode("utf-8")
        is_alive = struct.unpack("1s", syscat.read(1))[0].decode("utf-8")
        if is_alive == "0":
            #n_fields = struct.unpack("i", syscat.read(4))[0]
            syscat.seek(-9, 1)
            break
        #number of fields
        syscat.seek(4, 1)
        syscat.seek(MAX_FIELDS * 8, 1)
        name = syscat.read(8)
    t_name = "{:8s}".format(params[0])
    syscat.write(struct.pack("8s", bytes(t_name, "utf-8")))
    syscat.write(struct.pack("1s", b"1"))  #is_alive
    syscat.write(struct.pack("i", int(params[1])))
    for f_name in params[2:]:
        f_name = "{:8s}".format(f_name)
        syscat.write(struct.pack("8s", bytes(f_name, "utf-8")))
    for _ in range(MAX_FIELDS - len(params[2:])):
        f_name = "{:8s}".format("")
        syscat.write(struct.pack("8s", bytes(f_name, "utf-8")))
    syscat.close()


def create_file(filename, n_fields):
    n_fields = int(n_fields)
    r_size = 4 * n_fields + 1
    file = open(filename, "w")
    file.close()
    file = open(filename, "r+b")
    #emptySpace = struct.pack("i", PAGESIZE-4)
    page_strs = []
    page_records = []
    #Create format string for each record.
    #Each will have the form of:
    #Full/Empty information(1 byte) and fields (n_fields*4) bytes
    format_list = ["i" for _ in range(n_fields)]
    format_list.insert(0, "1s")
    format_str = "".join(format_list)
    fields = [0 for _ in range(n_fields)]
    fields.insert(0, b"E")

    first_page_strs = []
    first_page_records = []
    pos = 8
    while (pos + r_size < PAGESIZE):
        record = struct.pack(format_str, *fields)
        first_page_strs.append(str(r_size) + "s")
        first_page_records.append(record)
        pos += r_size
    if PAGESIZE - pos > 0:
        first_page_strs.append(str(PAGESIZE - pos) + "s")
        first_page_records.append(b"")
    first_page_strs.insert(0, "i")
    first_page_records.insert(0, 1020)
    first_page_strs.insert(0, "i")
    first_page_records.insert(0, 0)
    first_page = struct.pack("".join(first_page_strs), *first_page_records)
    file.write(first_page)

    #creating other pages.
    pos = 4
    while (pos + r_size < PAGESIZE):
        record = struct.pack(format_str, *fields)
        page_strs.append(str(r_size) + "s")
        page_records.append(record)
        pos += r_size
    if PAGESIZE - pos > 0:
        page_strs.append(str(PAGESIZE - pos) + "s")
        page_records.append(b"")
    page_strs.insert(0, "i")
    page_records.insert(0, 1020)
    page = struct.pack("".join(page_strs), *page_records)
    for i in range(FILEPAGES - 1):
        file.write(page)
    file.close()


def delete_type(params):
    type_to_delete = params[0]
    files = os.listdir()
    files_to_delete = [f for f in files if (type_to_delete + "_file_") in f]
    for f in files_to_delete:
        os.remove(f)
    syscat = open("syscat", "r+b")
    syscat.read(4)
    types = struct.unpack("i", syscat.read(4))[0]
    syscat.seek(8, 0)
    name = syscat.read(8)
    while name != b'':
        name = struct.unpack("8s", name)[0].strip().decode("utf-8")
        if name == type_to_delete:
            syscat.write(struct.pack("1s", b"0"))
            syscat.seek(4, 0)
            syscat.write(struct.pack("i", types - 1))
            syscat.close()
            break
        #is_alive information
        syscat.read(1)
        #n_fields
        syscat.read(4)
        syscat.read(MAX_FIELDS * 8)
        name = syscat.read(8)
    syscat.close()


def list_type(params):
    syscat = open("syscat", "r+b")
    outfile = open(params[-1], "r+")
    #Go to end of outfile
    outfile.seek(0, 2)
    syscat.seek(4, 0)
    types = struct.unpack("i", syscat.read(4))[0]
    name = syscat.read(8)
    types = []
    while name != b"":
        name = struct.unpack("8s", name)[0].strip().decode("utf-8")
        is_alive = struct.unpack("1s", syscat.read(1))[0].decode("utf-8")
        if is_alive == "1":
            types.append(name)
        syscat.seek(4, 1)
        syscat.seek(MAX_FIELDS * 8, 1)
        name = syscat.read(8)
    syscat.close()
    types = sorted(types)
    for name in types:
        outfile.write(name)
        outfile.write("\n")
    outfile.close()