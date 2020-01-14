filename = '__tests__/logs/log.log'


result = []
pos = []
while True:
    try:
        with open(filename, 'rb') as f:
            for p, s in pos:
                f.read(p)
                f.read(s)
            a = f.read()
        a.decode('utf-16-be')
        break
    except UnicodeDecodeError as err:
        # print(err)
        msg = err.__str__()
        st = ''
        i = 49
        while True:
            s = msg[i]
            if s == ':':
                break
            st += s
            i += 1
        first, second = map(int, st.split('-'))
        pos.append( (first, second-first) )
        # print(pos)
print(pos)


with open(filename, 'rb') as f:
    for p, s in pos:
        result.append(f.read(p))
        f.read(s)
    result.append(f.read())

# result = list(map(lambda x: x.decode('utf-16-be'), result))
print(len(result))
result = (b''.join(result)).split(b'\r\n')
print(len(result))
result = [i for i in result if b'Mixed Content' not in i]
print(len(result))
result = b''.join(result)
print(len(result))


with open('__tests__/logs/l.log', 'w', encoding='utf-16-be') as f:
    f.write(result.decode('utf-16-be'))
