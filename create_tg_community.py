import asyncio
import json
import python_socks
from pathlib import Path
from telethon import TelegramClient
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    InviteToChannelRequest,
    EditAdminRequest,
    SetDiscussionGroupRequest
)
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import ChatAdminRights

API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION_PATH = "/Users/ricksabchez/telegram_userbot/rick_session"
PROXY = (python_socks.ProxyType.SOCKS5, "127.0.0.1", 10808)

CHANNEL_TITLE = "جامعه یوتیوبرهای ایران | Iranian YouTubers"
CHANNEL_ABOUT = "پایگاه و کانال مستقل اطلاع‌رسانی، تحلیل داده و جامعه یوتیوبرهای ایرانی. پرتال وب: m4tinbeigi-official.github.io/iranian-youtubers"

GROUP_TITLE = "انجمن یوتیوبرهای ایران | Iranian YouTubers Group"
GROUP_ABOUT = "سوپرگروه تخصصی تبادل نظر، همکاری و شبکه‌سازی تولیدکنندگان محتوای یوتیوب فارسی. ورود با تایید ادمین."

async def setup():
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH, proxy=PROXY)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("Telegram client not authorized!")
        return

    print("Connected to Telegram successfully.")

    # 1. Create Broadcast Channel
    print("Creating Broadcast Channel...")
    c_res = await client(CreateChannelRequest(
        title=CHANNEL_TITLE,
        about=CHANNEL_ABOUT,
        megagroup=False
    ))
    channel = c_res.chats[0]
    print(f"Channel created: {channel.title} (ID: {channel.id})")

    # Export Channel Invite Link
    c_invite = await client(ExportChatInviteRequest(
        peer=channel,
        title="Official Channel Link"
    ))
    channel_link = c_invite.link
    print(f"Channel link: {channel_link}")

    # 2. Create Supergroup (megagroup=True)
    print("Creating Community Supergroup...")
    g_res = await client(CreateChannelRequest(
        title=GROUP_TITLE,
        about=GROUP_ABOUT,
        megagroup=True
    ))
    group = g_res.chats[0]
    print(f"Group created: {group.title} (ID: {group.id})")

    # Export Group Invite Link with request_needed=True (Admin Approval)
    g_invite = await client(ExportChatInviteRequest(
        peer=group,
        request_needed=True,
        title="Official Group Link (Admin Approval)"
    ))
    group_link = g_invite.link
    print(f"Group link (Approval Required): {group_link}")

    # 3. Link Group as Discussion Group to Channel
    try:
        await client(SetDiscussionGroupRequest(
            broadcast=channel,
            group=group
        ))
        print("Channel and Group linked successfully!")
    except Exception as e:
        print(f"Failed to link discussion group: {e}")

    # 4. Invite Ardalan Ketabchi (@Ketabchi0) and Promote to Full Admin
    try:
        ardalan = await client.get_entity("Ketabchi0")
        print("Found Ardalan entity.")
        
        # Add to Group
        await client(InviteToChannelRequest(channel=group, users=[ardalan]))
        print("Invited Ardalan to Group.")
        
        # Promote in Group
        admin_rights = ChatAdminRights(
            change_info=True,
            post_messages=True,
            edit_messages=True,
            delete_messages=True,
            ban_users=True,
            invite_users=True,
            pin_messages=True,
            add_admins=True,
            manage_call=True,
            other=True,
            manage_topics=True
        )
        await client(EditAdminRequest(
            channel=group,
            user_id=ardalan,
            admin_rights=admin_rights,
            rank="مدیر ارشد انجمن"
        ))
        print("Ardalan promoted to Full Admin in Group.")

        # Add and Promote in Channel
        try:
            await client(InviteToChannelRequest(channel=channel, users=[ardalan]))
            await client(EditAdminRequest(
                channel=channel,
                user_id=ardalan,
                admin_rights=admin_rights,
                rank="مدیر ارشد"
            ))
            print("Ardalan promoted to Full Admin in Channel.")
        except Exception as ec:
            print(f"Channel admin notice: {ec}")

    except Exception as e:
        print(f"Admin delegation note: {e}")

    # Save output metadata
    out_data = {
        "channel_id": channel.id,
        "channel_title": channel.title,
        "channel_link": channel_link,
        "group_id": group.id,
        "group_title": group.title,
        "group_link": group_link
    }
    
    out_path = Path("/Users/ricksabchez/workspace/projects/iranian-youtubers/data/telegram_community.json")
    out_path.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved credentials to {out_path}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(setup())
