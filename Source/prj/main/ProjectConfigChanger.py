
import mtm.util.YamlSerializer as YamlSerializer

from mtm.util.Assert import *

import mtm.ioc.Container as Container
from mtm.ioc.Inject import Inject
from mtm.ioc.Inject import InjectMany
import mtm.ioc.IocAssertions as Assertions

from mtm.util.Platforms import Platforms

from prj.main.ProjenyConstants import ProjectConfigFileName
from prj.main.ProjectConfig import ProjectConfig

class ProjectConfigChanger:
    _log = Inject('Logger')
    _sys = Inject('SystemHelper')
    _packageManager = Inject('PackageManager')
    _varMgr = Inject('VarManager')

    def _getProjectConfigPath(self, projectName):
        return self._varMgr.expandPath('[UnityProjectsDir]/{0}/{1}'.format(projectName, ProjectConfigFileName))

    def _loadProjectConfig(self, projectName):
        configPath = self._getProjectConfigPath(projectName)

        yamlData = YamlSerializer.deserialize(self._sys.readFileAsText(configPath))

        result = ProjectConfig()

        for pair in yamlData.__dict__.items():
            result.__dict__[pair[0]] = pair[1]

        return result

    def _saveProjectConfig(self, projectName, projectConfig):
        configPath = self._getProjectConfigPath(projectName)
        self._sys.writeFileAsText(configPath, YamlSerializer.serialize(projectConfig))

    def setPackagesForProject(self, projectName, packageNames):
        with self._log.heading('Setting packages {0} to project {1}'.format(packageNames, projectName)):
            # assertThat(packageNames in self._packageManager.getAllPackageNames(projectName), "Could not find the given package '{0}' in the UnityPackages folder", packageNames)
            self._packageManager.setPathsForProjectPlatform(projectName, Platforms.Windows)

            projConfig = self._loadProjectConfig(projectName)

            projConfig.assetsFolder = packageNames

            self._saveProjectConfig(projectName, projConfig)

            self._log.info("Set packages '{0}' to '{1}/{2}'", packageNames, projectName, ProjectConfigFileName)

    def addPackage(self, projectName, packageName, addToAssetsFolder):
        with self._log.heading('Adding package {0} to project {1}'.format(packageName, projectName)):
            assertThat(packageName in self._packageManager.getAllPackageNames(projectName), "Could not find the given package '{0}' in the UnityPackages folder", packageName)
            self._packageManager.setPathsForProjectPlatform(projectName, Platforms.Windows)

            projConfig = self._loadProjectConfig(projectName)

            assertThat(packageName not in projConfig.assetsFolder and packageName not in projConfig.pluginsFolder,
               "Given package '{0}' has already been added to project config", packageName)

            if addToAssetsFolder:
                projConfig.assetsFolder.append(packageName)
            else:
                projConfig.pluginsFolder.append(packageName)

            self._saveProjectConfig(projectName, projConfig)

            self._log.good("Added package '{0}' to file '{1}/{2}'", packageName, projectName, ProjectConfigFileName)

