"""This module contains the core classes of the launchers infrastructure."""

from abc import ABC, abstractmethod
from typing import Optional, List, Type, Dict

from psi.j.job_executor_config import JobExecutorConfig
from psi.j.job import Job


class Launcher(ABC):
    """An abstract base class for all launchers."""

    _launchers = {}  # type: Dict[str, Type[Launcher]]

    def __init__(self, config: Optional[JobExecutorConfig] = None) -> None:
        """
        Base constructors for launchers.

        :param config: An optional configuration. If not specified,
            :attr:`~psi.j.JobExecutorConfig.DEFAULT` is used.
        """
        if config is None:
            config = JobExecutorConfig.DEFAULT
        self.config = config

    @abstractmethod
    def get_launch_command(self, job: Job) -> List[str]:
        """
        Constructs a command to launch a job given a job specification.

        :param job: The job to launch.
        :return: A list of strings representing the launch command and all of its arguments.
        """
        pass

    @staticmethod
    def get_instance(name: str, config: Optional[JobExecutorConfig] = None) -> 'Launcher':
        """
        Returns an instance of a launcher optionally configured using a certain configuration.

        The returned instance may or may not be a singleton object.

        :param name: The name of the launcher to return an instance of.
        :param config: An optional configuration.
        :return: A launcher instance.
        """
        if name not in Launcher._launchers:
            raise ValueError('No such launcher: "{}"'.format(name))
        lcls = Launcher._launchers[name]
        return lcls(config=config)

    @staticmethod
    def register_launcher(lcls: Type['Launcher']) -> None:
        """
        Registers a launcher class.

        The registered class cang then be instantiated using
            :func:`~psi.j.Launcher.get_instance`.

        :param lcls: The launcher class to register.
        """
        if not hasattr(lcls, '_NAME_'):
            raise ValueError('Class is missing the launcher name attribute, "_NAME_"')
        name = getattr(lcls, '_NAME_')
        Launcher._launchers[name] = lcls
