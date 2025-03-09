# У файлов должны быть одинаковые форматы
n = open("file1", "rb")
out = open("file2", "wb")
out.write(n.read())
out.close()
n.close()
