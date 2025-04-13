from pydantic import BaseModel

# Request schema
class UserRequest(BaseModel):
    userID: int
