from UI.PowerBinderCommand import PowerBinderCommand

####### Power Unqueue
class PowerUnqueueCmd(PowerBinderCommand):
    Name = "Power Unqueue"
    Menu = "Powers"

    def MakeBindString(self):
        return 'powexecunqueue' if self.Profile.Server == "Homecoming" else 'px_uq'
