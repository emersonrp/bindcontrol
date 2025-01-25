from UI.PowerBinderCommand import PowerBinderCommand

####### Power Abort
class PowerAbortCmd(PowerBinderCommand):
    Name = "Power Abort"
    Menu = "Powers"

    def MakeBindString(self):
        return 'powexecabort'
