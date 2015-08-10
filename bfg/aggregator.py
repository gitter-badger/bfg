import threading as th
import queue
import multiprocessing as mp
from .module_exceptions import ConfigurationError
from .util import AbstractFactory
import asyncio
import logging


LOG = logging.getLogger(__name__)


class ResultsSink(object):
    def __init__(self, event_loop):
        self.event_loop = event_loop
        self.results = {}
        self.results_queue = mp.Queue()
        self._stopped = th.Event()
        self.event_loop.create_task(self._reader())

    def stop(self):
        self._stopped.set()

    @asyncio.coroutine
    def _reader(self):
        LOG.info("Results reader started")
        while not self._stopped.is_set():
            try:
                sample = self.results_queue.get_nowait()
                self.results.setdefault(sample.ts, []).append(sample)
            except queue.Empty:
                if self._stopped.is_set():
                    LOG.info("Stopping results reader")
                    return
                else:
                    yield from asyncio.sleep(1)


class AggregatorFactory(AbstractFactory):
    FACTORY_NAME = "aggregator"

    def __init__(self, component_factory):
        super().__init__(component_factory)
        self.results = ResultsSink(self.event_loop)

    def get(self, key):
        if key in self.factory_config:
            return self.results
        else:
            raise ConfigurationError(
                "Configuration for %s schedule not found" % key)
