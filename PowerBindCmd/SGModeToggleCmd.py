from PowerBindCmd import PowerBindCmd

####### SG Mode Toggle
class SGModeToggleCmd(PowerBindCmd):
    def MakeBindString(self, dialog):
        return 'sgmode'
