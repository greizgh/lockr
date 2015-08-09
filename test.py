from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from asyncio import coroutine


class TestComponent(ApplicationSession):
    @coroutine
    def onJoin(self, details):
        print("session ready")

        try:
            res = yield from self.call('lockr.seat.get_id')
            print("call result: {}".format(res))
        except Exception as e:
            print("call error: {0}".format(e))


if __name__ == '__main__':
    runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='lockr')
    runner.run(TestComponent)
