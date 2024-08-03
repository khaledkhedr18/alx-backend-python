from typing import NewType

UserId = NewType('UserId', int)

some_id = UserId(12345)
print(some_id)
