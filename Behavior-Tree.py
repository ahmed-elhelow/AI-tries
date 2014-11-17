class BT:
    valid_action_returns = ['SUCCESS', 'FAILURE', 'RUNNING']
    valid_types = ['SELECTOR', 'SEQUENCE']
    def __init__(self, node):
        self.node = node
        self.childs = []
        self.is_leaf = False    ##True=is_action
        self.is_selector = False
        self.is_sequence = False
        self.sel_or_seq = False
        self.action_return = None
        self.func = None

    def add_child(self, child):
        self.is_leaf = False
        self.childs.append(child)

    def give_return(self, action_return):
        if action_return in self.valid_action_returns:
            self.action_return = action_return

    def give_type(self, my_type):
        if my_type == self.valid_types[0]:
            self.is_selector = True
            self.is_sequence = False
            self.sel_or_seq = True
        elif my_type == self.valid_types[1]:
            self.is_selector = False
            self.is_sequence = True
            self.sel_or_seq = True

    def execute(self):
        if self.is_leaf:
            self.give_return(self.valid_action_returns[2])   #'RUNNING'
            action_return = self.func()
            self.give_return(action_return)
            self.print_node(); print        ######
            return action_return
        else:
            if self.sel_or_seq and self.is_selector:
                return self.do_selector()
            elif self.sel_or_seq and self.is_sequence:
                return self.do_sequence()

    def do_selector(self):
        action_return=None
        for ch in self.childs:
            action_return = ch.execute()
            if action_return=='SUCCESS':
                break
        self.give_return(action_return)
        self.print_node(); print        ######
        return action_return

    def do_sequence(self):
        action_return=None
        for ch in self.childs:
            action_return = ch.execute()
            if action_return=='FAILURE':
                break
        self.give_return(action_return)
        self.print_node(); print        ######
        return action_return

    def give_func(self, function):
        self.is_leaf = True
        self.is_selector = False
        self.is_sequence = False
        self.sel_or_seq = False
        self.func = function

    def print_node(self):
        print 'node:', self.node
        print 'childs num:', len(self.childs)
        print 'leaf:', self.is_leaf
        if self.sel_or_seq:
            print 'selector:', self.is_selector
            print 'sequence:', self.is_sequence
        print 'returned action:', self.action_return
        print 'func:', self.func
            

def check_battery():
    print 'check battery'
    return 'FAILURE'
def nav_dock():
    print 'nav dock'
    return 'SUCCESS'
def charge():
    print 'charge'
    return 'FAILURE'
def nav_0():
    print 'nav 0'
    return 'SUCCESS'
def nav_1():
    print 'nav 1'
    return 'SUCCESS'
def nav_2():
    print 'nav 2'
    return 'FAILURE'
def nav_3():
    print 'nav 3'
    return 'SUCCESS'

def test():
    bt = BT('behave')
    bt.give_type('SEQUENCE')
    
    t = BT('stay healthy')
    t.give_type('SELECTOR')    
    bt.add_child(t)

    t_ch = BT('check battery')
    t_ch.give_func(check_battery)
    t.add_child(t_ch)

    t_ch = BT('recharge')
    t_ch.give_type('SEQUENCE')
    t.add_child(t_ch)

    t_ch_ch = BT('nav dock')
    t_ch_ch.give_func(nav_dock)
    t_ch.add_child(t_ch_ch)

    t_ch_ch = BT('charge')
    t_ch_ch.give_func(charge)
    t_ch.add_child(t_ch_ch)
    
    t = BT('Patrol')
    t.give_type('SEQUENCE')    
    bt.add_child(t)

    t_ch = BT('nav 0')
    t_ch.give_func(nav_0)
    t.add_child(t_ch)

    t_ch = BT('nav 1')
    t_ch.give_func(nav_1)
    t.add_child(t_ch)

    t_ch = BT('nav 2')
    t_ch.give_func(nav_2)
    t.add_child(t_ch)

    t_ch = BT('nav 3')
    t_ch.give_func(nav_3)
    t.add_child(t_ch)
    
    bt.execute()

test()
