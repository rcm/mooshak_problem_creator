import tabulate
import markdown
import sys
import re

def read_rankings(selected = None):
    tab = []
    headers = None
    for line in sys.stdin:
        line = re.sub(r'\(\d+\)', '', line)
        fields = line.split('\t')
        if headers is None:
            headers = [f.strip() for f in fields]
            if selected is None:
                selected = headers
        else:
            fields = [f.strip() if f.strip() else 0 for f in fields]
            tab_line = {k : v for k, v in zip(headers, fields) if k in selected}
            if not tab_line: continue
            for k in tab_line:
                if re.match('^([A-Z]|Points)$', k):
                    tab_line[k] = int(tab_line[k])
            tab_line["Nota"] = tab_line["Points"] / 300 * 20
            tab.append(tab_line)
    return tab

tab = read_rankings(selected = "Id A B C Points".split())
print(tabulate.tabulate(tab, headers="keys"))
