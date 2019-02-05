#from touch2_lib.State import State
#from touch2_lib.StateConfig import *


class StateMachine(object):
    STOPPED = 0
    RUNNING = 1

    def __init__(self):
        super(StateMachine, self).__init__()
        self.transition_table = dict()
        self.current_state = None
        self.init_state = None
        self.sm_stat = self.RUNNING

    def config(self):
        self.sm_stat = self.RUNNING
        state0, state1 = State(), State()
        self.transition_table = {
            state0: (state1, state0),
            state1: (state0, state1)
        }
        self.current_state = state0

    def run(self):
        print_('StateMachine.run()')
        try:
            status = next(self.current_state.gen)
        except Exception as e:
            # TODO: Do we need reset here? It might useful when SM restarts
            #self.current_state._reset()
            print_("StateMachine.run() runtime error: %s" % type(e).__name__)
            raise e
        self._next_state(status)
        return status

    def stop(self):
        self.sm_stat = self.STOPPED

    def isStopped(self):
        return self.sm_stat == self.STOPPED

    def _next_state(self,status):
        print_('StateMachine._next_state()')
        index = status.get("next_state_index")
        if index is None: return
        print_('GET args of current_state to set for next_state')
        args = self.current_state.get_args()
        print_('GET args OK')
        self.current_state = self.transition_table.get(self.current_state)[index]
        self.current_state.set_args(args)
        print_('SET args for next_state OK')

