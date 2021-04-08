"""
Esta script gera uma password aleatória para cada aluno e manda a password por email.
"""

import glob
from muda_pwd import muda_pwd

with open('lista.txt', 'w') as F:
    for user in sorted(glob.glob("pg*")):
        print(*muda_pwd(user), file = F)
