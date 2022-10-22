from abc import ABC, abstractmethod


class AbstractUnitOfWorks(ABC):

    def __enter__(self):
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def rollback(self):
        ...
