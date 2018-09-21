import geni.portal as portal
import geni.rspec.pg as RSpec
import geni.rspec.igext

HADOOP_VERSION = "2.7.6"

pc = portal.Context()

pc.defineParameter( "n", "Number of slave nodes", portal.ParameterType.INTEGER, 3 )

params = pc.bindParameters()

def Node( name ):
    node = RSpec.RawPC( name )
    # node.disk_image = "urn:publicid:IDN+apt.emulab.net+image+emulab-ops:UBUNTU14-64-STD"
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//hadoop-276"

    # node.addService( RSpec.Install( "http://apache.cs.utah.edu/hadoop/common/hadoop-" + HADOOP_VERSION + "/hadoop-" + HADOOP_VERSION + "-bin.tar.gz", "/usr/local" ) )

    # node.addService( RSpec.Install( "http://boa.cs.iastate.edu/cloudlab/hadoop-" + HADOOP_VERSION + "-setup.tar.gz", "/tmp" ) )
    # node.addService( RSpec.Execute( "sh", "sudo /tmp/setup/init-hdfs.sh " + HADOOP_VERSION ) )
    return node

rspec = RSpec.Request()

lan = RSpec.LAN()
rspec.addResource( lan )

node = Node( "master" )
iface = node.addInterface( "if0" )
lan.addInterface( iface )
rspec.addResource( node )

for i in range( params.n ):
    node = Node( "slave" + str( i ) )
    iface = node.addInterface( "if0" )
    lan.addInterface( iface )
    rspec.addResource( node )

tour = geni.rspec.igext.Tour()
tour.Description( geni.rspec.igext.Tour.TEXT, "A cluster running Hadoop " + HADOOP_VERSION + " as a single master and configurable number of slaves." )
tour.Instructions( geni.rspec.igext.Tour.MARKDOWN, "After your instance boots (2-3 minutes), and Hadoop is installed/configured (another 10 minutes due to formatting of HDFS drives), you can log into the master node and submit jobs.\n* [JobTracker web interface](http://{host-master}:50030/)\n* [HDFS web interface](http://{host-master}:50070/)" )
rspec.addTour( tour )

pc.printRequestRSpec( rspec )
