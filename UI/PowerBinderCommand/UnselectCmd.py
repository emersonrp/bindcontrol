from UI.PowerBinderCommand import PowerBinderCommand

####### Unselect
class UnselectCmd(PowerBinderCommand):
    Name = "Unselect"
    Menu = "Targeting"

    def MakeBindString(self):
        return 'unselect'
