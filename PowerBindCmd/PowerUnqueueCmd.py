from PowerBindCmd import PowerBindCmd

####### Power Unqueue
class PowerUnqueueCmd(PowerBindCmd):
    def MakeBindString(self, dialog):
        return 'powexecunqueue'
