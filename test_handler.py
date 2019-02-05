#from test_state_machine import TestStateMachine
#from touch2_lib.StateConfig import *
#from sage.all import *

#load('touch2_lib/touch_logging.py')
load('touch2_lib/StateConfig.py')
load('touch2_lib/State.py')
load('touch2_lib/StateMachine.py')
load('./test_state.py')
load('./test_state_machine.py')


class Handler(object):
    def __init__(self, g3):
        super(Handler, self).__init__()
        # init state machine
        self._sm = TestStateMachine()
        self._sm.config()
        self.g3 = g3

    def main(self):
        print_("Handler.main()")
        try:
            self.sm_loop()
        finally:
            print_('Store StateMachine obj before exit')
            return

    def stop_sm(self):
        self._sm.stop()

    def sm_loop(self):
        while True:
            try:
                if not self._sm.isStopped():
                    status = self._sm.run()
                    self._update(status)
                else:
                    return
            except Exception as e:  # TODO: distinguish exception type
                print('Error in sm_loop: %s' % type(e).__name__)
                print_('Error in sm_loop: %s' % type(e).__name__)
                raise e

    def _update(self,status):
        print_('handler._update')
        state_id = status.get("state_id")
        response = status.get("response")
        next_state_index=status.get("next_state_index")

        if status.get(StatusId.LOAD_GOOD3) is not None:
            # g3 = self._dh.loadData(FileId.FILE_GOOD3)
            self._sm.push_args(self.g3)

        if response is not None:
            if response.get("rel_of_pair_ready"):
                self._sm.state4._set_rel_of_pair(self._sm.current_state.rel)
                #save(self._sm.current_state.rel, 'RelOfPair_wid')

        if state_id == StateId.STOP_SM:
            print('STOP_SM')
            print_('STOP_SM')
            self.stop_sm()

    def __getstate__(self):
        print "I'm being pickled under Handler"
        self.handler_info = dict()
        self.handler_info['current_state_id'] = self._sm.current_state.state_id
        self.handler_info['current_state_stat'] = self._sm.current_state.stat

        self.handler_info['state1.max_sub_rel'] = self._sm.state1.max_sub_rel

        self.handler_info['state2.sub_rel'] = self._sm.state2.sub_rel
        self.handler_info['state2.max_sub_rel'] = self._sm.state2.max_sub_rel
        self.handler_info['state2.main_team'] = self._sm.state2.main_team

        return self.handler_info

    def __getitem__(self):
        return self.handler_info

# This is necessary for future GUI app
def main(g3):
    h = Handler(g3)
    h.main()

    return h


# Script starts
#g3 = [(1,2,3)]
#h=main(g3)

g3 = load('touch2_data/m16Jan_fix_g3_0')
main(list(map(tuple,g3)))