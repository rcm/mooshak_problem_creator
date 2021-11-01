example = """#	Id	Group	Name	A	B	C	Z	Solved	Points 
1	pg45963	UM	pg45963	100 (1)	100 (3)	100 (2)	100 (1)		400 
2	pg45474	UM	pg45474	100 (1)	100 (3)	100 (3)	100 (1)		400 
3	pg45469	UM	pg45469	100 (3)	100 (2)	94 (5)	100 (1)		394 
4	pg45458	UM	pg45458	100 (3)	100 (10)	59 (13)	100 (1)		359 
5	pg45466	UM	pg45466	100 (1)	80 (1)	59 (1)	100 (1)		339 
6	pg45970	UM	pg45970	100 (2)	90 (5)	41 (1)	100 (2)		331 
7	pg45461	UM	pg45461	100 (1)	80 (4)	41 (1)	100 (1)		321 
8	pg42879	UM	pg42879	100 (2)	100 (7)	0 (3)	100 (1)		300 
9	pg45464	UM	pg45464	100 (9)	100 (5)	100 (1)	 		300 
10	pg45473	UM	pg45473	100 (1)	90 (12)	100 (1)	 		290 
11	pg45971	UM	pg45971	100 (4)	85 (7)	100 (2)	 		285 
12	pg45964	UM	pg45964	100 (11)	80 (9)	0 (1)	100 (2)		280 
13	pg45467	UM	pg45467	100 (5)	100 (2)	59 (12)	 		259 
14	pg45962	UM	pg45962	100 (4)	90 (9)	62 (2)	 		252 
15	pg43176	UM	pg43176	100 (2)	80 (1)	68 (2)	 		248 
16	pg45463	UM	pg45463	100 (1)	100 (3)	41 (3)	 		241 
17	pg45472	UM	pg45472	100 (2)	80 (2)	59 (2)	 		239 
18	pg42861	UM	pg42861	100 (1)	85 (2)	41 (3)	 		226 
19	pg45969	UM	pg45969	100 (7)	80 (3)	41 (2)	 		221 
20	pg45965	UM	pg45965	100 (9)	80 (6)	41 (6)	 		221 
21	pg45475	UM	pg45475	100 (2)	100 (2)	0 (4)	 		200 
22	pg42486	UM	pg42486	100 (1)	80 (3)	19 (2)	 		199 
23	pg45459	UM	pg45459	100 (5)	80 (2)	 	17 (2)		197 
24	pg45477	UM	pg45477	100 (1)	90 (3)	0 (2)	 		190 
25	pg42882	UM	pg42882	100 (4)	90 (4)	0 (6)	 		190 
26	pg45476	UM	pg45476	100 (5)	85 (3)	 	 		185 
27	pg45967	UM	pg45967	100 (11)	80 (3)	0 (9)	 		180 
28	pg45468	UM	pg45468	50 (19)	50 (4)	59 (4)	 		159 
29	pg44580	UM	pg44580	50 (6)	0 (1)	 	100 (4)		150 
30	pg45968	UM	pg45968	50 (11)	80 (3)	0 (1)	 		130 
31	pg45465	UM	pg45465	50 (13)	80 (7)	0 (1)	 		130 
32	pg44380	UM	pg44380	5 (1)	 	 	 		5 
33	pg45462	UM	pg45462	0 (5)	0 (4)	 	 		0 
34	pg27665	UM	pg27665	 	 	 	 		0 

"""

def read_rankings(text):
    import re
    header = None
    table = []
    for l in text.splitlines():
        if l.strip() != "":
            l = re.sub(r'\s+\(\d+\)', '', l)
            fields = l.split('\t')
            id = fields[1]
            campos = [x if re.sub(r'\s+', '', x) else '0' for x in fields[4:-2]]
            total = fields[-1]
            if header is None:
                header = campos
            else:
                dic = {k : v for k, v in zip(header + 'id total'.split(), campos + [id, total])}
                table.append(dic)

    return table

def print_table(table, select = None, format_total = None):
    import io
    with io.StringIO() as F:
        if format_total is None:
            format_total = lambda x: x
        if select is None:
            select = ['id'] + sorted(fld for fld in table[0].keys() if fld not in {'id','total'})
        else:
            select = ['id'] + select if 'id' not in select else select
        print(*[f"{x:8}" for x in select], "total".center(8), sep = " | ", file = F)
        print(*["-" * 8 for x in select], "-"*8, sep = " | ", file = F)
        for line in sorted(table, key = lambda l: l['id']):
            total = sum(int(line[k]) for k in select if k != 'id')
            print(*[f"{line[k]:>8}" for k in select], f"{format_total(total):>8}", sep = " | ", file = F)

        F.seek(0)
        return F.read()

import markdown
res = print_table(read_rankings(example), select = "A B C".split(), format_total = lambda x: f"{20 * x / 300:.2f}")
print(markdown.markdown(res, extensions=['tables']))
