from flask_login import current_user
from notion.client import NotionClient
from app.models import Highlight
from sqlalchemy import desc, func
from app import db


# Get Client
def notion_client():
    client = NotionClient(token_v2=current_user.token_v2)
    return client


# Get Highlights
def get_Highlights(link):
    client = notion_client()
    page = client.get_block(link)

    # Getting all bulleted list
    for child in page.children:
        if child.type == "bulleted_list":
            highlight = Highlight(
                title=page.title, highlight=child.title, author=page.author, tags=str(page.tags), user_id=current_user.id)
            db.session.add(highlight)

    db.session.commit()


def get_daily_highlights():
    highlights = Highlight.query.filter(Highlight.user_id == current_user.id).order_by(func.random()).limit(5).all()
    return highlights
