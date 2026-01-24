from dataclasses import dataclass


@dataclass
class ChangePassInAcc:

    current: str
    new: str
    repeat: str