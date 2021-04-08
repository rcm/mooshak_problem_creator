import sys
import mooshak
import markdown
import importlib

def ended(line):
    return len(line) == 0 or line.strip() == 'END'

def get_block(F, line, frame):
    ret = None
    
    while not ended(line):
        if ret is None:
            ret = ''
        else:
            ret += line
        line = F.readline()
    return ret

def get_description(F, line, frame):
    return markdown.markdown(get_block(F, line, frame))

def add_input(frame, line):
    if 'INPUTS' not in frame:
        frame['INPUTS'] = []
    frame['INPUTS'].append(line)
    return ('INPUTS', frame['INPUTS'])

def get_input(F, line, frame):
    line = ' '.join(line.split()[1:])
    return add_input(frame, line)
    
def get_longinput(F, line, frame):
    line = get_block(F, line, frame)
    return add_input(frame, line)

def get_input_generator(F, line, frame):
    fields = line.split()
    num = 1
    if len(fields) == 3:
        keyword, num, generator = fields
        num = int(num)
        line = f"{keyword} {generator}"
    generator = get_function(F, line, frame)
    for i in range(num):
        ret = add_input(frame, generator())
    return ret

def get_tests(F, line, frame):
    ret = frame.get('TESTS', [])
    fall_though = ["IMPORT"]
    frm = {F : frame[F] for F in frame if F in fall_though}
    ret.append(parser(F, frame = frm, handler = {'INPUT' : get_input, 'LONGINPUT' : get_longinput, 'INPUTGEN' : get_input_generator}))
    return ('TESTS', ret)

def get_function(F, line, frame):
    tokens = line.split()
    if len(tokens) == 2:
        key, fun = tokens
        fun = fun.strip()
        if fun in globals():
            return globals()[fun]
        elif any(fun in dir(M) for M in frame['IMPORT'].values()):
            for M in frame['IMPORT'].values():
                if fun in dir(M):
                    return getattr(M, fun)
        else:
            raise Exception(f'Function {fun} not found!')           
    else:
        fun = ' '.join(tokens[1:])
        assert tokens[1] == 'lambda', f"Error parsing function '{fun}'"
        attempt = fun.split(':')
        assert len(attempt) > 1, f"Error parsing function '{fun}'"
        ret = eval(fun)
        assert callable(ret), f"Error parsing function '{fun}'"
        return ret

def do_imports(F, line, frame):
    key, module = line.split()
    if 'IMPORT' not in frame:
        frame['IMPORT'] = {}
    frame['IMPORT'][module] = importlib.import_module(module)
    return ('IMPORT', frame['IMPORT'])
    
def parser(File, frame = None, handler = None, line = '\n'):
    if frame is None:
        frame = {}
    if handler is None:
        handler = {}
        
    while not ended(line):
        if len(line.strip()) > 0:
            keyword, *rest = line.strip().split()

            if keyword not in handler:
                frame[keyword] = ' '.join(rest)
            else:
                res = handler[keyword](File, line, frame)
                assert callable(res) or type(res) is str or (type(res) is tuple and len(res) == 2), f"Bad result from handler of {keyword}: {res}"
                if type(res) is tuple:
                    keyword, value = res
                    frame[keyword] = value
                else:
                    frame[keyword] = res

        line = File.readline()
        
    return frame

def do_code(F, line, frame):
    code = get_block(F, line, frame)
    import hashlib
    mod_hash = hashlib.md5(code.encode()).hexdigest()
    spec = importlib.util.spec_from_loader(mod_hash, loader = None)
    module = importlib.util.module_from_spec(spec)
    exec(code, module.__dict__)
    if 'IMPORT' not in frame:
        frame['IMPORT'] = {}
    frame['IMPORT'][mod_hash] = module
    return ('IMPORT', frame['IMPORT'])
    

    
def parse_problem(FHandler):
    res = parser(FHandler, handler = {
        'SOLVER'        : get_function,
        'DESCRIPTION'   : get_description,
        'TESTS'         : get_tests,
        'IMPORT'        : do_imports,
        'CODE'          : do_code,
        })
    if len(res) == 0:
        return
    
    fields = "name letter description solver".split()
    dic = {field : res[field.upper()] for field in fields if field.upper() in res}
    p = mooshak.Problem(**dic)
    for T in res['TESTS']:
        fields = "INPUTS FEEDBACK POINTS SHOW".split()
        dic = {field.lower() : T[field] for field in fields if field in T}
        p.add_tests(**dic)
    if 'POINTS' in res:
        p.assign_points(int(res['POINTS']))
    p.create_files()
    return p

def parse(filename, encoding = "UTF8"):
    with open(filename, encoding = encoding) as FHandler:
        while (p := parse_problem(FHandler)) is not None:
            print(p)
            import os, webbrowser
            filename = f'{p.folder}/description.html'
            webbrowser.open(f'file://{os.path.realpath(filename)}')

    
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            print(f'Parsing {file}')

            parse(file)
    else:
        example = 'exemplo_generator.txt'
        print(f'Parsing example file {example}')
        parse(example)
    
