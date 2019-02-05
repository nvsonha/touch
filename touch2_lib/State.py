

class State(object):
    def __init__(self):
        super(State, self).__init__()
        self.stat = "__init__"
        self._reset()

    def _reset(self):
        self.gen = self._gen()  # this gen is called in StateMachine.run()

    def _entry(self):
        return {"state_id": self.state_id}

    def _body(self, pass_or_fail=True, response=dict(), err_msg=None):
        response["pass_or_fail"] = pass_or_fail
        return {"response": response, "err_msg": err_msg}

    def _exit(self, pass_or_fail):
        index = 0 if pass_or_fail else 1    # if good: next state, else: stay same state
        return {"next_state_index": index}

    def set_args(self, args):
        pass

    def get_args(self):
        return

    def _gen(self):
        self.stat = "entry"
        yield self._entry()

        self.stat = "body"
        status = self._body()
        yield status

        self.stat = "exit"
        pass_or_fail = status.get("response").get("pass_or_fail")
        status = self._exit(pass_or_fail)
        self._reset()

        yield status

