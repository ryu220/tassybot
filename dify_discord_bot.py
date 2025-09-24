import discord
from discord.ext import commands
import requests
import json
import os
from typing import Optional
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Discord Bot設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 設定値（環境変数から読み込み）
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DIFY_API_KEY = os.getenv('DIFY_API_KEY')
DIFY_API_BASE = os.getenv('DIFY_API_BASE', 'https://api.dify.ai/v1')

class DifyClient:
    """Dify APIクライアント"""
    
    def __init__(self, api_key: str, api_base: str):
        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def chat_completion(self, query: str, user_id: str, conversation_id: Optional[str] = None) -> dict:
        """Dify APIでチャット完了を実行"""
        url = f"{self.api_base}/chat-messages"
        
        data = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": user_id
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Dify API error: {e}")
            return {"error": str(e)}

# Difyクライアントの初期化
dify_client = DifyClient(DIFY_API_KEY, DIFY_API_BASE) if DIFY_API_KEY else None

@bot.event
async def on_ready():
    """ボット起動時の処理"""
    print(f'✅ {bot.user} has connected to Discord!')
    print(f'📊 Bot is in {len(bot.guilds)} guilds')
    print(f'🆔 Bot User ID: {bot.user.id}')
    print(f'🔧 Bot Prefix: !')
    print(f'📝 Message Content Intent: {intents.message_content}')
    
    # サーバー情報を表示
    for guild in bot.guilds:
        print(f'🏠 Server: {guild.name} (ID: {guild.id})')
        # ボットの権限を確認
        bot_member = guild.get_member(bot.user.id)
        if bot_member:
            permissions = bot_member.guild_permissions
            print(f'   📋 Read Messages: {permissions.read_messages}')
            print(f'   💬 Send Messages: {permissions.send_messages}')
            print(f'   📖 Read Message History: {permissions.read_message_history}')

@bot.event
async def on_message(message):
    """メッセージ受信時の処理"""
    # デバッグ用ログ
    try:
        channel_name = getattr(message.channel, 'name', 'DM')
        guild_name = message.guild.name if hasattr(message, 'guild') and message.guild else 'DM'
        print(f"📨 メッセージ受信: [{guild_name} / {channel_name}] {message.author} -> {message.content}")
        # チャンネル権限確認（ボット視点）
        bot_member = message.guild.get_member(bot.user.id) if message.guild else None
        if bot_member and hasattr(message, 'channel'):
            ch_perms = message.channel.permissions_for(bot_member)
            print(
                "🔐 ChannelPerms: "
                f"view={ch_perms.view_channel}, read_hist={ch_perms.read_message_history}, "
                f"send={ch_perms.send_messages}"
            )
    except Exception as e:
        print(f"⚠️ ログ出力中に例外: {e}")
    
    # ボット自身のメッセージは無視
    if message.author == bot.user:
        print("🤖 ボット自身のメッセージを無視")
        return
    
    # メンションされた場合またはDMの場合に応答（mentions配列も考慮）
    mentioned = (bot.user in getattr(message, "mentions", [])) or bot.user.mentioned_in(message)
    is_dm = isinstance(message.channel, discord.DMChannel)
    print(f"🔍 メンション確認: {mentioned}")
    print(f"🔍 DM確認: {is_dm}")
    
    if mentioned or is_dm:
        if not dify_client:
            await message.reply("❌ Dify APIが設定されていません。管理者に連絡してください。")
            return
        
        # メンション部分を除去してクエリを取得（<@id> と <@!id> の両方に対応）
        content = message.content
        content = content.replace(f'<@{bot.user.id}>', '')
        content = content.replace(f'<@!{bot.user.id}>', '')
        query = content.strip()
        if not query:
            await message.reply("質問を入力してください。")
            return
        
        # 「考え中...」メッセージを送信
        thinking_msg = await message.reply("🤔 考え中...")
        
        try:
            # Dify APIに問い合わせ
            user_id = str(message.author.id)
            response = dify_client.chat_completion(query, user_id)
            
            if "error" in response:
                await thinking_msg.edit(content=f"❌ エラーが発生しました: {response['error']}")
                return
            
            # 応答を取得
            answer = response.get('answer', '申し訳ありませんが、回答を生成できませんでした。')
            
            # Discord文字数制限（2000文字）を考慮して分割
            if len(answer) > 2000:
                chunks = [answer[i:i+2000] for i in range(0, len(answer), 2000)]
                await thinking_msg.edit(content=chunks[0])
                for chunk in chunks[1:]:
                    await message.channel.send(chunk)
            else:
                await thinking_msg.edit(content=answer)
                
        except Exception as e:
            await thinking_msg.edit(content=f"❌ エラーが発生しました: {str(e)}")
            print(f"Error processing message: {e}")
    
    # コマンドの処理を継続
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    """ボットの応答確認"""
    await ctx.send(f'🏓 Pong! レイテンシ: {round(bot.latency * 1000)}ms')

@bot.command(name='help_dify')
async def help_dify(ctx):
    """ヘルプメッセージ"""
    embed = discord.Embed(
        title="🤖 Dify Discord Bot",
        description="DifyのAIチャットボットとDiscordを連携したボットです",
        color=0x00ff00
    )
    embed.add_field(
        name="使い方",
        value="• ボットをメンション（@ボット名）して質問\n• DMで直接質問\n• `!ping` でボットの状態確認",
        inline=False
    )
    embed.add_field(
        name="注意事項",
        value="• 回答には数秒かかる場合があります\n• 長い回答は複数のメッセージに分割されます",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name='status')
async def status(ctx):
    """ボットの状態確認"""
    if not dify_client:
        status_text = "❌ Dify API未設定"
        color = 0xff0000
    else:
        status_text = "✅ Dify API接続済み"
        color = 0x00ff00
    
    embed = discord.Embed(
        title="ボット状態",
        description=status_text,
        color=color
    )
    embed.add_field(name="サーバー数", value=len(bot.guilds), inline=True)
    embed.add_field(name="レイテンシ", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKENが設定されていません")
        exit(1)
    
    if not DIFY_API_KEY:
        print("⚠️ DIFY_API_KEYが設定されていません")
    
    print("🚀 ボットを起動中...")
    bot.run(DISCORD_TOKEN)

