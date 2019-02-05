#from touch2_lib.StateMachine import StateMachine
#from test_state import *


class TestStateMachine(StateMachine):
    def config(self):
        self.state1 = State_LoadData()

        self.state2 = State_MultipleMainTeam()
        self.state3 = State_CheckStop()

        self.state4 = State_FindRel()

        self.state0 = State_StopSM()

        self.transition_table = {
            self.state1: (self.state2, self.state0),
            self.state2: (self.state4, self.state3),
            self.state3: (self.state2, self.state0),
            self.state4: (self.state2, self.state2)
        }
        self.init_state = self.state1

        self.current_state = self.init_state

    def push_args(self,args):
        self.current_state.set_args(args)

