import graphene
from charivol.models import DonationStatus as DonationStatusModel
from charivol.models import DonationTypeItems as DonationTypeItemsModel

class DonationTypeOptions(graphene.Enum):
    CLOTHING = DonationTypeItemsModel.CLOTHING
    FOOD = DonationTypeItemsModel.FOOD
    STATIONERY = DonationTypeItemsModel.STATIONERY
    BOOK = DonationTypeItemsModel.BOOK
    TOY = DonationTypeItemsModel.TOY
    FOOTWEAR = DonationTypeItemsModel.FOOTWEAR
    FURNITURE = DonationTypeItemsModel.FURNITURE
    OTHER = DonationTypeItemsModel.OTHER

class DonationStatusOptions(graphene.Enum):
    PENDING = DonationStatusModel.PENDING
    ACCEPTED = DonationStatusModel.ACCEPTED
    REJECTED = DonationStatusModel.REJECTED