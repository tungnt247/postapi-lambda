from flask_dynamo import Dynamo
from boto3.session import Session


db = Dynamo()

def init_database(app):
    db.init_app(app)
    app.config['DYNAMO_TABLES'] = [
        dict(
            TableName='posts',
            KeySchema=[dict(AttributeName='id', KeyType='HASH')],
            AttributeDefinitions=[dict(AttributeName='id', AttributeType='S')],
            BillingMode='PAY_PER_REQUEST'
        )
    ]

    with app.app_context():
        db.create_all()

    return db
