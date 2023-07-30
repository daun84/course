from enum import Enum

class EnumPostStatus(Enum):
    not_set = 'not_set'
    draft = 'draft'
    published = 'published'
    deleted = 'deleted'
