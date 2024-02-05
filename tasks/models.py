from pydantic import BaseModel, Field

class Bronze(BaseModel):
    """
        Pydantic model for bronze data schema
    """

    title: str
    url: str
    self_url: str
    domain: str
    flair: str
    create_date: str
    user: str
    user_link: str
    comments: int = Field(ge=0)
    upvotes: str

class Silver(Bronze):
    """
        Pydantic model for silver data schema
    """

    upvotes: int = Field(ge=-1)
    post_type: str
    create_timestamp: str
    create_time: str
    created_at: str
    upvote_range: str
