#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Curso de Elementos de Sistemas
# Desenvolvido por: Rafael Corsi <rafael.corsi@insper.edu.br>
#
# Adaptado de :     Pedro Cunial   <pedrocc4@al.insper.edu.br>
#                   Luciano Soares <lpsoares@insper.edu.br>
# Data de criação: 07/2017
##################################################
from os.path import join, dirname
import sys
import os
import shutil
import subprocess

ROOT_PATH = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
PROJ_PATH = os.path.join(ROOT_PATH, 'Projetos', 'src')
TOOLS_PATH = os.path.join(ROOT_PATH, 'Projetos', 'Z01-tools')
TOOLS_SCRIPT_PATH = os.path.join(TOOLS_PATH, 'scripts')
PROJ_C_PATH = os.path.join(PROJ_PATH, 'C-LogicaCombinacional')
PROJ_D_PATH = os.path.join(PROJ_PATH, 'D-UnidadeLogicaAritmetica')

sys.path.insert(0,TOOLS_SCRIPT_PATH)
sys.path.insert(0,PROJ_C_PATH)
sys.path.insert(0,PROJ_D_PATH)

from testeVHDL import vhdlScript
from testeLogicaCombinacional import tstLogiComb
from testeULA import tstUla
from report import report
##################################################

class tstLogiSeq(object):

    def __init__(self):
        self.pwd = os.path.dirname(os.path.abspath(__file__))
        self.rtl = os.path.join(self.pwd,'src/rtl/')
        self.tst = os.path.join(self.pwd,'tests/')
        self.log = os.path.join(TOOLS_PATH,'log','logE.xml')
        self.work = vhdlScript(self.log)

    def addSrc(self, work):
        work.addSrc(self.rtl)

    def addTst(self, work):
        work.addTstConfigFile(self.tst)

    def add(self, work):
        self.addSrc(work)
        self.addTst(work)

if __name__ == "__main__":

    # Init ALU
    tstLogiSeq = tstLogiSeq()

    # Logica Combinacional RTL
    tstLogiComb = tstLogiComb()
    tstLogiComb.addSrc(tstLogiSeq.work)

    # ULA
    tstUla = tstUla()
    tstUla.addSrc(tstLogiSeq.work)

    # Logica Sequencial
    print("---------- E-Logica-Sequencial")
    tstLogiSeq.add(tstLogiSeq.work)
    tstLogiSeq.work.run()

    print("===================================================")
    print("Reporting test result to server")
    r = report(tstLogiSeq.log, 'E')
    error = r.hw()
    r.send()
    sys.exit(error)
    print("===================================================")


