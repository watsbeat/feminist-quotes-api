from dotenv import load_dotenv

from fastapi import Security, Depends, Request, FastAPI, HTTPException, APIRouter
from fastapi.security.api_key import APIKeyHeader

from graphene import ObjectType, List, String, Schema, Field, Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor

from starlette.graphql import GraphQLApp
from starlette import status

from schemas import QuoteType
import os
import json

load_dotenv()

API_KEY = os.environ['API_KEY']
API_KEY_NAME = os.environ['API_KEY_NAME']

api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def check_authentication_header(api_key_header: str = Security(api_key_header_auth)):
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

router = APIRouter()
app = FastAPI(title=f"FeministQuoteGenerator")

# Unsecured endpoint
@app.get("/")
async def root():
    return {"message": "Welcome, Feminist 💁🏻‍♀️"}

# Secured endpoint
@app.get("/secure", dependencies=[Security(check_authentication_header)])
async def secure_endpoint():
    return {"message": "This is a secure endpoint"} 

class Query(ObjectType):
    quote_list = None
    get_quote = Field(List(QuoteType), id=String())

    async def resolve_get_quote(self, info, id=None):
        with open("./quotes.json") as quotes:
            quote_list = json.load(quotes)
        if (id):
            for quote in quote_list:
                if quote['id'] == id: return [quote]
        return quote_list

class CreateQuote(Mutation):
    quote = Field(QuoteType)

    class Arguments:
        id = String(required=True)
        quote = String(required=True)
        author = String(required=True)

    async def mutate(self, info, id, quote, author):
        with open("./quotes.json", "r+") as quotes:
            quote_list = json.load(quotes)

            for quote in quote_list:
                if quote['id'] == id:
                    raise Exception('Quote with provided id already exists')

            quote_list.append({"id": id, "quote": quote, "author": author})
            quotes.seek(0)
            json.dump(quote_list, quotes, indent=2)
        return CreateQuote(quote=quote_list[-1])

class Mutation(ObjectType):
    create_quote = CreateQuote.Field()

graphql_app = GraphQLApp(
    schema=Schema(query=Query, mutation=Mutation),
    executor_class=AsyncioExecutor
)

@router.api_route("/graphql", methods=["GET", "POST"])
async def graphql(
    request: Request,
    authorize: str = Depends(check_authentication_header)
):
    request.state.authorize = authorize
    return await graphql_app.handle_graphql(request=request)

app.include_router(router)
