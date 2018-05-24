
from mtm.util.Assert import *
from mtm.ioc.Inject import Inject

class ProjectConfig:
    """
    Misc. helper functions related to windows junctions
    """
    _log = Inject('Logger')

    def __init__(self):
        self.pluginsFolder = []
        self.assetsFolder = []
        self.customDirectories = {}
        self.solutionProjects = []
        self.solutionFolders = []
        self.packageFolders = []
        self.targetPlatforms = []
        self.projectSettingsPath = None

    def getAssetByName(self, name):
    	for x in self.assetsFolder:
    		if type(x) is dict:
    			if x["name"] == name:
    				return x
    		else:
    			if x == name:
    				return x
