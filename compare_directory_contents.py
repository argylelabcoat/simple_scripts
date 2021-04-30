from multiprocessing import Process, Lock, Pool, cpu_count
import hashlib
import os, shutil
import gdbm

BLOCKSIZE = 65536
dblocks = {}
dbfor = {}

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def hash_and_save(dir_path, file_path):
    file_hash = hash_file(file_path)

    dblocks[dir_path].acquire()
    db = gdbm.open(dbfor[dir_path], 'c')
    db[file_hash]=file_path
    db.sync()
    db.close()
    dblocks[dir_path].release()

def hash_and_save_tpl(tpl):
    dir_path, file_path = tpl
    hash_and_save(dir_path, file_path)

def hash_every_file(dir_path):
    to_hash = []
    for root, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                to_hash.append((dir_path, file_path))
    
    
    pool = Pool(processes=cpu_count()-2)
    pool.map(hash_and_save_tpl, to_hash)

def compare_dirs(dir_a, dir_b):
    db_a = gdbm.open(dbfor[dir_a], 'r')
    db_b = gdbm.open(dbfor[dir_b], 'r')

    a_not_in_b = []
    b_not_in_a = []
    # first check a into b:
    k = db_a.firstkey()
    while k != None:
        if not k in db_b:
            a_not_in_b.append(k)
        k = db_a.nextkey(k)

    # next check b into a:
    k = db_b.firstkey()
    while k != None:
        if not k in db_a:
            b_not_in_a.append(k)
        k = db_b.nextkey(k)

    print("\n"+"="*50+"MISSING FROM B")
    missing_a = os.path.join(dir_b,"missing_from_compare")
    os.makedirs(missing_a)
    for k in a_not_in_b:
        file_name = db_a[k]
        rel_path = os.path.relpath(file_name, dir_a)
        if not os.path.exists(os.path.join(missing_a, os.path.dirname(rel_path))):
            os.makedirs(os.path.join(missing_a, os.path.dirname(rel_path)))
        base_name = os.path.basename(file_name)
        dest_name = os.path.join(missing_a, rel_path)
        shutil.copyfile(file_name, dest_name)
        print(k, file_name, dest_name)
    
    print("\n"+"="*50+"MISSING FROM A")
    missing_b = os.path.join(dir_a,"missing_from_compare")
    os.makedirs(missing_b)
    for k in b_not_in_a:
        file_name = db_b[k]
        rel_path = os.path.relpath(file_name, dir_b)
        if not os.path.exists(os.path.join(missing_b, os.path.dirname(rel_path))):
            os.makedirs(os.path.join(missing_b, os.path.dirname(rel_path)))
        base_name = os.path.basename(file_name)
        dest_name = os.path.join(missing_b, rel_path)
        print(k, file_name, dest_name)
        shutil.copyfile(file_name, dest_name)

    db_a.close()
    db_b.close()
    
def perform_comparison(dir_a, dir_b):
    dblocks[dir_a] = Lock()
    dblocks[dir_b] = Lock()

    db_a = os.path.basename(os.path.normpath(dir_a))+".db"
    db_b = os.path.basename(os.path.normpath(dir_b))+".db"
    dbfor[dir_a] = db_a
    dbfor[dir_b] = db_b

    hash_every_file(dir_a)
    hash_every_file(dir_b)

    compare_dirs(dir_a, dir_b)


if __name__ == '__main__':
    import sys
    perform_comparison(sys.argv[1],sys.argv[2])