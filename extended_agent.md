#agent的扩展

##Linux

eg:get Os Version

1. GuestAgentLinux.py<br/>

    ```
    class LinuxVdsAgent(AgentLogicBase):
        ...
        def getOsVersion(self):
            return os.uname()[2]
        
    ```
2. GuestAgentLinux.py<br/>
    
    ```
    class CommandHandlerLinux:
        ...
        def get_infomation(self, name):
            ...
            elif name == 'os_version':
                return self.agent.getOsVersion()
                
    ```
    



##Windows

eg:get Machine Name

1. GuestAgentWindows.py<br/>

    ```
    class WindowsVdsAgent(AgentLogicBase):
        ...
        def getMachineName(self):
            return socket.getfqdn()
        
    ```
2. GuestAgentWindows.py<br/>
    
    ```
    class CommandHandlerWindows:
        ...
        def get_infomation(self, name):
            ...
            elif name == 'machine_name':
                return self.agent.getMachineName()
                
    ```
    