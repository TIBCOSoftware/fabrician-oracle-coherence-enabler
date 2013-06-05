[fabrician.org](http://fabrician.org/)
==========================================================================
Oracle Coherence Enabler User Guide
==========================================================================
 
Introduction
--------------------------------------
A Silver Fabric Enabler allows an external application or application platform, 
such as a J2EE application server to run in a TIBCO Silver Fabric software 
environment. The Oracle Coherence Enabler supports configuration and runtime 
management of a distributed Oracle Coherence cache cluster. 

Summary
--------------------------------------
<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Enabled platform</td>
    <td>Oracle Coherence 3.7.1</td>
  </tr>
  <tr>
    <td>Cluster configuration support</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>Dynamic clustering support</td>
    <td>Yes</td>
  </tr>
</table>

Supported Platforms
--------------------------------------
* Silver Fabric 5
* Windows, Linux
 
Installation
--------------------------------------
The Oracle Coherence Enabler consists of an Enabler Runtime Grid Library and a Distribution 
Grid Library. The Enabler Runtime contains information specific to a Silver Fabric 
version that is used to integrate the Enabler, and the Distribution contains the 
application server or program used for the Enabler. Installation of the Oracle Coherence
Enabler involves copying these Grid Libraries to the 
SF_HOME/webapps/livecluster/deploy/resources/gridlib directory on the Silver Fabric Broker. 
 
Runtime Grid Library
--------------------------------------
The Enabler Runtime Grid Library is created by building the maven project.
```bash
mvn package
```
 
Distribution Grid Library
--------------------------------------
The Distribution Grid Library is created by performing the following steps:
* Download and extract the Oracle Coherence for Java package from http://www.oracle.com.
* Create a grid-library.xml file with the below contents and place it alongside the coherence directory.
* Create a tar.gz or zip of the contents.

```xml
    <grid-library os="all">
        <grid-library-name>oracle-coherence-distribution</grid-library-name>
        <grid-library-version>3.7.1</grid-library-version>
    </grid-library>
```
 
Statistics
--------------------------------------
<table>
  <tr>
    <th>Name</th>
    <th>Description</th>
    <th>Units</th>
  </tr>
  <tr>
    <td>Available Memory</td>
    <td>The total available memory</td>
    <td>MB</td>
  </tr>
  <tr>
    <td>Send Queue Size</td>
    <td>The number of packets currently scheduled for delivery. This number includes both packets that are to be sent immediately and packets that have already been sent and awaiting for acknowledgment. Packets that do not receive an acknowledgment within ResendDelay interval will be automatically resent.</td>
    <td>Queued Packets</td>
  </tr>
  <tr>
    <td>Request Average Duration</td>
    <td>The average duration (in milliseconds) of an individual synchronous request issued by the service since the last time the statistics were reset.</td>
    <td>Milliseconds</td>
  </tr>
  <tr>
    <td>Request Pending Count</td>
    <td>The number of pending synchronous requests issued by the service.</td>
    <td>Requests</td>
  </tr>
  <tr>
    <td>Task Average Duration</td>
    <td>The number of pending synchronous requests issued by the service.</td>
    <td>Milliseconds</td>
  </tr>
  <tr>
    <td>Task Backlog</td>
    <td>The number of pending synchronous requests issued by the service.</td>
    <td>Tasks</td>
  </tr>
  <tr>
    <td>Thread Average Active Count</td>
    <td>The number of pending synchronous requests issued by the service.</td>
    <td>Active Threads</td>
  </tr>  
</table>
 
Runtime Context Variables
--------------------------------------
To configure a Silver Fabric Component based on this enabler, use J2EE Component Type. The following 
Runtime Variables may need to be configured in a typical Component configuration, when working with 
default Coherence cache and operational configuration:
* COHERENCE_CLUSTER_NAME
* COHERENCE_CLUSTER_ADDRESS
* COHERENCE_CLUSTER_PORT
* MAX_HEAP
* MIN_HEAP
* JMX_USERNAME
* JMX_PASSWORD
* SERVICE_NAME

To use a non-default Coherence cache and operational configuration, add an operational configuration 
override file conventionally named tangosol-coherence-override.xml, and any custom cache configuration 
file referred from the operational override file, to the Component under the relative path config. 
You may also need to set the SERVICE_NAME Runtime Variable.

Coherence security and JMX security are disabled by default. To enable, place your .jks keystore files in the content/security path or otherwise update the COHERENCE_KEYSTORE_FILE and JMX_SSL_KEYSTORE_FILE runtime context variables to point to your keystores.

Full list of Runtime Context Variables:

<table>
  <tr>
    <th>Variable</th>
    <th>Type</th>
    <th>Description</th>
    <th>Default Value</th>
  </tr>
  <tr>
    <td>HOST_NAME</td>
    <td>String</td>
    <td>Name of the host machine on which this enabler will be running</td>
    <td>${LISTEN_ADDRESS}</td>
  </tr>
  <tr>
    <td>MULTICAST_TTL</td>
    <td>String</td>
    <td>Multi-cast  time to live in terms of network hops</td>
    <td>4</td>
  </tr>
  <tr>
    <td>COHERENCE_WKA_ADDRESS</td>
    <td>String</td>
    <td>Well Known Address for unicast; by default multicast is used so this is empty</td>
    <td> </td>
  </tr>
  <tr>
    <td>COHERENCE_WKA_PORT</td>
    <td>String</td>
    <td>Well Known Address port for unicast: This applies only if unicast is used</td>
    <td>8088</td>
  </tr>
  <tr>
    <td>COHERENCE_UNICAST_ADDRESS</td>
    <td>String</td>
    <td>Unicast listener address This applies only if unicast is used</td>
    <td>${HOST_NAME}</td>
  </tr>
  <tr>
    <td>COHERENCE_UNICAST_PORT</td>
    <td>String</td>
    <td>Unicast listener port: This applies only if unicast is used</td>
    <td>8088</td>
  </tr>
  <tr>
    <td>COHERENCE_CLUSTER_NAME</td>
    <td>String</td>
    <td>Coherence cluster name</td>
    <td>cluster1</td>
  </tr>
  <tr>
    <td>COHERENCE_CLUSTER_ADDRESS</td>
    <td>String</td>
    <td>Cluster network address</td>
    <td>227.7.7.9</td>
  </tr>
  <tr>
    <td>COHERENCE_CLUSTER_PORT</td>
    <td>String</td>
    <td>Cluster network port on the Cluster Address</td>
    <td>9778</td>
  </tr>
  <tr>
    <td>SHUTDOWN</td>
    <td>String</td>
    <td>Shutdown: force, none, false</td>
    <td>force</td>
  </tr>
  <tr>
    <td>SERVICE_TIMEOUT</td>
    <td>String</td>
    <td>In milliseconds, greather than or equal to the packet-delivery timeout</td>
    <td>305000</td>
  </tr>
  <tr>
    <td>PACKET_DELIVERY_TIMEOUT</td>
    <td>String</td>
    <td>In milliseconds, greater of 300000 and two times the maximum expected full GC duration</td>
    <td>300000</td>
  </tr>
  <tr>
    <td>SITE_NAME</td>
    <td>String</td>
    <td>Site Name</td>
    <td>site</td>
  </tr>
  <tr>
    <td>MACHINE_NAME</td>
    <td>String</td>
    <td>Machine Name</td>
    <td>${HOST_NAME}</td>
  </tr>
  <tr>
    <td>RACK_NAME</td>
    <td>String</td>
    <td>Rack Name</td>
    <td>${HOST_NAME}</td>
  </tr>
  <tr>
    <td>PROCESS_NAME</td>
    <td>String</td>
    <td>Process Name</td>
    <td>coherence</td>
  </tr>
  <tr>
    <td>MEMBER_NAME</td>
    <td>String</td>
    <td>Member Name</td>
    <td>${HOST_NAME}</td>
  </tr>
  <tr>
    <td>ROLE_NAME</td>
    <td>String</td>
    <td>Role Name</td>
    <td>Manager</td>
  </tr>
  <tr>
    <td>PRIORITY</td>
    <td>String</td>
    <td>Priority</td>
    <td> </td>
  </tr>
  <tr>
    <td>COHERENCE_RUN_MODE</td>
    <td>String</td>
    <td>Coherence run mode; possible values are prod, dev and eval</td>
    <td>dev</td>
  </tr>
  <tr>
    <td>COHERENCE_SECURITY_ENABLED</td>
    <td>String</td>
    <td>Coherence security enabled</td>
    <td>false</td>
  </tr>
  <tr>
    <td>COHERENCE_USERNAME</td>
    <td>String</td>
    <td>Coherence username for the server</td>
    <td>manager</td>
  </tr>
  <tr>
    <td>COHERENCE_PASSWORD</td>
    <td>String</td>
    <td>Coherence password for the server</td>
    <td>password</td>
  </tr>
  <tr>
    <td>JDK_NAME</td>
    <td>String</td>
    <td> </td>
    <td>j2sdk</td>
  </tr>
  <tr>
    <td>JDK_VERSION</td>
    <td>String</td>
    <td> </td>
    <td>1.6.0</td>
  </tr>
  <tr>
    <td>JAVA_HOME</td>
    <td>String</td>
    <td> </td>
    <td>${GRIDLIB_JAVA_HOME}</td>
  </tr>
  <tr>
    <td>COHERENCE_HOME</td>
    <td>String</td>
    <td> </td>
    <td>${COHERENCE_DOMAIN_DIR}</td>
  </tr>
  <tr>
    <td>DELETE_RUNTIME_DIR</td>
    <td>String</td>
    <td>Delete runtime directory</td>
    <td>true</td>
  </tr>
  <tr>
    <td>COHERENCE_DOMAIN_NAME</td>
    <td>String</td>
    <td>Coherence domain name</td>
    <td>coherence_domain</td>
  </tr>
  <tr>
    <td>COHERENCE_DOMAIN_DIR</td>
    <td>Environment</td>
    <td>Coherence runtime directory</td>
    <td>${ENGINE_WORK_DIR}/${COHERENCE_DOMAIN_NAME}</td>
  </tr>
  <tr>
    <td>COHERENCE_RUNTIME_DEPLOYMENT_DIR</td>
    <td>Environment</td>
    <td>Deployment directory for additional jars</td>
    <td>${COHERENCE_DOMAIN_DIR}/deploy</td>
  </tr>
  <tr>
    <td>COHERENCE_CONFIG_FILE</td>
    <td>Environment</td>
    <td>Configuration file for caches</td>
    <td>${COHERENCE_DOMAIN_DIR}/config/tangosol-coherence.xml</td>
  </tr>
  <tr>
    <td>COHERENCE_LOG_FILE</td>
    <td>Environment</td>
    <td>The Coherence log file</td>
    <td>${COHERENCE_DOMAIN_DIR}/coherence.log</td>
  </tr>
  <tr>
    <td>COHERENCE_KEYSTORE_FILE</td>
    <td>String</td>
    <td>The full path to the Coherence security framework keystore file</td>
    <td>${COHERENCE_DOMAIN_DIR}/security/keystore.jks</td>
  </tr>
  <tr>
    <td>COHERENCE_PERMISSIONS_FILE</td>
    <td>String</td>
    <td>The Coherence security framework permissions  file</td>
    <td>${COHERENCE_DOMAIN_DIR}/security/permissions.xml</td>
  </tr>
  <tr>
    <td>COHERENCE_LOGIN_CONFIG_FILE</td>
    <td>Environment</td>
    <td>Coherence login config file</td>
    <td>${COHERENCE_DOMAIN_DIR}/lib/security/login.config</td>
  </tr>
  <tr>
    <td>COHERENCE_REPORTS_DIR</td>
    <td>Environment</td>
    <td>Coherence report config</td>
    <td>${COHERENCE_DOMAIN_DIR}/config/reports</td>
  </tr>
  <tr>
    <td>COHERENCE_REPORT_CONFIG</td>
    <td>String</td>
    <td>Coherence report config</td>
    <td>${COHERENCE_REPORTS_DIR}/report-group.xml</td>
  </tr>
  <tr>
    <td>RMI_REGISTRY_PORT</td>
    <td>Environment</td>
    <td>JMXport for JMX connection</td>
    <td>9000</td>
  </tr>
  <tr>
    <td>RMI_CONNECTION_PORT</td>
    <td>Environment</td>
    <td>RMI port for JMX remote connection</td>
    <td>3000</td>
  </tr>
  <tr>
    <td>TCP_PROXY_PORT</td>
    <td>String</td>
    <td>TCP proxy port for remote Coherence clients</td>
    <td>9099</td>
  </tr>
  <tr>
    <td>SERVICE_NAME</td>
    <td>String</td>
    <td>Service name. User for building JMX path to statistics</td>
    <td>DistributedCache</td>
  </tr>
  <tr>
    <td>WINDOWS_STARTUP_COMMAND</td>
    <td>String</td>
    <td>Windows startup command</td>
    <td>&quot;${COHERENCE_DOMAIN_DIR}/bin/cache-server.cmd&quot;</td>
  </tr>
  <tr>
    <td>UNIX_STARTUP_COMMAND</td>
    <td>String</td>
    <td>Unix Startup Command</td>
    <td>${COHERENCE_DOMAIN_DIR}/bin/cache-server.sh</td>
  </tr>
  <tr>
    <td>MAX_HEAP</td>
    <td>String</td>
    <td>Maximum heap size</td>
    <td>512m</td>
  </tr>
  <tr>
    <td>MIN_HEAP</td>
    <td>String</td>
    <td>Minimum heap size</td>
    <td>128m</td>
  </tr>
  <tr>
    <td>JMX_PASSWORD</td>
    <td>String</td>
    <td>Password for JMX access (if required)</td>
    <td>changeit</td>
  </tr>
  <tr>
    <td>JMX_USERNAME</td>
    <td>String</td>
    <td>Username for JMX access (if required)</td>
    <td>coherence</td>
  </tr>
  <tr>
    <td>JMX_URL</td>
    <td>String</td>
    <td>JMX URL for statistics and monitoring</td>
    <td>service:jmx:rmi://${HOST_NAME}:${RMI_CONNECTION_PORT}/jndi/rmi://${HOST_NAME}:${RMI_REGISTRY_PORT}/jmxrmi</td>
  </tr>
  <tr>
    <td>JMX_SSL_ENABLED</td>
    <td>String</td>
    <td>JMX SSL enabled</td>
    <td>false</td>
  </tr>
  <tr>
    <td>JMX_TWO_WAY_SSL_ENABLED</td>
    <td>String</td>
    <td>JMX Two way SSL enabled</td>
    <td>false</td>
  </tr>
  <tr>
    <td>JMX_SECURITY_ENABLED</td>
    <td>String</td>
    <td>JMX security enabled</td>
    <td>false</td>
  </tr>
  <tr>
    <td>JMX_CONFIG_FILE</td>
    <td>Environment</td>
    <td>JMX config file</td>
    <td>${COHERENCE_DOMAIN_DIR}/management/management.properties</td>
  </tr>
  <tr>
    <td>JMX_SSL_CONFIG_FILE</td>
    <td>Environment</td>
    <td>JMX SSL config file</td>
    <td>${COHERENCE_DOMAIN_DIR}/management/jmxssl.properties</td>
  </tr>
  <tr>
    <td>JMX_SSL_KEYSTORE_FILE</td>
    <td>String</td>
    <td>The full path to the JMX ssl keystore file</td>
    <td>${COHERENCE_DOMAIN_DIR}/management/jmxssl.jks</td>
  </tr>
  <tr>
    <td>JMX_SSL_TRUSTSTORE_FILE</td>
    <td>String</td>
    <td>JMX ssl trust store file</td>
    <td>${COHERENCE_DOMAIN_DIR}/management/jmxssl.jks</td>
  </tr>
  <tr>
    <td>JMX_SSL_KEYSTORE_PASSWORD</td>
    <td>String</td>
    <td>JMX ssl keystore password</td>
    <td>changeit</td>
  </tr>
  <tr>
    <td>JMX_SSL_TRUSTSTORE_PASSWORD</td>
    <td>String</td>
    <td>JMX ssl truststore password</td>
    <td>changeit</td>
  </tr>
  <tr>
    <td>JMX_PASSWORD_FILE</td>
    <td>Environment</td>
    <td>JMX remote password file</td>
    <td>${COHERENCE_DOMAIN_DIR}/management/jmxremote.password</td>
  </tr>
  <tr>
    <td>JMX_ACCESS_FILE</td>
    <td>String</td>
    <td>JMX remote access file</td>
    <td>${COHERENCE_DOMAIN_DIR}/management/jmxremote.access</td>
  </tr>
</table>
