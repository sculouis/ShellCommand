import subprocess
from pathlib import Path
import shutil
from os import chdir
import os  
import shutil  
from Library.Enums import Command,ProjectKind,Package

class ShellCommand:
    def __init__(self,mainPath):
        self.mainPath = mainPath

    def ShellCmd(self,cmd):
        process = subprocess.Popen(cmd, 
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

        while True:
            output = process.stdout.readline()
            print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                # print('RETURN CODE', return_code)
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    print(output.strip())
                break

    def CreateSlnFolder(self,path):
        self.slnPath = path
        try:
            if not os.path.exists(self.slnPath):
                os.makedirs(self.slnPath)
        except OSError as e:
            print(e)
        else:
            print("The directory is created successfully")

    def RemoveFolder(self,path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            print(e)
        else:
            print("The directory is deleted successfully")

    def NewProject(self,projectName,ProjectKind):
        chdir(self.slnPath)
        p = Path()
        print(f'work path:{p.cwd()}')
        arg = ['dotnet',Command.NEW.value,ProjectKind.value, '-n', projectName]
        self.ShellCmd(arg)

    def RemoveProject(self,projectName):
        chdir(self.slnPath)
        p = Path()
        print(f'work path:{p.cwd()}')
        chdir(projectName)
        p = Path()
        print(f'work path:{p.cwd()}')
        RemoveFolder(p.absolute())

    def CopyFolder(self,src,dest):    
        # List files and directories  
        print("Before copying file:")  
        print(os.listdir(self.mainPath))  
        destination = shutil.copytree(src, dest, copy_function = shutil.copy)  
        # List files and directories  
        # in "C:/Users / Rajnish / Desktop / GeeksforGeeks"  
        print("After copying file:")  
        print(os.listdir(self.mainPath))  
        # Print path of newly  
        # created file  
        print("Destination path:", destination) 

    def AddPackage(self,projectName,package,packageName,version):
        chdir(self.slnPath + f'/{projectName}')
        p = Path()
        print(f'work path:{p.cwd()}')
        arg = ['dotnet',package.value,'package',packageName,'--version',version]
        self.ShellCmd(arg)

    def PrepareDotnetProject(self):
        # Source path  
        src = f'{self.mainPath}/CodeGen/GenDotnetClass/Models'
        # Destination path  
        dest = f'{self.slnPath}/DataAccess/Models'
        self.CopyFolder(src,dest)

        # Source path  
        src = f'{self.mainPath}/CodeGen/GenDotnetClass/Interfaces'
        # Destination path  
        dest = f'{self.slnPath}/DataAccess/Interfaces'
        self.CopyFolder(src,dest)

        # Source path  
        src = f'{self.mainPath}/CodeGen/GenDotnetClass/Repository'
        # Destination path  
        dest = f'{self.slnPath}/DataAccess/Repository'
        self.CopyFolder(src,dest)

    def copytree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def PrepareMvcProject(self):
        # Source path  
        src = f'{self.mainPath}/CodeGen/GenDotnetClass/Controllers'
        # Destination path  
        dest = f'{self.mainPath}/MyWebProject/MyWeb/Controllers'
        self.copytree(src,dest)

    def GenClassLibProject(self,projectName): 
        self.NewProject(projectName,ProjectKind.CLASSLIB)
        packageName = "Microsoft.EntityFrameworkCore.SqlServer"
        version = "3.1.3"
        projectName = "DataAccess"
        self.AddPackage(projectName,Package.ADD,packageName,version)

    def GenWebMVCProject(self,projectName): 
        self.NewProject(projectName,ProjectKind.MVC)
        # packageName = "Microsoft.EntityFrameworkCore.SqlServer"
        # version = "3.1.3"
        # projectName = "DataAccess"
        # self.AddPackage(f'{mainPath}/{projectName}',Package.ADD,packageName,version)

    def CreateSln(self):
        chdir(self.slnPath)
        arg = ['dotnet',Command.ADD.value,'MyWeb/MyWeb.csproj','reference','DataAccess/DataAccess.csproj']
        self.ShellCmd(arg)

        arg = ['dotnet',Command.NEW.value,ProjectKind.SLN.value]
        self.ShellCmd(arg)

        arg = ['dotnet',ProjectKind.SLN.value, Command.ADD.value, 'DataAccess/DataAccess.csproj'] 
        self.ShellCmd(arg)

        arg = ['dotnet',ProjectKind.SLN.value, Command.ADD.value, 'MyWeb/MyWeb.csproj'] 
        self.ShellCmd(arg)
