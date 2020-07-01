import datetime
import json
import re
import time
import collections
from flags import Flags
from lxml import etree

userpic_urls: dict = {}
analysis_todo: dict = {}
DEF_FLAGS = """
notext hastext 
noemoji hasemoji  
noattachment hasattachment 
noforward hasforward isforward
graffiti sticker voice 
"""
flag = Flags("Message Flags", DEF_FLAGS)


class Object:
    def __init__(self, d: dict):
        for key, value in d.items():
            self.__setattr__(key, value)

    def type(self):
        return self.__class__.__qualname__


class Message(Object):
    __slots__ = ("msgid", "date_info", "user_info",
                 "text_info", "attachments", "forwards", "flags")


class DateInfo(Object):
    __slots__ = ("time", "date")


class UserInfo(Object):
    __slots__ = ("userid", "userlink",
                 "userpic", "username")


class TextInfo(Object):
    __slots__ = ("text", "emoji",
                 "length_words",
                 "length_symbols_spaces",
                 "length_symbols_no_spaces",)


class Attachment(Object):
    __slots__ = ("att_type",
                 "att_link",
                 "att_link_text",
                 "att_wall_text",
                 "att_wall_attachments")


class Forward(Object):
    __slots__ = ("msgid", "date_info", "user_info",
                 "text_info", "attachments", "forwards", "flags")


def parse_file(file_path: str, batch_amount: int):
    with open(file_path, "rb") as file:
        tree = etree.iterparse(file, html=True, huge_tree=True, events=("start", "end"))

        batch_list = []

        pt1 = time.perf_counter()

        for event, elem in tree:
            if event == "end":
                msg_amount(elem)
                if elem.tag == "div":
                    if "id" in elem.attrib:
                        batch_list.append(parse_message(elem))
                        elem.clear()
                        if len(batch_list) == batch_amount:
                            print(f"Пропарсил {batch_amount} сообщений за {round(time.perf_counter()-pt1, 3)}")
                            pt1 = time.perf_counter()

                            global analysis_todo
                            analysis_dict = analyse(analysis_todo)
                            analysis_todo.clear()

                            yield batch_list, analysis_dict
                            batch_list = []

        if len(batch_list) > 0:
            analysis_dict = analyse(analysis_todo)
            analysis_todo.clear()

            yield batch_list, analysis_dict

        tree = ()


def msg_amount(elem):
    textp = re.compile(r" Всего сообщений:")
    intp = re.compile(r"\d+")
    if elem.tag == "h4" and elem.text:
        if re.match(textp, elem.text):
            amount = re.search(intp, elem.text).group()
            print(f"Всего сообщений: {amount}")


def parse_message(message_item):
    # получение msgid
    if "id" in message_item.attrib:
        msgid = message_item.attrib["id"]
    else:
        msgid = "fwd"

    from_contents = message_item.findall(".div[@class='from']*")

    user_info = parse_user_info(message_item, from_contents, msgid)
    date_info = parse_date_info(from_contents, msgid)
    text_info = parse_text_info(message_item)
    attachments = parse_attachments(message_item)
    forwards = parse_forwards(message_item)
    flags = parse_flags(msgid, text_info, attachments, forwards)

    message_info = {"user_info": user_info, "date_info": date_info,
                    "text_info": text_info, "attachments": attachments,
                    "forwards": forwards}

    global analysis_todo
    analysis_todo[msgid] = message_info
    message_info.update({"msgid": msgid,
                         "flags": flags})

    if msgid == "fwd":
        return Forward(message_info)
    else:
        return Message(message_info)


def parse_user_info(message_item, from_contents, msgid):
    upic_contents = message_item.find(".div[@class='upic']*")
    userid = from_contents[1].text
    username = from_contents[0].text
    userlink = from_contents[1].attrib["href"]
    userpic = upic_contents.attrib["src"]

    global userpic_urls
    if userid not in userpic_urls and msgid != "fwd":
        userpic_urls[userid] = userpic

    return UserInfo({"userid": userid,
                     "username": username,
                     "userlink": userlink,
                     "userpic": userpic})


def parse_date_info(from_contents, msgid):
    if msgid == "fwd":
        date_raw = from_contents[1].tail.strip()
    else:
        date_raw = from_contents[2].text
    date = datetime.datetime.strptime(date_raw, "%Y.%m.%d %X").strftime("%d.%m.%Y")
    time_ = datetime.datetime.strptime(date_raw, "%Y.%m.%d %X").strftime("%X")

    return DateInfo({"date": date,
                     "time": time_})


def parse_text_info(message_item):
    msg_body = message_item.find(".div[@class='msg_body']")

    if msg_body is not None:
        text, emoji = get_text_emoji(msg_body)
        length_words = len(text.split())
        length_symbols_spaces = len(text)
        length_symbols_no_spaces = len("".join(text.split()))
        if not length_symbols_no_spaces == 0:
            return TextInfo({"text": text,
                             "length_words": length_words,
                             "length_symbols_spaces": length_symbols_spaces,
                             "length_symbols_no_spaces": length_symbols_no_spaces,
                             "emoji": emoji})
        else:
            return None
    else:
        return None


def get_text_emoji(msg_body):
    msg_body_elems = msg_body.xpath(".//node()")
    text = ""
    emoji = []

    for elem in msg_body_elems:
        if type(elem) == etree._Element and elem.tag == "img":
            text += elem.attrib["alt"]
            emoji.append(elem.attrib["alt"])
        elif type(elem) == etree._Element and elem.tag == "br":
            text += "\n"
        elif type(elem) == etree._Element and elem.tag == "a":
            text += elem.text
        elif type(elem) == etree._ElementUnicodeResult:
            text += elem
    return text, emoji


def parse_attachments(message_item):
    if message_item.find(".div[@class='attacments']") is not None:
        return get_attachments(message_item)
    else:
        return None


def get_attachments(message_item):
    attachments_list = []
    for att in message_item.xpath("div"):
        if "class" in att.attrib:
            if att.attrib["class"] in ("attacment", "attacment attb_link"):
                attachment = parse_attachment(att)
                attachments_list.append(Attachment(attachment))
        elif "style" in att.attrib:
            attachments_list.append(Attachment({"att_type": "conf_userpic_update",
                                                "att_link": None,
                                                "att_link_text": "обновил(а) фотографию беседы:"}))
        else:
            print("Неизвестный тип сообщения")
            raise TypeError
    return attachments_list


def parse_attachment(attachment):
    # если аттачмент преобразован (нет тэга <pre>)
    if attachment.find(".pre") is None:
        if attachment.attrib["class"] == "attacment":
            return get_att_info(attachment)
        elif attachment.attrib["class"] == "attacment attb_link":
            return get_attb_link(attachment)
    else:
        return get_pre(attachment)


def get_att_info(attachment):
    attachment_contents = attachment.xpath("*")
    att_link = attachment_contents[1].attrib["href"]
    att_link_text = attachment_contents[1].text
    att_type = get_att_type(attachment, att_link_text)
    att_info = {"att_type": att_type,
                "att_link": att_link,
                "att_link_text": att_link_text}
    if att_type == "att_wall":
        return {**att_info, **get_att_wall(attachment, attachment_contents)}
    return att_info


def get_att_type(attachment, att_link_text):
    att_type = re.sub(r"[^\w]", " ", attachment.xpath("*")[0].attrib["class"]).split()[1]
    graffiti_pattern = re.compile(r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\.png")
    voice_pattern = re.compile(r"(audio_msg|voice_message|audiocomment|(\d+_\d+))\.(opus|webm|3gp|ogg)")

    if att_type == "att_doc":
        if graffiti_pattern.match(att_link_text):
            att_type = "att_graffiti"
            return att_type
        elif voice_pattern.match(att_link_text):
            att_type = "att_voice"
            return att_type
    return att_type


def get_att_wall(attachment, attachment_contents):
    if not attachment_contents[2].text == " ":
        att_wall_text = attachment_contents[2].text
    else:
        att_wall_text = "<Без текста>"

    att_wall_attachments = []
    for wall_attachment in attachment.findall("./div[@class='attacment']") or \
                           attachment.findall(".div[@class='attacment attb_link']"):
        att_wall_attachments.append(parse_attachment(wall_attachment))

    return {"att_wall_text": att_wall_text,
            "att_wall_attachments": att_wall_attachments}


def get_attb_link(attachment_contents):

    att_type = "attb_link"
    att_link = attachment_contents[1].attrib["href"]
    att_link_text = attachment_contents[1].xpath("text()")[0]
    return {"att_type": att_type,
            "att_link": att_link,
            "att_link_text": att_link_text}


def get_pre(attachment):
    data = json.loads(attachment.find(".pre").text, strict=False)  # json в словарь
    att_type = data["type"]
    pre_info = {"att_type": att_type}

    if att_type == "market":
        return {**pre_info, **get_pre_market(data)}

    elif att_type == "poll":
        return {**pre_info, **get_pre_poll(data)}

    elif att_type == "photos_list":
        return {**pre_info, **get_pre_photos_list(data)}
    else:
        return get_pre_unknown(att_type)


def get_pre_market(data):
    owner = str(data["market"]["owner_id"] * -1)
    product_id = str(data["market"]["id"])
    att_link = "https://vk.com/market-%s?w=product-%s_%s" % (owner, owner, product_id)
    att_link_text = data["market"]["title"]
    return {"att_link": att_link,
            "att_link_text": att_link_text}


def get_pre_poll(data):
    owner = str(data["poll"]["owner_id"] * -1)
    poll_id = str(data["poll"]["id"])
    att_link = "https://vk.com/poll%s_%s" % (owner, poll_id)
    att_link_text = data["poll"]["question"]
    return {"att_link": att_link,
            "att_link_text": att_link_text}


def get_pre_photos_list(data):
    att_link = "https://vk.com/photo%s" % (data["photos_list"][0])
    att_link_text = "Фотоальбом"
    return {"att_link": att_link,
            "att_link_text": att_link_text}


def get_pre_unknown(att_type):
    att_link = "?"
    att_link_text = f"Тип {att_type} не поддерживается"
    return {"att_type": att_type,
            "att_link": att_link,
            "att_link_text": att_link_text}


def parse_forwards(message_item):
    if message_item.find(".div[@class='fwd']") is not None:
        forward = message_item.find(".div[@class='fwd']")
        return get_forwards(forward)
    else:
        return None


def get_forwards(head_tag):
    forwards = head_tag.xpath("*")
    forwards_list = []
    for forward in forwards:
        forward_info = parse_message(forward)
        forwards_list.append(forward_info)
    return forwards_list


def parse_flags(msgid, text_info, attachments, forwards):
    att_conditions = bool(attachments) and len(attachments) == 1
    flag_conditions = {flag.isforward: msgid == "fwd",
                       flag.hastext: bool(text_info),
                       flag.hasemoji: bool(text_info) and bool(text_info.emoji),
                       flag.notext: text_info is None,
                       flag.hasattachment: bool(attachments),
                       flag.sticker: att_conditions and attachments[0].att_type == "att_sticker",
                       flag.graffiti: att_conditions and attachments[0].att_type == "att_graffiti",
                       flag.voice: att_conditions and attachments[0].att_type == "att_voice",
                       flag.hasforward: bool(forwards)}

    flags = flag.no_flags
    for fl, cond in flag_conditions.items():
        if cond:
            flags = flags | fl
    return flags


def analyse(todo: dict):
    most_words_cntr = collections.Counter()
    most_emojis_cntr = collections.Counter()
    words_amount = 0
    symbols_amount = 0
    stickers_amount = 0
    emojis_amount = 0

    for message in todo.values():
        if message["text_info"]:
            length_words = message["text_info"].length_words
            length_symbols = message["text_info"].length_symbols_no_spaces
            text = message["text_info"].text
            emojis = message["text_info"].emoji
            words_amount += length_words
            symbols_amount += length_symbols

            for word in text.lower().split():
                most_words_cntr[word] += 1

            if emojis is not None:
                emojis_amount += len(emojis)
                for emoji in emojis:
                    most_emojis_cntr[emoji] += 1

        if message["attachments"]:
            for attachment in message["attachments"]:
                if attachment.att_type == "att_sticker":
                    stickers_amount += 1

    analysis_dict = {"most_words": most_words_cntr,
                     "words_amount": words_amount,
                     "symbols_amount": symbols_amount,
                     "stickers_amount": stickers_amount,
                     "emojis_amount": emojis_amount,
                     "most_emojis": most_emojis_cntr}

    return analysis_dict