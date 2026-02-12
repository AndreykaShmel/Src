def split_string(s, group_size):
    return [s[i:i + group_size] for i in range(0, len(s), group_size)]

slowar = {'0': '0000',
          '1': '0001',
          '2': '0010',
          '3': '0011',
          '4': '0100',
          '5': '0101',
          '6': '0110',
          '7': '0111',
          '8': '1000',
          '9': '1001',
          '+': '1010',
          '-': '1011',
          '*': '1100',
          '/': '1101',
          ',': '1110',
          '.': '1111'}
st = '6.02214'
binary_st = ''
for num in st:
    binary_st += slowar[num]
list = split_string(binary_st, 2)
slowar = {
    '00': 'A',
    '01': 'C',
    '10': 'G',
    '11': 'T',
}
cepochka = ''
for pair in list:
    cepochka += slowar[pair]
print(st)
print(cepochka)

gen = 'GGAGTCTCCTCAGGATAATTATTTATTATTCATAGTCATCAGCATCTTCATTAATTATTCATATGATCCTTAATTATTATCCTTAACAATAAGAGCAGTAAATAGCAGAAAAGTCCTTGAGGTGCCTAAGGCCCAGGGCCGGGTGCCTCCGGGCAGTTAGACCAGCTAATGCCCTCAGGGCAGTGGGGGGACCACAGGCCCCACCTACTGCCGGCCCTGCCCCTGCCCCTCTCACTGGGGCCCAGGGGACTGCAGGAGAAGATGGTCCCAAGGGCTGGGGGAGGAGCTGTGCTTTCGAGTTCCTCTCCCCTTCCACGGTCAGGGCCTCCTGAGCAGGGCCTCCAAGGGGAGCGGCCCAGCAGCGCCTTGATCCCTG'
try_st = ''
curency = 1
popravka = 1/len(cepochka)
for i in range(len(gen) - len(cepochka)):
    for j in range(i, i + len(cepochka)):
        try_st += gen[j]
    for k in range(len(try_st)):
        if try_st[k] != cepochka[k]:
            curency -= popravka
    if curency >= 0.5:
        print('Эврика')
        print(try_st)
        print(cepochka)
        print('точночть =', curency)
    try_st = ''
    curency = 1
