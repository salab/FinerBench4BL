#-*- coding: utf-8 -*-
from __future__ import print_function
import os
import shutil
import subprocess
import git
from commons import Subjects

########################################################################################
class Launcher(object):
    ProgramPATH = u'/mnt/exp/git-stein/'
    TYPE = u'Test'

    def getargs(self):
        import argparse
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('-p', dest='project', default=None, help='A specific project name what you want to work.')
        parser.add_argument('-g', dest='group', default=None, help='A specific group name what you want to work.')
        parser.add_argument('-c', dest='isClean', default=False, type=bool, help='work option: clean or process')
        parser.add_argument('-t', dest='removeTest', default=True, type=bool, help='work option: exclude test files in answer files')

        args = parser.parse_args()

        if args.removeTest is None:
            parser.print_help()
            return None

        if args.isClean is None:
            parser.print_help()
            return None
        return args

    def executeHistorege(self, gitrepo, gitrepo_file):
        options = u'--no-classes --no-fields --no-original --method-ext=.java --parsable --unqualify'
        command = u'java -jar /mnt/exp/git-stein/build/libs/git-stein-all.jar Historage -o %s %s %s' % (gitrepo, options, gitrepo_file)
        commands = command.split(u' ')
        try:
            #subprocess.call(commands, cwd=_cwd, shell=False) #, stdout=self.log, stderr=self.log)
            p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, cwd=self.ProgramPATH)
            while True:
                line = p.stdout.readline()
                if line != '':
                    # the real code does filtering here
                    print (line.rstrip())
                    # ログの生成を完全に無視している
                    #self.log.write(line.rstrip()+u'\n')
                    #self.log.flush()
                else:
                    break

        except Exception as e:
            print(e)
            return None
        return 'Success'


    def work(self, _sGroup=None, _sProject=None, _removeTest=True):

        S = Subjects()
        for group in (S.groups if _sGroup is None else [_sGroup]):
            for project in (S.projects[group] if _sProject is None else [_sProject]):
                # mv gitrepo/ gitrepo_file/
                path_gitrepo = S.getPath_gitrepo(group, project)
                path_gitrepo_file = S.getPath_gitrepofile(group, project)
                shutil.move(path_gitrepo,path_gitrepo_file)
                # execute git-stein
                # java -jar build/libs/git-stein-all.jar Historage
                # -o gitrepo --no-classes
                # --no-fields --no-original --method-ext='.java' --parsable
                # --unqualify gitrepo_file
                self.executeHistorege(path_gitrepo, path_gitrepo_file)
                # git checkout
                subprocess.check_call(['git', 'checkout', 'master'], stderr=subprocess.STDOUT, cwd=path_gitrepo)


if __name__ == '__main__':
    obj = Launcher()
    args = obj.getargs()
    if args is None:
        exit(1)

    obj.work(args.group, args.project, args.removeTest)
    pass
