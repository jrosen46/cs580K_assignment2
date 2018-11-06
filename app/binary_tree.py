from mininet.topo import Topo


class BinaryTreeTopo(Topo):

    def build(self, levels=3):

        # makes implementation easier to store them as fields
        self.switch_num = 2**levels-1
        self.levels = levels

        # build switches in binary tree topology
        root = [self.addSwitch('s%s' % self.switch_num)]
        self.switch_num -= 1
        self._build_aux(root)
       
    def _build_aux(self, root):
        switches = []
        for node in root:
            # create and attach right child
            switch_right = self.addSwitch('s%s' % self.switch_num)
            self.addLink(node, switch_right)
            self.switch_num -= 1
            switches.append(switch_right)

            # create and attach left child
            switch_left = self.addSwitch('s%s' % self.switch_num)
            self.addLink(node, switch_left)
            self.switch_num -= 1
            switches.append(switch_left)

        if self.switch_num > 0:
            return self._build_aux(switches)

        # build and link hosts as last layer leaves
        for host_num, switch in zip(range(1, 2**self.levels+1, 2),
                                    reversed(switches)):
            # build and attach left host
            left_host = self.addHost('h%s' % host_num)
            self.addLink(left_host, switch)

            # build right host
            right_host = self.addHost('h%s' % str(host_num+1))
            self.addLink(right_host, switch)
    

# export so that we can use to enter mininet CLI
topos = {'mytopo': BinaryTreeTopo}
