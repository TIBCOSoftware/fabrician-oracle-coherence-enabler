import os
import time
import sys
import os.path

from jarray import array

from java.lang import String
from java.lang import Object
from java.lang import Boolean
from java.lang import Integer
from java.lang import System
from java.util import Hashtable

from javax.management import MBeanServerConnection
from javax.management import ObjectName
from javax.management.remote import JMXConnector
from javax.management.remote import JMXConnectorFactory
from javax.management.remote import JMXServiceURL

from com.datasynapse.fabric.util import ContainerUtils
from com.datasynapse.fabric.container import Feature
from com.datasynapse.fabric.common import RuntimeContextVariable

class UnZipFile:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def extract(self, file, dir):
        if os.path.getsize(file) == 0:
            return
        
        if not dir.endswith(':') and not os.path.exists(dir):
            os.mkdir(dir)

        zf = zipfile.ZipFile(file)

        # create directory structure to house files
        self._createstructure(file, dir)

        # extract files to directory structure
        for i, name in enumerate(zf.namelist()):
            if self.verbose == True:
                logger.fine("Extracting:" + `name`)

            if not name.endswith('/'):
                outfile = open(os.path.join(dir, name), 'wb')
                outfile.write(zf.read(name))
                outfile.flush()
                outfile.close()


    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)


    def _createdir(self, basedir, dir):
        """ Create any parent directories that don't currently exist """
        index = dir.rfind('/')
        if index > 0:
            dir = dir[0:index]
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                self._createdir(basedir, curdir)
                os.mkdir(dir)
            else:
                return
        else:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)


    def _makedirs(self, directories, basedir):
        """ Create any directories that don't currently exist """
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                self._createdir(basedir, curdir)

    def _listdirs(self, file):
        """ Grabs all the directories in the zip structure
        This is necessary to create the structure before trying
        to extract the file to it. """
        zf = zipfile.ZipFile(file)

        dirs = []

        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)
            else:
                index = name.rfind('/')
                if index > 0:
                    index = index + 1
                    name = name[0:index]
                    dirs.append(name)

        dirs.sort()
        return dirs
    
class CoherenceServer:
    def __init__(self):
        " initialize coherence server"
        
        self.__jmxUrl = getVariableValue("JMX_URL")
        self.__jmxUser = getVariableValue("JMX_USERNAME")
        self.__jmxPassword = getVariableValue("JMX_PASSWORD")
        self.__serviceName = getVariableValue("SERVICE_NAME")
        self.__nodeId = None
        self.__jmxConnector = None
        self.__jmxConnection = None
        self.__clusterMBean = None
        self.__nodeMBean = None
        self.__serviceMBean = None
        
        
        self.__nameAttr = {"Available Memory (MB)":"MemoryAvailableMB", 
                           "Send Queue Size":"SendQueueSize", 
                           "Request Average Duration":"RequestAverageDuration",
                           "Request Pending Count":"RequestPendingCount",
                           "Task Average Duration":"TaskAverageDuration",
                           "Task Backlog":"TaskBacklog",
                           "Thread Average Active Count":"ThreadAverageActiveCount" };
        self.__attrMBean = {"MemoryAvailableMB":None, 
                            "SendQueueSize":None, 
                            "RequestAverageDuration":None,
                            "RequestPendingCount":None,
                            "TaskAverageDuration":None,
                            "TaskBacklog":None,
                            "ThreadAverageActiveCount":None };
        
    def __createJMXConnection(self):
        "create JMX connection"
        
        self.__jmxConnection = None
        self.__jmxConnector = None
        
        try:
            jmxServiceUrl = JMXServiceURL(self.__jmxUrl)
            env = Hashtable()
            cred = array([self.__jmxUser, self.__jmxPassword], String)
            env.put("jmx.remote.credentials", cred)
            logger.info("Connecting to Oracle Coherence MBean Server:" + `jmxServiceUrl`)
            self.__jmxConnector = JMXConnectorFactory.connect(jmxServiceUrl, env)
            self.__jmxConnection = self.__jmxConnector.getMBeanServerConnection()
            logger.info("Successfully connected to Oracle Coherence MBean Server:" + `jmxServiceUrl`)
        except:
            type, value, traceback = sys.exc_info()
            logger.finer("JMX Connection error:" + `value`)
            self.__jmxConnection = None
            try:
                if self.__jmxConnector:
                    self.__jmxConnector.close()
                    self.__jmxConnector = None
            except:
                type, value, traceback = sys.exc_info()
                logger.finer("JMX Connector close error:" + `value`)
        
    def isServerRunning(self):
        " is server running"
        return self.__jmxConnection.getAttribute(self.__clusterMBean, "Running")
    
    def hasServerStarted(self):
        " has server started"
        started = False

        if not self.__jmxConnection:
            self.__createJMXConnection()
            
        if self.__jmxConnection:  
            self.__clusterMBean = ObjectName("Coherence:type=Cluster")
            logger.info("Checking if Coherence cluster node has started:" + `self.__clusterMBean`)
            running = self.__jmxConnection.getAttribute(self.__clusterMBean, "Running")
            
            logger.info("Coherence cluster node has started:" + `running`)
            if running:
                logger.info("Getting LocalMemberId attribute from cluster node:" + `self.__clusterMBean`)
                self.__nodeId = self.__jmxConnection.getAttribute(self.__clusterMBean, "LocalMemberId")
                logger.info("Oracle Coherence Cluster LocalMemberId:" + `self.__nodeId`)
                self.__nodeMBean = ObjectName("Coherence:type=Node,nodeId=" + `self.__nodeId`)
                self.__attrMBean["MemoryAvailableMB"] = self.__nodeMBean
                self.__attrMBean["SendQueueSize"] = self.__nodeMBean
               
                self.__serviceMBean = ObjectName("Coherence:type=Service,name="+self.__serviceName+",nodeId="+`self.__nodeId`)
                self.__attrMBean["RequestAverageDuration"] = self.__serviceMBean
                self.__attrMBean["RequestPendingCount"] = self.__serviceMBean
                self.__attrMBean["TaskAverageDuration"] = self.__serviceMBean
                self.__attrMBean["TaskBacklog"] = self.__serviceMBean
                self.__attrMBean["ThreadAverageActiveCount"] = self.__serviceMBean
                
                started = True
        
        return started
        
    def shutdownServer(self):
        "shutdown server"

        try:
            container = proxy.container
            process = container.process
            if process and process.isRunning():
                shutdownStart = System.currentTimeMillis()
                
                logger.info("Shutting down cluster node:" + `self.__clusterMBean`)
            
                oa = array([], Object)
                sa = array([], String)
                self.__jmxConnection.invoke(self.__clusterMBean, "shutdown", oa, sa)
                    
                container.waitForShutdown(shutdownStart)
        finally:
            self.__jmxConnection = None
            try:
                if self.__jmxConnector:
                    self.__jmxConnector.close()
                    self.__jmxConnector = None
            except:
                type, value, traceback = sys.exc_info()
                logger.finer("JMX Connector close error:" + `value`)
    
    def getStatistic(self, statName):
        " get statistic"
        attrName = self.__nameAttr[statName]
        attrMbean = self.__attrMBean[attrName]
        return self.__jmxConnection.getAttribute(attrMbean, attrName)
    
def getVariableValue(name, value=None):
    "get runtime variable value"
    var = runtimeContext.getVariable(name)
    if var != None:
        value = var.value
    
    return value

def doInit(additionalVariables):
    "do init"
    coherenceServer = CoherenceServer()
             
    # save mJMX MBean server as a runtime context variable
    coherenceServerRcv = RuntimeContextVariable("COHERENCE_SERVER_OBJECT", coherenceServer, RuntimeContextVariable.OBJECT_TYPE)
    runtimeContext.addVariable(coherenceServerRcv)
    
def doStart():
    "do start"
    logger.info("Enter OracleCoherenceEnabler:doStart")
    
    # install archives: we need to install them before starting the oracle coherence server
    
    archiveFeatureInfo = ContainerUtils.getFeatureInfo(Feature.ARCHIVE_FEATURE_NAME, proxy.container, proxy.container.currentDomain)
    if archiveFeatureInfo != None:
        rootDirPath = runtimeContext.rootDirectory.absolutePath
        archiveDir = archiveFeatureInfo.archiveDirectory
        archiveDirPath = os.path.join(rootDirPath, archiveDir)
        if os.path.isdir(archiveDirPath):
            deploymentDir = getVariableValue("COHERENCE_RUNTIME_DEPLOYMENT_DIR")
            logger.info("OracleCoherenceEnabler:doStart:Extracting archives:" + archiveDirPath + " --> " + deploymentDir)
            uzip = UnZipFile()
            for entry in os.listdir(archiveDirPath):
                archiveFile = os.path.join(archiveDirPath, entry)
                if os.path.isfile(archiveFile):
                    logger.info("OracleCoherenceEnabler:doStart:Extracting archive:" + archiveFile)
                    try:
                        uzip.extract(archiveFile, deploymentDir)
                    except:
                        type, value, traceback = sys.exc_info()
                        logger.severe("OracleCoherenceEnabler:doStart:Error extracting archive file:"+`value`)
                    
        # we do not want the archive feature to install the archives
        archiveFeatureInfo.setInstallArchivesViaFileCopy(False)
    
    # start coherence server
    proxy.doStart()
    logger.info("Exit OracleCoherenceEnabler:doStart")

def doShutdown():
    "do shutdown"
    logger.info("Enter OracleCoherenceCluster:doShutdown")
    try:
        coherenceServer = getVariableValue("COHERENCE_SERVER_OBJECT")
        if coherenceServer:
            coherenceServer.shutdownServer()
    except:
        type, value, traceback = sys.exc_info()
        logger.severe("OracleCoherenceCluster:doShutdown:JMX Shutdown error:" + `value`)
    
    logger.info("Exit OracleCoherenceCluster:doShutdown")

def hasContainerStarted():
    started = False
    try:
        coherenceServer = getVariableValue("COHERENCE_SERVER_OBJECT")
        
        if coherenceServer:
            started = coherenceServer.hasServerStarted()
            
    except:
        type, value, traceback = sys.exc_info()
        logger.severe("Unexpected error in OracleCoherenceCluster:hasContainerStarted:" + `value`)
    
    return started
    
def isContainerRunning():
    running = False
    try:
        coherenceServer = getVariableValue("COHERENCE_SERVER_OBJECT")
        if coherenceServer:
            running = coherenceServer.isServerRunning()
    except:
        type, value, traceback = sys.exc_info()
        logger.severe("Unexpected error in OracleCoherenceCluster:isContainerRunning:" + `value`)
    
    return running

def getStatistic(statName):
    stat = None
    try:
        coherenceServer = getVariableValue("COHERENCE_SERVER_OBJECT")
        if coherenceServer:
            stat = coherenceServer.getStatistic(statName)
    except:
        type, value, traceback = sys.exc_info()
        logger.severe("Unexpected error in OracleCoherenceCluster:getStatistic:" + `value`)
    return stat

