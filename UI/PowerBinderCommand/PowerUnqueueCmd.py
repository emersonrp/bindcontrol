from UI.PowerBinderCommand import PowerBinderCommand

####### Power Unqueue
class PowerUnqueueCmd(PowerBinderCommand):
    Name = "Power Unqueue"
    Menu = "Powers"

    def MakeBindString(self):
        return 'powexecunqueue'
