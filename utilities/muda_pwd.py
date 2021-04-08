"""
Esta script gera uma password aleatória para um aluno e manda a password por email.
"""

def muda_pwd(user):
    """Esta função recebe o nome de um utilizador que já existe e atribui-lhe uma palavra chave aleatória

    PARAMETERS
    ----------
    user: str
        O utilizador

    Esta função envia também a palavra chave por email.
    """
    import glob, crypt, os, random, string
    try:
        os.rename(f"{user}/.data.tcl", f"{user}/.data.tcl.old")
    except:
        pass
    with open(f"{user}/.class.tcl", "w") as f:
        print('return Team', file = f)
    with open(f"{user}/.data.tcl", "w") as f:
        pwd = ''.join(random.choice(string.ascii_letters) for i in range(8))
        email = f"{user}@alunos.uminho.pt"
        print(f"""set        Fatal {{}}
set      Warning {{}}
set         Name {user}
set     Password {crypt.crypt(pwd, "pg")}
set        Email {{{email}}}
set     Location {{}}
set    Qualifies {{}}
set       Person {{}}
set        Start {{}}
set         Rank {{}}
set      Profile team""", file = f)
        texto = f"""
        Caro aluno,
        Eis as suas credenciais para entrar no MOOshak:
        Utilizador: {user}
        Password:   {pwd}
        
        Iremos a partir de agora utilizar este sistema para as fichas de AASB.

        Cumprimentos,

        --Rui Mendes
        """
        attachment = f'/tmp/{user}.txt'
        with open(attachment, 'w') as F_Email:
            print(texto, file = F_Email)
        email += " rcm@di.uminho.pt"
        os.system(f'mutt -s "[AASB] Password do MOOshak" {email} < {attachment}')
    return (user, pwd, email)

if __name__ == '__main__':
    import sys
    print(muda_pwd(sys.argv[1]))
