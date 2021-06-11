from PowerBindCmd import PowerBindCmd

####### Unselect
class UnselectCmd(PowerBindCmd):
    def MakeBindString(self, dialog):
        return 'unselect'
