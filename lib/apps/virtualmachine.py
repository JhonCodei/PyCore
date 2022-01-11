"""
Description
-----------
"""
__version__ = '20210621'

import sys
import os
import time
import platform

from datetime import datetime

import proc.process      as p
import utils.fileutils   as fu
import utils.netutils    as nu
import utils.strutils    as su

#from utils.emailutils    import EmailUtils
#from transport           import sshutil

from apps.pybase        import _PyBaseApp
from statements.virtualmachine  import _SQLVirtualmachine

current_date     = datetime.now().strftime('%Y%m%d')
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')


class Virtualmachine(_PyBaseApp):

    def __init__(self):

        super(Virtualmachine, self).__init__()
        self.exitOnError = False

        # Environmental variables:
        self.env_vars = { }

        # Configuration variables:

        self.config = {
                        'virtualizadorWIND' : '',
                        'virtualizadorUNIX' : '',
                        'nombre_maquina-1'  : '',
                        'accion-1'          : '',
                        'tipo-1'            : '',
                      }

        self.callqry = _SQLVirtualmachine()
        self.em_cfg  = { }
        # Allowable commands for this application
        self.cmdStep = {
                        'X': self.iniciar_maquina_virtual,
                       } 
    # Use only for configuration values that need some manipulations/checks.
    def set_config_vars(self):
        # [if use 2 args in script file]
        if len(self.runSeq2) == 0: self.runSeq2 = 1

        self.virtualizadorWIND = self.config_vars[f"virtualizadorWIND"            ]
        self.virtualizadorUNIX = self.config_vars[f"virtualizadorUNIX"            ]
        self.nombre_maquina    = self.config_vars[f"nombre_maquina-{self.runSeq2}"]
        self.accion            = self.config_vars[f"accion-{self.runSeq2}"        ]
        self.tipo              = self.config_vars[f"tipo-{self.runSeq2}"          ]

        return 0

    #####################################
    ######## VIRTUALMACHINE ###############
    #####################################

    def setear_comando_accion(self, accion):
        if accion == 'i' : return "startvm", "Iniciando Maquina virtual"
        else             : return "", "Mensaje"

    def tipo_accion_condicion(self, tipo):
        comando = f"--type="
        return f"{comando}{tipo}"
        

    def iniciar_maquina_virtual(self):
        
        if platform.system() == "Windows": ejecutable = self.virtualizadorWIND
        else                             : ejecutable = self.virtualizadorUNIX

        accion, msj  = self.setear_comando_accion(self.accion)
        tipo         = self.tipo_accion_condicion(self.tipo)

        comando = f'"{ejecutable}" {accion} {tipo} {self.nombre_maquina}'

        self.log.info(f"{msj} {self.nombre_maquina}")
        rc, msg = p.run_sync(comando, self.log) ## running commads
        return rc

    def test(self):
        ret = 0
        print("123-test")
        return ret

def main(Args):

    a = Virtualmachine()
    rc = a.main(Args)
    return rc

if __name__ == '__main__':

    rc = main(sys.argv)
    sys.exit(rc)
