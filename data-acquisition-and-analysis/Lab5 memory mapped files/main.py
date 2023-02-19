import mmap
import timeit

FILENAME = "file2.txt"

def regular_io():
    with open(FILENAME, mode="r", encoding="utf8") as file_obj:
        text = file_obj.read()
        text.find("13906")

def mmap_io():
    with open(FILENAME, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            mmap_obj.find(b"13906")

def main():
    print("OUTPUT FOR REGULAR SEARCH: ", timeit.repeat(
         "regular_io()",
         repeat=3,
         number=1,
         setup="from __main__ import regular_io"))

    print("OUTPUT FOR MEMORY MAPPED FILE: ", timeit.repeat(
         "mmap_io()",
         repeat=3,
         number=1,
         setup="from __main__ import mmap_io"))

if __name__ == "__main__":
    main()

