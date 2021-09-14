from graphene import String, ObjectType

class QuoteType(ObjectType):
  id = String(required=True)
  quote = String(required=True)
  author = String(required=True)
