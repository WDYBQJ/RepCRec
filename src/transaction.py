# -----------------------------------------------------------------------------
# transcation.py
#
# Classes for transactions
# -----------------------------------------------------------------------------

import time
from enum import Enum

#~ Status = Enum('created', 'ready', 'running', 'blocked', 'terminated')
class Status(Enum):
	created = 1
	ready = 2
	running = 3
	blocked = 4
	terminated = 5

class TransactionBase(object):
	def __init__(self, name, status=Status.created):
		self.name = name
		self.status = status
		self.create_time = time.time() # might be useful for killing
	def set_status(self, status):
		self.status = status
	def commit(self):
		self.set_status(Status.terminated)


class ReadWriteTransaction(TransactionBase):
	pass


class ReadOnlyTransaction(TransactionBase):
	pass
