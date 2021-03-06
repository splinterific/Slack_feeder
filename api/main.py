from flask import Blueprint, json, Flask, request
from databases import db
import os
from SlackFeedr import parse
from slackclient import SlackClient
from blocks_builds import block
import pprint

api = Blueprint("api", __name__, url_prefix="/api")
blockout = block.Blocks_class()
keygrab = db.MongoRepository()


@api.route("/add_feed", methods=["POST"])
def add_rss_feed_subscription():
    """Add feed endpoint
    Returns:
        [string] -- [confirmation of RSS Feed]
    Expects:
        token=gIkuvaNzQIHg97ATvDxqgjtO
        &team_id=T0001
        &team_domain=example
        &enterprise_id=E0001
        &enterprise_name=Globular%20Construct%20Inc
        &channel_id=C2147483705
        &channel_name=test
        &user_id=U2147483697
        &user_name=Steve
        &command=/weather
        &text=94070
        &response_url=https://hooks.slack.com/commands/1234/5678
        &trigger_id=13345224609.738474920.8088930838d88f008e0
    Information:
        https://api.slack.com/slash-commands
    """
    try:
        payload = request.form.to_dict()
        feed_url = payload["text"]
        # response_url = payload["response_url"]
        if not feed_url:
            return "please enter some text e.g. `/add_feed test.com`"
        else:
            test_feed = parse.test_rss_feed(feed_url)

            if test_feed["status"] is True:
                key = keygrab.key_grab(payload["team_id"])
                sc = SlackClient(key["bot_token"])
                sc.api_call(
                    "chat.postMessage",
                    channel=payload["channel_id"],
                    text="hi",
                    blocks=blockout.success_block_preview(
                        feed_subtext=test_feed["feed_subtext"],
                        feed_link=feed_url,
                        feed_title=test_feed["title"],
                        feed_summary=test_feed["feed_summary"],
                        feed_entry_link=test_feed["feed_entry_link"],
                    ),
                )
                return ""
            else:
                return f"{feed_url} is not a valid RSS feed. Please see <https://rss.com/rss-feed-validators/|this link> for some feed validators"
    except:
        return "sorry, you've experienced an error"


@api.route("/remove_feed", methods=["POST"])
def remove_rss_feed_subscription():
    # Add a confirm removal block here, or perhaps a confirm box?
    return "removed feed"


@api.route("/actions", methods=["POST"])
def action_route():
    payload = json.loads(request.form.get("payload"))
    for button_payload in payload["actions"]:
        if button_payload["block_id"] == "add_decline":
            if button_payload["value"] == "add_rss_feed":
                keygrab.add_feed(
                    user_id=payload["user"]["id"],
                    feed_url=button_payload["action_id"],
                    channel=payload["channel"]["id"],
                    workspace=payload["user"]["team_id"],
                    latest="last_feed",
                )
                return "that worked"
            elif button_payload["value"] == "cancel":
                return "cancelled"
        else:
            return "try again"
