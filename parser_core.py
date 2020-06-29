import datetime
import json
import re
import time
import collections
from flags import Flags
from lxml import etree

userpic_urls: dict = {}
analysis_todo: dict = {}
flags = """
notext hastext hasemoji noemoji noattachment
hasattachment graffiti sticker voice 
noforward hasforward isforward
"""
flag = Flags("Message Flags", flags)


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
    textp = re.compile(" Всего сообщений:")
    intp = re.compile("\d+")
    if elem.tag == "h4" and elem.text:
        if re.match(textp, elem.text):
            amount = re.search(intp, elem.text).group()
            print(f"Всего сообщений: {amount}")


def parse_message(message_item):
    flags = flag.no_flags
    # получение msgid
    if "id" in message_item.attrib:
        msgid = message_item.attrib["id"]
    else:
        msgid = "fwd"
        flags = flags | flag.isforward

    # получение user_info
    upic_contents = message_item.find(".div[@class='upic']*")
    from_contents = message_item.findall(".div[@class='from']*")

    userpic = upic_contents.attrib["src"]
    username = from_contents[0].text
    userlink = from_contents[1].attrib["href"]
    userid = from_contents[1].text

    global userpic_urls
    if userid not in userpic_urls and msgid != "fwd":
        userpic_urls[userid] = userpic

    user_info = UserInfo({"userid": userid,
                          "username": username,
                          "userlink": userlink,
                          "userpic": userpic})

    # получение date_info
    if msgid == "fwd":
        date_raw = from_contents[1].tail.strip()
    else:
        date_raw = from_contents[2].text
    date = datetime.datetime.strptime(date_raw, "%Y.%m.%d %X").strftime("%d.%m.%Y")
    time = datetime.datetime.strptime(date_raw, "%Y.%m.%d %X").strftime("%X")

    date_info = DateInfo({"date": date,
                          "time": time})

    # получение text info
    msg_body = message_item.find(".div[@class='msg_body']")

    if msg_body is not None:
        text = ""
        emoji = []

        msg_body_list = msg_body.xpath(".//node()")

        for i in msg_body_list:
            if type(i) == etree._Element and i.tag == "img":
                text += i.attrib["alt"]
                emoji.append(i.attrib["alt"])
            elif type(i) == etree._Element and i.tag == "br":
                text += "\n"
            elif type(i) == etree._Element and i.tag == "a":
                text += i.text
            elif type(i) == etree._ElementUnicodeResult:
                text += i
            else:
                print(f"\n\n\n\n!!! {type(i)} !!!\n\n\n\n")
                raise TypeError

        length_words = len(text.split())
        length_symbols_spaces = len(text)
        length_symbols_no_spaces = len("".join(text.split()))

        if len(emoji) > 0:
            flags = flags | flag.hasemoji
        else:
            emoji = None
            #flags = flags | flag.noemoji

        if not length_symbols_no_spaces == 0:
            flags = flags | flag.hastext
            text_info = TextInfo({"text": text,
                                  "length_words": length_words,
                                  "length_symbols_spaces": length_symbols_spaces,
                                  "length_symbols_no_spaces": length_symbols_no_spaces,
                                  "emoji": emoji})
        else:
            flags = flags | flag.notext
            text_info = None
    else:
        flags = flags | flag.notext
        text_info = None

    # получение attachments
    if message_item.find(".div[@class='attacments']") is not None:
        try:
            attachments = attachments_info(message_item)
            flags = flags | flag.hasattachment
            if len(attachments) == 1:
                if attachments[0].att_type == "att_sticker":
                    flags = flags | flag.sticker
                elif attachments[0].att_type == "att_graffiti":
                    flags = flags | flag.graffiti
                elif attachments[0].att_type == "att_voice":
                    flags = flags | flag.voice
        except:
            print(msgid, text_info)
            raise
        #print(msgid, attachments)
    else:
        attachments = None
        #flags = flags | flag.noattachment

    # получение forwards
    if message_item.find(".div[@class='fwd']") is not None:
        forward = message_item.find(".div[@class='fwd']")
        forwards = parse_forward(forward)
        flags = flags | flag.hasforward
    else:
        forwards = None
        #flags = flags | flag.noforward

    analysis_todo[msgid] = {"user_info": user_info, "date_info": date_info,
                       "text_info": text_info, "attachments": attachments,
                       "forwards": forwards}

    if msgid == "fwd":
        return Forward({"msgid": msgid, "user_info": user_info,
                        "date_info": date_info, "text_info": text_info,
                        "attachments": attachments, "forwards": forwards, "flags": flags})
    else:
        return Message({"msgid": msgid, "user_info": user_info,
                        "date_info": date_info, "text_info": text_info,
                        "attachments": attachments, "forwards": forwards, "flags": flags})


def attachments_info(message_item):
    attachments_list = []
    for att in message_item.xpath("div"):
        if "class" in att.attrib:
            if att.attrib["class"] in ("attacment", "attacment attb_link"):
                attachment = attachment_info(att)
                attachments_list.append(Attachment(attachment))
        elif "style" in att.attrib:
            attachments_list.append(Attachment({"att_type": "conf_userpic_update",
                                                "att_link": None,
                                                "att_link_text": "обновил(а) фотографию беседы:"}))
        else:
            print("Неизвестный тип сообщения")
            raise TypeError
    return attachments_list


def attachment_info(attachment):
    # если аттачмент преобразован (нет тэга <pre>)
    if attachment.find(".pre") is None:
        if attachment.attrib["class"] == "attacment":
            attachment_contents = attachment.xpath("*")
            att_type = attachment_type(attachment)
            att_link = attachment_contents[1].attrib["href"]
            att_link_text = attachment_contents[1].text
            graffiti_pattern = re.compile(r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\.png")
            voice_pattern = re.compile(r"(audio_msg|voice_message|audiocomment|(\d+_\d+))\.(opus|webm|3gp|ogg)")
            att_wall_attachments = []

            if att_type == "att_doc":
                if graffiti_pattern.match(att_link_text):
                    att_type = "att_graffiti"
                elif voice_pattern.match(att_link_text):
                    att_type = "att_voice"

            if att_type == "att_wall":
                if not attachment_contents[2].text == " ":
                    att_wall_text = attachment_contents[2].text
                else:
                    att_wall_text = "<Без текста>"

                for wall_attachment in attachment.findall("./div[@class='attacment']") or \
                                       attachment.findall(".div[@class='attacment attb_link']"):
                    att_wall_attachments.append(attachment_info(wall_attachment))

                return {"att_type": att_type,
                        "att_link": att_link,
                        "att_link_text": att_link_text,
                        "att_wall_text": att_wall_text,
                        "att_wall_attachments": att_wall_attachments}
            else:
                return {"att_type": att_type,
                        "att_link": att_link,
                        "att_link_text": att_link_text}
        # если плейлист
        elif attachment.attrib["class"] == "attacment attb_link":
            attachment_contents = attachment.xpath("*")
            att_type = "attb_link"
            att_link = attachment_contents[1].attrib["href"]
            att_link_text = attachment_contents[1].xpath("text()")[0]
            return {"att_type": att_type,
                    "att_link": att_link,
                    "att_link_text": att_link_text}

    # если аттачмент не преобразован
    else:
        data = json.loads(attachment.find(".pre").text, strict=False)  # json в словарь
        att_type = data["type"]

        if att_type == "market":
            owner = str(data["market"]["owner_id"] * -1)
            product_id = str(data["market"]["id"])
            att_link = "https://vk.com/market-%s?w=product-%s_%s" % (owner, owner, product_id)
            att_link_text = data["market"]["title"]
            return {"att_type": att_type,
                    "att_link": att_link,
                    "att_link_text": att_link_text}

        elif att_type == "poll":
            owner = str(data["poll"]["owner_id"] * -1)
            poll_id = str(data["poll"]["id"])
            att_link = "https://vk.com/poll%s_%s" % (owner, poll_id)
            att_link_text = data["poll"]["question"]
            return {"att_type": att_type,
                    "att_link": att_link,
                    "att_link_text": att_link_text}

        elif att_type == "photos_list":
            att_link = "https://vk.com/photo%s" % (data["photos_list"][0])
            att_link_text = "Фотоальбом"
            return {"att_type": att_type,
                    "att_link": att_link,
                    "att_link_text": att_link_text}

        else:
            att_link = "?"
            att_link_text = "Тип %s не поддерживается" % att_type
            return {"att_type": att_type,
                    "att_link": att_link,
                    "att_link_text": att_link_text}


def attachment_type(attachment):
    att_type = re.sub("[^\w]", " ",  attachment.xpath("*")[0].attrib["class"]).split()[1]
    return att_type


def parse_forward(head_tag):
    forwards = head_tag.xpath("*")
    forwards_list = []
    for forward in forwards:
        forward_info = parse_message(forward)
        forwards_list.append(forward_info)
    return forwards_list


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

