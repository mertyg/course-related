import os
import struct
from ddl import create_file

MAX_FIELDS = 8
PAGESIZE = 1024
FILEPAGES = 8


def get_n_fields(tname):
    syscat = open("syscat", "rb")
    n_fields = 0
    #DatabaseID and N_Types
    syscat.seek(8, 0)
    name = syscat.read(8)
    #check the system catalogue for the number of fields
    while name != b'':
        name = struct.unpack("8s", name)[0].strip().decode("utf-8")
        if name == tname:
            is_alive = syscat.read(1)
            n_fields = struct.unpack("i", syscat.read(4))[0]
            break
        else:
            syscat.seek(1, 1)
            syscat.seek(4, 1)
            syscat.seek(8 * MAX_FIELDS, 1)
            name = syscat.read(8)
    syscat.close()
    return n_fields


def create_record(params):
    tname = params[0]
    f_size = len(params[1:-1])
    r_size = 1 + f_size * 4
    files = os.listdir()
    searchSpace = [f for f in files if (tname + "_file_") in f]
    written = False
    #buraya file header check etmek gelecek belki
    pos = 0
    for filename in searchSpace:
        file = open(filename, "r+b")

        filepos = 0
        pageno = 0
        page = file.read(PAGESIZE)
        #for the first page, the first 4 bytes are just the number of records.
        #we don't need them here.
        pos = 4
        while pageno < FILEPAGES:
            #empty spaces is in the beginning of the page
            emptySpaces = struct.unpack("i", page[pos:pos + 4])[0]
            pos += 4
            #if not enough space in the file for the record
            if emptySpaces < 1 + f_size * 4:
                page = file.read(PAGESIZE)
                pageno += 1
                filepos += PAGESIZE
                pos = 0
                continue
            while pos + r_size < PAGESIZE:
                record = page[pos:pos + r_size]
                full_flag = struct.unpack("1s",
                                          bytes(record[0:1]))[0].decode("utf-8")
                if full_flag == "F":
                    pos += r_size
                    continue
                else:
                    #preparing the record to write
                    format_list = ["i" for _ in range(f_size)]
                    format_list.insert(0, "1s")
                    format_list.insert(0, ">")
                    format_str = "".join(format_list)
                    fields = params[1:-1]
                    fields = [int(f) for f in fields]
                    fields.insert(0, b"F")
                    #print(fields)
                    record = struct.pack(format_str, *fields)
                    #preparing the modified page
                    if filepos == 0:
                        prev = page[8:pos]
                    else:
                        prev = page[4:pos]
                    after = page[pos + r_size:]
                    str_list = [
                        "i",
                        str(len(prev)) + "s",
                        str(r_size) + "s",
                        str(len(after)) + "s"
                    ]
                    content = [emptySpaces - r_size, prev, record, after]
                    if filepos == 0:
                        str_list.insert(0, "i")
                        n_records = struct.unpack("i", page[:4])[0]
                        content.insert(0, n_records + 1)
                    page_str = "".join(str_list)
                    new_page = struct.pack(page_str, *content)
                    #writing the modified page to its place in the file
                    file.seek(filepos, 0)
                    file.write(new_page)
                    file.close()
                    return
            #reading page by page
            page = file.read(PAGESIZE)
            pos = 0
            pageno += 1
            filepos += PAGESIZE
            #print("No space in page" + str(pageno))
        #print("No space in file" + filename)
        file.close()
    #print("No file with spaces")
    search_n = [int(f.split("_")[-1]) for f in searchSpace]
    i = 1
    while True:
        if i in search_n:
            i += 1
            continue
        else:
            break
    new_file = tname + "_file_" + str(i)
    create_file(new_file, f_size)
    create_record(params)


def delete_record(params):
    tname = params[0]
    n_fields = get_n_fields(tname)
    r_size = 1 + n_fields * 4
    filename, pageno, page_pos = search_record([tname, params[1], params[-1]],
                                               write_out=False)
    if filename is None:
        return

    #del_file = check_empty(filename)
    file = open(filename, "r+b")
    first_page = file.read(PAGESIZE)
    n_records = struct.unpack("i ", first_page[:4])[0]
    #print("In delete record, number of records: ", n_records)
    if n_records == 1:
        file.close()
        os.remove(filename)
        return

    file.seek(pageno * PAGESIZE, 0)
    page = file.read(PAGESIZE)
    empty_flag = struct.pack("1s", b"E")

    if pageno == 0:
        prev = page[4:page_pos]
    else:
        prev = page[:page_pos]
    after = page[page_pos + 1:]
    str_list = [str(len(prev)) + "s", str(1) + "s", str(len(after)) + "s"]
    content = [prev, empty_flag, after]

    if pageno == 0:
        str_list.insert(0, "i")
        n_records = struct.unpack("i", page[:4])[0]
        #print("Current n_records before decreasing: ", n_records)
        content.insert(0, n_records - 1)

    page_str = "".join(str_list)
    new_page = struct.pack(page_str, *content)
    #writing the modified page to its place in the file
    file.seek(pageno * PAGESIZE, 0)
    file.write(new_page)
    file.close()


def list_record(params):
    tname = params[0]
    n_fields = get_n_fields(tname)
    #record size is obtained
    r_size = 1 + n_fields * 4

    #outfile = open(params[-1], "r+")
    #Go to end of outfile
    #outfile.seek(0, 2)
    pos = 0
    record_list = []
    files = os.listdir()
    searchSpace = [f for f in files if (tname + "_file_") in f]
    for filename in searchSpace:
        file = open(filename, "r+b")
        pageno = 0
        page = file.read(PAGESIZE)
        #again, this is number of records only for the first page.
        page_pos = 4
        while pageno < FILEPAGES:
            emptySpaces = struct.unpack("i", page[page_pos:page_pos + 4])[0]
            page_pos += 4
            #if the file is empty
            if emptySpaces == 1020:
                pageno += 1
                page = file.read(PAGESIZE)
                page_pos = 0
                continue
            #while not EOF
            while page_pos + r_size < PAGESIZE:
                #slice the record
                record = page[page_pos:page_pos + r_size]
                page_pos += r_size
                r_pos = 0
                full_flag = struct.unpack(
                    "1s", record[r_pos:r_pos + 1])[0].decode("utf-8")
                r_pos += 1
                #if record is not full/alive.
                if full_flag != "F":
                    continue
                else:
                    w_record = []
                    for _ in range(n_fields):
                        #idk why, big endian works. check back later.
                        field = struct.unpack(">i", record[r_pos:r_pos + 4])[0]
                        r_pos += 4
                        w_record.append(str(field))
                    record_list.append(w_record)

            page = file.read(PAGESIZE)
            page_pos = 0
            pageno += 1
        #print("File searched: " + filename)
        file.close()
        outfile = open(params[-1], "r+")
        outfile.seek(0, 2)
        record_list = sorted(record_list, key=lambda x: int(x[0]))
        for i in range(len(record_list)):
            outfile.write(" ".join(record_list[i]).strip())
            outfile.write("\n")
        outfile.close()


def search_record(params, write_out=True):
    tname = params[0]
    n_fields = get_n_fields(tname)
    r_size = 1 + n_fields * 4
    search_key = int(params[1])
    files = os.listdir()
    searchSpace = [f for f in files if (tname + "_file_") in f]
    outfile = open(params[-1], "r+")
    outfile.seek(0, 2)
    for filename in searchSpace:
        file = open(filename, "rb")
        pageno = 0
        page = file.read(PAGESIZE)
        #Only for the first page this is n_records.
        page_pos = 4
        while pageno < FILEPAGES:
            emptySpaces = struct.unpack("i", page[page_pos:page_pos + 4])[0]
            page_pos += 4
            #if the file is empty
            if emptySpaces == 1020:
                pageno += 1
                page = file.read(PAGESIZE)
                page_pos = 0
                continue
            #while not EOF
            while page_pos + r_size < PAGESIZE:
                #slice the record
                record = page[page_pos:page_pos + r_size]
                page_pos += r_size
                r_pos = 0
                full_flag = struct.unpack(
                    "1s", record[r_pos:r_pos + 1])[0].decode("utf-8")
                #print(full_flag)
                r_pos += 1
                #if record is not full/alive.
                if full_flag != "F":
                    continue
                else:
                    key = struct.unpack(">i", record[r_pos:r_pos + 4])[0]
                    if key == search_key:
                        if not write_out:
                            file.close()
                            return filename, pageno, page_pos - r_size
                        for i in range(n_fields):
                            #idk why, big endian works. check back later.
                            field = struct.unpack(">i",
                                                  record[r_pos:r_pos + 4])[0]
                            r_pos += 4
                            outfile.write(str(field))
                            if i != n_fields - 1:
                                outfile.write(" ")
                        outfile.write("\n")
                        file.close()
                        outfile.close()
                        return filename, pageno, page_pos - r_size
            page = file.read(PAGESIZE)
            page_pos = 0
            pageno += 1
        #print("File searched in search_record: " + filename)
        file.close()
        outfile.close()
    return None, None, None


def update_record(params):
    tname = params[0]
    n_fields = len(params[1:-1])
    r_size = 1 + n_fields * 4
    #print("Update: ", params)
    filename, pageno, page_pos = search_record([tname, params[1], params[-1]],
                                               write_out=False)
    #print(params, filename, pageno, page_pos)
    if filename is None:
        return
    file = open(filename, "r+b")
    file.seek(pageno * PAGESIZE, 0)
    page = file.read(PAGESIZE)
    format_list = ["i" for _ in range(n_fields)]
    format_list.insert(0, "1s")
    format_list.insert(0, ">")
    format_str = "".join(format_list)
    fields = params[1:-1]
    fields = [int(f) for f in fields]
    fields.insert(0, b"F")
    record = struct.pack(format_str, *fields)
    #preparing the modified page
    prev = page[:page_pos]
    after = page[page_pos + r_size:]
    page_str = "".join(
        [str(len(prev)) + "s",
         str(r_size) + "s",
         str(len(after)) + "s"])
    content = [prev, record, after]
    new_page = struct.pack(page_str, *content)
    #writing the modified page to its place in the file
    file.seek(pageno * PAGESIZE, 0)
    file.write(new_page)
    file.close()
