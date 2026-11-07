import os
import discord
from keep_alive import keep_alive
from discord.ext import commands

# ตั้งค่า Intents (จำเป็นต้องเปิด ทั้งในโค้ดและใน Discord Developer Portal)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'ล็อกอินในชื่อ: {bot.user.name}')

# 🔨 1. คำสั่งแบน (ส่ง DM ก่อน แล้วค่อยแบน)
@bot.command()
@commands.has_permissions(ban_members=True)
async def b(ctx, member: discord.Member, *, reason=""):
    # ส่ง DM หาคนที่จะถูกแบนก่อน
    try:
        await member.send(f">>> คุณถูกแบนจาก **{ctx.guild.name}**                                                       \nเหตุผล: {reason}")
    except discord.Forbidden:
        await ctx.send(f"")

    # ทำการแบนหลังจากส่ง DM เสร็จ
    await member.ban(reason=reason)
    await ctx.send(f">>> แบน **@{member.name}** เรียบร้อยแล้ว!")

# จัดการข้อผิดพลาดเมื่อผู้ใช้คำสั่งไม่มีสิทธิ์ (Permission)
@b.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้ (จำเป็นต้องมีสิทธิ์ Ban Members)")
        
# คำสั่งปลดแบน (!unban ชื่อผู้ใช้ หรือ ID)

@bot.command()
@commands.has_permissions(ban_members=True)
# บังคับให้ผู้ใช้คำสั่งต้องมีสิทธิ์แบนสมาชิก
async def unban(ctx, *, user_input):
# ดึงรายชื่อผู้ใช้ที่ถูกแบนทั้งหมดในเซิร์ฟเวอร์
    banned_users = ctx.guild.bans()

    async for ban_entry in banned_users:
        user = ban_entry.user

# ตรวจสอบว่าตรงกับชื่อผู้ใช้, แท็ก หรือ ID ที่ใส่มาหรือไม่
        if (user_input == str(user) or 
            user_input == user.name or 
            user_input == str(user.id)):

            await ctx.guild.unban(user)
            await ctx.send(f'>>> ปลดแบน **@{user.name}** เรียบร้อยแล้ว!')
            return

    # หากไม่พบผู้ใช้ในรายชื่อคนโดนแบน
    await ctx.send(f'ไม่พบผู้ใช้ที่ชื่อหรือ ID "{user_input}" ในรายการแบน')

# จัดการข้อผิดพลาดเมื่อผู้ใช้คำสั่งไม่มีสิทธิ์ (Permission)
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้ (จำเป็นต้องมีสิทธิ์ Ban Members)")


keep_alive()

# ใส่ Token ของบอทคุณที่นี่

bot.run(os.getenv("TOKEN"))
