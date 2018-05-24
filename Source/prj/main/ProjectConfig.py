
from mtm.util.Assert import *

class ProjectConfig:
    def __init__(self):
        self.pluginsFolder = []
        self.assetsFolder = []
        self.customDirectories = {}
        self.solutionProjects = []
        self.solutionFolders = []
        self.packageFolders = []
        self.targetPlatforms = []
        self.projectSettingsPath = None
