from PowerBindCmd import PowerBindCmd

####### Power Abort
class PowerAbortCmd(PowerBindCmd):
    def MakeBindString(self, dialog):
        return 'powexecabort'
