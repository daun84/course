from dataclasses import field
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class EventComponentButton:
    linked_item: object
    linked_enum: object

