#!/usr/bin/env python
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
import uuid


class SeatComponent(ApplicationSession):
    _free = True
    _locker_id = ""

    def get_id(self):
        """Get unique identifier"""
        return str(uuid.uuid4())

    def refresh(self):
        """Send lock/unlock events according to current seat state"""
        if self._free:
            self.publish('lockr.seat.unlocked', self._locker_id)
        else:
            self.publish('lockr.seat.locked', self._locker_id)

    def lock(self, client):
        """Lock the resource

        Returns True if successfully locked, False otherwise
        """
        if not self._free:
            return False
        else:
            self._locker_id = client
            self._free = False
            self.refresh()
            return True

    def unlock(self, client):
        """Release the resource

        Returns True if successfully released, False otherwise
        """
        if not self._free and client == self._locker_id:
            self._free = True
            self.refresh()
            return True
        else:
            return False

    @coroutine
    def onJoin(self, details):
        try:
            yield from self.register(self.get_id, 'lockr.seat.get_id')
            yield from self.register(self.lock, 'lockr.seat.lock')
            yield from self.register(self.unlock, 'lockr.seat.unlock')
            yield from self.subscribe(self.refresh, 'lockr.seat.refresh')
        except Exception as e:
            print("Register error: {}".format(e))

if __name__ == '__main__':
    runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='lockr')
    runner.run(SeatComponent)
