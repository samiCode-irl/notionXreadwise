from flask_login import current_user
from notion.client import NotionClient
from app.models import Highlight
from sqlalchemy import func
from app import db
import re

previous_data = dict()

# Get Client
def notion_client():
    client = NotionClient(token_v2=current_user.token_v2)
    return client


# Get Highlights
def get_highlights(link):
    client = notion_client()
    page = client.get_block(link)

    # Getting all bulleted list
    for child in page.children:
        if child.type == "bulleted_list":
            highlight = Highlight(
                title=page.title, highlight=child.title, author=page.author, tags=str(
                    page.tags), user_id=current_user.id)
            db.session.add(highlight)

    db.session.commit()


# Filter 5 random highlights from the database
def get_daily_highlights(no):
    highlights = Highlight.query.filter(
        Highlight.user_id == current_user.id).order_by(func.random()).limit(no).all()
    return highlights


# Compare highlights
def compare_highlights(highlights, time):
    confirmed_list = highlights
    if time not in previous_data:
        previous_data[time] = highlights
        return previous_data[time]
    else:
        confirmed_list = previous_data[time]
        for i in confirmed_list:
            if i.user_id != current_user.id:
                confirmed_list.pop(i)
                confirmed_list.append(get_daily_highlights(1))

        return confirmed_list


# Get Tags for Highlights
def get_tags():
    tag_list = list()
    tags = db.session.query(Highlight.tags).filter(
        Highlight.user_id == current_user.id).all()
    for i in tags:
        done = re.findall(r"'(.*?)'", str(i))
        for i in done:
            if i.lower() not in tag_list:
                tag_list.append(i.lower())

    return(tag_list)
