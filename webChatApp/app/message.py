import dataclasses

@dataclasses.dataclass
class Message:
    """description of class"""
    room_no: int
    username: str
    regist_date: str
    regist_time: str
    message: str
    kbn: str
    file_path: str