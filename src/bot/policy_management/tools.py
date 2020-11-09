import gzip

def decode(file):
    fp = gzip.open('foo.gz')
    contents = fp.read() # contents now has the uncompressed bytes of foo.gz
    fp.close()
    u_str = contents.decode('utf-8') # u_str is now a unicode string