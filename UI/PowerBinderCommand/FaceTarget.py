from UI.PowerBinderCommand import PowerBinderCommand

####### Unselect
class FaceTarget(PowerBinderCommand):
    Name = "Turn to Face Target"
    Menu = "Targeting"

    def MakeBindString(self) -> str:
        return 'face'
