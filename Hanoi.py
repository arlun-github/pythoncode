count = 1
def test(num, src, dst, rest):
    global count
    if num < 1:
        print("ilegal param")
    elif num == 1:
        print("{}:\t{} -> {}" .format(count, src, dst))
        count += 1
    elif num > 1:
        test(num - 1, src, rest, dst)
        test(1, src, dst, rest)
        test(num - 1, rest, dst, src)
    
           
test(10,'A','C','B')
print("total count{}".format(count-1))
