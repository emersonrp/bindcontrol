# BindControl custom exceptions

# BindFile exceptions
class BCBindFileException(Exception): pass
class BindFileParentDirsException(BCBindFileException): pass
class BindFileCreateBindFileException(BCBindFileException): pass
class BindFileBindTooLongException(BCBindFileException): pass
class BindFileWriteToBindFileException(BCBindFileException): pass

# GameData exceptions
class BCGameDataException(Exception): pass
class GameDataBadServerException(BCGameDataException): pass

# Profile exceptions
class BCProfileException(Exception): pass
class ProfileLoadFromFileException(BCProfileException): pass
class ProfileCreateBindsDirException(BCProfileException): pass
class ProfileProfileIDFileException(BCProfileException): pass
class ProfilePopulateBindFileException(BCProfileException): pass
class ProfileWriteBindFileException(BCProfileException):pass

# Popmenu Editor exceptions
class BCPopmenuEditorException(Exception): pass
class PopmenuBadSubmenuException(BCPopmenuEditorException): pass
class PopmenuUnknownMenuItemException(BCPopmenuEditorException): pass

# Models/* exceptions
class BCModelsException                 (Exception        ): pass
class ProfileFileMissingException       (BCModelsException): pass
class ProfileBindsDirectoryException    (BCModelsException): pass
class ProfileLoadJSONException          (BCModelsException): pass
class ProfileDefaultProfileJSONException(BCModelsException): pass
class ProfileParamsException            (BCModelsException): pass
class ProfileSaveException              (BCModelsException): pass
class ProfileNoProfileIDFileException   (BCModelsException): pass

# Page exceptions
class BCPageException(Exception): pass
class PageMovementBadCallbackException(BCPageException): pass

# UI/* exceptions
class BCUIException(Exception): pass
class UIUnknownWizClass(BCUIException): pass
class UIKeySelectNoDescException(BCUIException): pass
class UIControlGroupNoCttNameException(BCUIException): pass
class UIControlGroupUnknownCtlTypeException(BCUIException): pass

# Utils/* exceptions
class BCUtilException (Exception) : pass
class UtilIncarnateDataException(BCUtilException): pass
class UtilServerException(BCUtilException): pass
