#from touch2_lib.State import State
#from touch2_lib.StateConfig import StatusId, StateId


class State_LoadData(State):
    def __init__(self):
        super(State_LoadData, self).__init__()
        self.state_id = StateId.LOAD_DATA

        self.g3 = []
        self.rel = {}
        self.rel_g_main_team = {}
        self.max_sub_rel = -1  # TODO: OK to set -1?

    def _reset(self):
        super(State_LoadData, self)._reset()

        # self.g3 = []
        # self.rel = {}
        # self.rel_g_main_team = {}
        # self.max_sub_rel = -1  # TODO: OK to set -1?

    def _entry(self):
        return {StatusId.LOAD_GOOD3: True}

    def set_args(self, args):
        if args is not None:
            self.g3 = args

    def _get_rel(self):
        for g in self.g3:
            # (1, 2, 3)
            self.rel.setdefault(g[::2], []).append(g[1]) # '[1, 3]': 2
            self.rel.setdefault(g[:2], []).append(g[-1]) # '[1, 2]': 3
            self.rel.setdefault(g[1:], []).append(g[0])  # '[2, 3]': 1

    def _body(self, pass_or_fail=True, response=dict(), err_msg=None):
        self._get_rel()
        response["rel_of_pair_ready"] = True

        # For this 1st run: sub_rel = rel
        self.max_sub_rel = max([len(r) for r in self.rel.values()])
        self.rel_g_main_team = {gmt: self.rel[gmt] for gmt in self.rel.keys() if len(self.rel[gmt]) == self.max_sub_rel}
        print('len(rel_g_main_team) = %s' % len(self.rel_g_main_team))
        print_(self.rel_g_main_team)

        if len(self.rel_g_main_team) > 0:
            pass_or_fail = True
        else:
            pass_or_fail = False

        return super(State_LoadData, self)._body(pass_or_fail=pass_or_fail, response=response)

    def get_args(self):
        return True, self.rel_g_main_team


class State_MultipleMainTeam(State):
    def __init__(self):
        super(State_MultipleMainTeam, self).__init__()
        self.state_id = StateId.MULTIPLE

        self.rel = {}
        self.sub_rel = {}
        self.main_team = []
        self.main_team_ut = 0
        self.max_sub_rel = -1   # TODO: OK to set -1?

    def _reset(self):
        super(State_MultipleMainTeam, self)._reset()

        #self.rel = {}
        #self.sub_rel = {}
        #self.main_team = []
        #self.main_team_ut = 0
        #self.max_sub_rel = -1 # TODO: OK to set -1?

    def set_args(self, args):
        print_('// STATE MultipleMainTeam set_args\n// ======================')
        if args is not None and len(args) > 0:
            if args[0]:
                self.sub_rel = {}
                self.main_team = []
                self.main_team_ut = 0
                self.max_sub_rel = -1  # TODO: OK to set -1?

                self.rel = args[1]
                self.main_team = args[1].keys()
                if len(self.main_team) > 0:
                    print('Got %s. Extend...' %(len(self.main_team[0])))
            else:
                self.sub_rel.update(args[1])
                self.main_team_ut += 1

    def _get_gmt(self):
        # return: gmt in format [(),...,()]
        self.max_sub_rel = max([len(rl) for rl in self.sub_rel.values()])
        self.rel_g_main_team = {gmt: self.sub_rel[gmt] for gmt in self.sub_rel.keys()
                                if len(self.sub_rel[gmt]) == self.max_sub_rel}

    def _body(self, pass_or_fail=True, response=dict(), err_msg=None):
        if self.main_team_ut == len(self.rel):
            pass_or_fail = False  # Stop
            self._get_gmt()
            print('len(rel_g_main_team) = %s' % len(self.rel_g_main_team))
            print_(self.rel_g_main_team)
            #fp = '/nas/lrz/home/ga87yop/gmt.sobj'
            fp = 'touch2_data/gmt_mytest1213.sobj'
            save(self.rel_g_main_team, fp)
        else:
            pass_or_fail = True  # Continue

        return super(State_MultipleMainTeam, self)._body(pass_or_fail=pass_or_fail)

    def get_args(self):
        if self.main_team_ut == len(self.rel):
            return self.rel_g_main_team, self.max_sub_rel
        else:
            return self.rel, self.main_team[self.main_team_ut]


class State_CheckStop(State):
    def __init__(self):
        super(State_CheckStop, self).__init__()
        self.state_id = StateId.CHECK_STOP

        self.max_sub_rel = -1 # TODO: OK to set -1?
        self.rel_g_main_team = {}
        
    def _reset(self):
        super(State_CheckStop, self)._reset()

        self.max_sub_rel = -1 # TODO: OK to set -1?
        #self.rel_g_main_team = {}

    def set_args(self, args):
        print_('// STATE CheckStop set_args\n// ======================')
        if args is not None and len(args) > 0:
            self.rel_g_main_team, self.max_sub_rel = args

    def _body(self, pass_or_fail=True, response=dict(), err_msg=None):
        if self.max_sub_rel == 0:
            self.pass_or_fail = False    # Stop
        else:
            self.pass_or_fail = True     # Continue

        return super(State_CheckStop, self)._body(pass_or_fail=self.pass_or_fail)

    def get_args(self):
        if self.pass_or_fail:
            return True, self.rel_g_main_team
        else:
            # Easily skip by return
            return


class State_FindRel(State):
    def __init__(self):
        super(State_FindRel, self).__init__()
        self.state_id = StateId.FIND_REL

        self.rel = dict()
        self.sub_rel = dict()
        self.new_rel = set()
        self.size_new_rel = -1   # TODO

    def _reset(self):
        super(State_FindRel, self)._reset()

        # self.rel = dict()
        #self.sub_rel = dict()
        self.new_rel = set()
        self.size_new_rel = -1  # TODO

    def _set_rel_of_pair(self, rop):
        self.rel_of_pair = rop

    def set_args(self, args):
        print_('// STATE FindRel set_args\n// ======================')
        if args is not None and len(args) > 0:
            self.sub_rel = dict()

            self.rel = args[0]
            self.main_team = args[-1]

    def _get_rel(self, e1, e2):
        temp = tuple(sorted([e1, e2]))
        if self.rel_of_pair.get(temp) is not None:
            return self.rel_of_pair[temp]
        else:
            return []

    def _get_good_sub_team(self):
        mtl = list(self.main_team)
        for r in self.rel[self.main_team]:
            new_rel_list = [self._get_rel(e1, r) for e1 in self.main_team]
            self.new_rel = set(self.rel[self.main_team]).intersection(*[set(nr) for nr in new_rel_list])

            if len(self.new_rel) > self.size_new_rel:
                self.size_new_rel = len(self.new_rel)

                mtl.append(r)
                n_main_team = tuple(sorted(mtl))
                self.sub_rel = dict()
                self.sub_rel[n_main_team] = list(self.new_rel)
                del(mtl[-1])
            elif len(self.new_rel) == self.size_new_rel:
                # TODO: Manage case: len(self.new_rel) == self.size_new_rel == 0
                # example:  (76, 144, 201): [], (76, 156, 201): []
                mtl.append(r)
                n_main_team = tuple(sorted(mtl))
                self.sub_rel[n_main_team] = list(self.new_rel)
                del (mtl[-1])

    def _body(self, pass_or_fail=True, response=dict(), err_msg=None):
        self._get_good_sub_team()
        return super(State_FindRel, self)._body()

    def get_args(self):
        return False, self.sub_rel


class State_StopSM(State):
    def __init__(self):
        super(State_StopSM, self).__init__()
        self.state_id = StateId.STOP_SM
