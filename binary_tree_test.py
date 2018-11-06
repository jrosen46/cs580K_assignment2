class BinaryTreeTopo:

    def build(self, levels=3):

        # makes implementation easier to store them as fields
        self.switch_num = 2**levels-1
        self.levels = levels

        # build switches in binary tree topology
        root = ['s%s' % self.switch_num]
        self.switch_num -= 1
        return self._build_switches(root)
       


    def _build_switches(self, root):
        switches = []
        for node in root:
            # create and attach right child
            switch_right = 's%s' % self.switch_num
            self.switch_num -= 1
            switches.append(switch_right)

            # create and attach left child
            switch_left = 's%s' % self.switch_num
            self.switch_num -= 1
            switches.append(switch_left)

        if self.switch_num > 0:
            return self._build_switches(switches)

        # build and link hosts as last layer leaves
        hosts = []
        for host_num, switch in zip(range(1, 2**self.levels+1, 2),
                                    reversed(switches)):
            # build and attach left host
            left_host = 'h%s' % host_num
            hosts.append(left_host)

            # build right host
            right_host = 'h%s' % str(host_num+1)
            hosts.append(right_host)

        return list(reversed(switches)), hosts
    
# export so that we can use to enter mininet CLI
topos = {'mytopo': BinaryTreeTopo}
