from .RobotLxcLibraryKeywords import RobotLxcLibraryKeywords
from .version import VERSION

_version_ = VERSION

class RobotLxcLibrary(RobotLxcLibraryKeywords):
    """ RobotLxcLibrary - Support for robotframework for LXC containers"
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
