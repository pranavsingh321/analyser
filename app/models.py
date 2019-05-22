from app import db
from sqlalchemy.utils.types.choice import ChoiceType

class CampaignAnalysis(db.Model):
    id = db.Column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    campaign_id = db.Column(db.Integer)
    sentiment = db.Column(db.String(255))
    keywords = db.Column(db.String(255))


class CampaignReview(db.Model):
    REVIEW_TYPES = [
       ('neg', 'Negative'),
       ('neu', 'Neutral')
       ('pos', 'Positive')
    ]

    type = Column(ChoiceType(REVIEW_TYPES), default=u'neu')
    comment = db.Column(db.String(255))
    campaign_analysis = db.relationship(
        "CampaignAnalysis", backref=db.backref("reviews", l_azy=True)
    )
