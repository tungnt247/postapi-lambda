import dataclasses
from typing import Optional
from services.database import db
from services.upload_image import UploadImageService


@dataclasses.dataclass
class Post:
    id: int
    title: str
    content: str
    image: Optional[str] = None

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k not in names:
                raise ValueError(f'{k} is invalid field!')

            setattr(self, k, v)

    def save(self):
        db.tables['posts'].put_item(Item=dataclasses.asdict(self))

    @classmethod
    def all(self) -> list:
        return db.tables['posts'].scan()['Items']

    @classmethod
    def update(self, pk, **kwargs):
        if not kwargs.get('title'):
            raise ValueError('title is required')

        if not kwargs.get('content'):
            raise ValueError('content is required')

        if kwargs.get('image'):
            service = UploadImageService()
            url = service.upload(post_id=pk, image=kwargs['image'])
        else:
            post = self.retrieve(pk)
            url = post['image']

        db.tables['posts'].update_item(
            Key={'id': pk},
            AttributeUpdates={
                'title': {
                    'Value'  : kwargs['title'],
                    'Action' : 'PUT'
                },
                'content': {
                    'Value'  : kwargs['content'],
                    'Action' : 'PUT'
                },
                'image': {
                    'Value'  : url,
                    'Action' : 'PUT'
                }
            }
        )

    @classmethod
    def delete(self, pk):
        db.tables['posts'].delete_item(Key={'id': pk})

    @classmethod
    def retrieve(self, pk):
        item = db.tables['posts'].get_item(Key={'id': pk}).get('Item')
        if not item:
            return None
        return item
