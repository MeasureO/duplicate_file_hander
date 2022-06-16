import sys
import os
import hashlib
import pprint


def read_file(file):
    """Reads en entire file and returns file bytes."""
    
    #нужно добавить возможность читать только первый
    #мегабайт файла для ускорения работы на больших файлах
    
    buf_size = 16384  # 16 kilo bytes
    b = b""
    with open(file, "rb") as f:
        while True:
            # read 16K bytes from the file
            bytes_read = f.read(buf_size)
            if bytes_read:
                # if there is bytes, append them
                b += bytes_read
            else:
                # if not, nothing to do here, break out of the loop
                break
    return b


try:
    dir = sys.argv[1]
    size_root = {}
    print("Enter file format:")
    file_format = input()
    print("\nSize sorting options:")
    print("1. Descending")
    print("2. Ascending")
    print("\nEnter a sorting option:")
    while True:
        sorting_option = input()
        if sorting_option not in ('1', '2'):
            print("Wrong option")
            continue
        else:
            break
    new_ans = {}
    for root, dirs, files in os.walk(dir):
        for name in files:
            if size_root.get(os.path.getsize(os.path.join(root, name))) is None:
                size_root[os.path.getsize(os.path.join(root, name))] = [os.path.join(root, name)]
            else:
                size_root[os.path.getsize(os.path.join(root, name))].append(os.path.join(root, name))
    if sorting_option == '1':
        ans = dict(sorted(size_root.items(), reverse=True))
    elif sorting_option == '2':
        ans = dict(sorted(size_root.items()))
    for elem in ans:
        new_ans[elem] = [i for i in ans[elem] if i.endswith(file_format)]
        print(f'\n{elem} bytes')
        arr = [i for i in ans[elem] if i.endswith(file_format)]
        print(*arr, sep='\n')
    # print(new_ans)
    print("\nCheck for duplicates?")
    d = {}
    del_dict = {}
    while True:
        duplicate_option = input()
        if duplicate_option not in ('yes', 'no'):
            print("Wrong option")
            continue
        else:
            if duplicate_option == "yes":
                n = 1
                for size in new_ans.keys():
                    for elem in new_ans[size]:
                        # print(elem)
                        file_content = read_file(elem)
                        h = hashlib.md5(file_content).hexdigest()
                        #print(h)
                        if (size, h) not in d.keys():
                            d[(size, h)] = [elem]
                        else:
                            d[(size, h)].append(elem)
                # pprint.pprint(d)
                last_count = 0
                for elem in d:
                    if len(d[elem]) > 1:
                        if elem[0] != last_count:
                            print(f'\n{elem[0]} bytes')
                            last_count = elem[0]
                        print(f'Hash: {elem[1]}')
                        for i in range(len(d[elem])):
                            print(f'{n}. {d[elem][i]}')
                            del_dict[n] = (d[elem][i], elem[0])
                            n += 1
        break
    # print(del_dict)
    print("\nDelete files?")
    while True:
        delete_option = input()
        if delete_option not in ('yes', 'no'):
            print("Wrong option")
            continue
        elif delete_option == 'no':
            break
        elif delete_option == 'yes':
            print("\nEnter file numbers to delete:")
            while True:
                numbers = input()
                if numbers == '':
                    print("\nWrong format")
                    continue
                else:
                    try:
                        numbers = list(map(int, numbers.split()))
                    except:
                        print("\nWrong format")
                        continue
                for i in range(len(numbers)):
                    if numbers[i] > n and numbers[i] < 0:
                        print("\nWrong format")
                        continue
                break
            print(numbers)
            freed_space = 0
            for i in numbers:
                if os.path.exists(del_dict[i][0]):
                    os.remove(del_dict[i][0])
                    freed_space += del_dict[i][1]
                else:
                    print("The file does not exist")
            print(f'Total freed up space: {freed_space} bytes')
except IndexError:
    print("Directory is not specified")
