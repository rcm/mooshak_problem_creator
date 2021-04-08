def dna_codons(dna):
    import re
    return ' '.join(re.findall(r'...', dna))

def dna_translate_frame(dna):
    gencode = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}
    return ''.join(gencode[codon.upper()] for codon in dna_codons(dna).split())

def inverse_complement(dna):
    dir = 'ATCG'
    inv = 'TAGC'
    dna = dna[::-1].lower()
    
    for b, i in zip(dir, inv):
        dna = dna.replace(b.lower(), i)
    return dna
        

def reading_frames(dna):
    res = []
    for i in range(3):
        res .append( dna_translate_frame(dna[i:]) )
    revcomp = inverse_complement(dna)
    for i in range(3):
        res .append( dna_translate_frame(revcomp[i:]) )
    return '\n'.join(res)

def open_reading_frames(dna):
    import re
    res = sorted({p  for x in reading_frames(dna).splitlines()
                   for p in re.findall('M.*?_', x)},
                  key = lambda s: (-len(s), s))
    return '\n'.join(res)

    
