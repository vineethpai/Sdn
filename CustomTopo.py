#!/usr/bin/python
#Author: Vineeth Pai
#Created for Coursera Programming Assignent-2
# Creating a data centre topology with a given fanout value 


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2 , linkopts3, fanout=2, **opts):
        # Initialize topology and default options
                Topo.__init__(self, **opts)

                # Add your logic here ...
               
                #Create CORE switch
                coreSw = self.addSwitch('C1')

                #Create Connection between Core and Aggregation switches
                for i in range(0,fanout):
                        AgSwitch=self.addSwitch('A%s' %(i+1))
                        self.addLink(coreSw, AgSwitch, **linkopts1)#Connect Ag%i and Core
                        #print "Link COnnected C1, A%s" %(i+1) #Debug statement
                        for j in range((i*(fanout)), ((1+i)*fanout)):
                                EgSw = self.addSwitch('E%s' % (j+1))
                                self.addLink(AgSwitch, EgSw , **linkopts2) #Connect A1E1/A1E2
                                #print "Link Connected between A%s and E%s" %(i+1) %(j+1) #Debug Statements
                                for k in range((j*fanout), ((1+j)*fanout)):
                                        host = self.addHost('h%s' % (k+1))
                                        self.addLink(host, EgSw, **linkopts3)#Connect E1/h1H2
                                #print "Link Connected between E%s and H%s" %((j+1),(k+1)) #Debug Statements


#Function to create topo object and Mininet objects

def perfTest():
   "Create network and run simple performance test"
   #"--- core to aggregation switches"
   linkopts1 = {'bw':50, 'delay':'5ms'}
   #"--- aggregation to edge switches"
   linkopts2 = {'bw':30, 'delay':'10ms'}
   #"--- edge switches to hosts"
   linkopts3 = {'bw':10, 'delay':'15ms'}
   topo = CustomTopo(linkopts1 , linkopts2 , linkopts3 , fanout= 3)
   net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
   net.start()
   net.stop()






topos = { 'custom': ( lambda: CustomTopo() ) }

#Main function
if __name__ == "__main__":
 setLogLevel('info')
 perfTest()

                                                                                                                     
