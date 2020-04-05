import pytest 
from Shell.ShellCommand import ShellCommand

class TestShell:
    shell = ShellCommand('/Users/louischen/WorkSpace')	    
    webMainPath = '/Users/louischen/WorkSpace/MyWebProject'

    # @pytest.mark.skip(reason="skip this")	    
    def test_prepareFolder(self):
        self.shell.CreateSlnFolder(self.webMainPath)

        projectName = 'DataAccess'
        self.shell.GenClassLibProject(projectName)
        projectName = 'MyWeb'
        self.shell.GenWebMVCProject(projectName)

        self.shell.PrepareDotnetProject()
        self.shell.CreateSln()

    @pytest.mark.skip(reason="skip this")	    
    def test_removeFolder(self):
        self.shell.RemoveFolder(self.webMainPath)	