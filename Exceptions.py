# BindControl custom exceptions

# Models/* exceptions
class BCModelsException                 (Exception        ): pass
class ProfileFileMissingException       (BCModelsException): pass
class ProfileBindsDirectoryException    (BCModelsException): pass
class ProfileLoadJSONException          (BCModelsException): pass
class ProfileDefaultProfileJSONException(BCModelsException): pass
class ProfileParamsException            (BCModelsException): pass
class ProfileSaveException              (BCModelsException): pass
