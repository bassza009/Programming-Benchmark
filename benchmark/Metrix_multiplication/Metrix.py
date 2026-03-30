n = 500
a = [[1.0 for _ in range(n)] for _ in range(n) ]
b = [[2.0 for _ in range(n)] for _ in range(n) ]
def MatrixMul( mtx_a, mtx_b):
    tpos_b = zip( *mtx_b)
    rtn = [[ sum( ea*eb for ea,eb in zip(a,b)) for b in tpos_b] for a in mtx_a]
    return rtn


v = MatrixMul( a, b )

print( 'v = (')
for r in v:
    print ('['), 
    for val in r:
        print ( '%8.2f '%val), 
    print (']')
print (')')


u = MatrixMul(b,a)

print ('u = ')
for r in u:
    print ('['), 
    for val in r:
        print ('%8.2f '%val), 
    print (']')
print (')')