
for line in open('init_config.py').readlines():
    exec(line)

dset = DataSet()
print(dset._data)