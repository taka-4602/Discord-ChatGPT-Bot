import discord
import openai
import discord.app_commands

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

TOKEN = 'BOTのトークン'

openai.api_key = "ChatGPTのトークン"

@client.event
async def on_message(message: discord.Message):
    tables = str.maketrans(
        "！＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀>？＠ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～　",
        "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`>?@abcdefghijklmnopqrstuvwxyz{|}~ ",
    )
    
    message.content = message.content.translate(tables)
    if message.author.bot:
        return
    if client.user in message.mentions:
      try:  
        rep = await message.channel.fetch_message(message.reference.message_id)       
      except:
        return
      msg = await message.reply("GPTに連絡中...⏱", mention_author=False)
      async with message.channel.typing():
        try:
            flag=0
            if message.content[-3]+message.content[-2]+message.content[-1]==" -d":
              flag=1
              gprompt = message.content[:-3]
            else:              
              gprompt = message.content
            if ">> " in rep.content:
              gprompt=rep.content+"\n\n>> "+gprompt
              gprompt1 = gprompt.split(">> ")
              i=0
              messages=[]

              while i < len(gprompt1):
                if i%2==0:
                  messages.append({"role": "user", "content": f"{gprompt1[i]}"})
                  i=i+1
                else:
                  messages.append({"role": "assistant", "content": f"{gprompt1[i]}"})
                  i=i+1

              response = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=messages)
            else:  
              await msg.edit(content="そのリプライもとはGPTとの会話じゃないです.....")
              return
            gkun=(response.choices[0]["message"]["content"].strip())
            await msg.delete()
            try:
              if flag==1:
                await rep.delete()
              await message.reply(gprompt+"\n\n>> "+gkun, mention_author=False)
            except:
              i=2
              gkun1=""
              while i < len(gprompt1):                  
                gkun1=gkun1+f">> {gprompt1[i]}"
                i=i+1
              try:
                await message.reply(gkun1+"\n\n>> "+gkun, mention_author=False)
              except:
                i=6
                gkun1=""
                while i < len(gprompt1):                  
                  gkun1=gkun1+f">> {gprompt1[i]}"
                  i=i+1
                try:
                  await message.reply(gkun1+"\n\n>> "+gkun, mention_author=False)
                except:
                  try:
                    await message.reply("会話がながすぎです！")
                  except:
                    await message.channel.send("メッセージが消されてます！")
        except Exception as e: 
            await msg.delete()
            await message.reply(f"エラー\n{e}",mention_author=False)


    if message.content.startswith('gpt'):
      flag=0
      gprompt = message.content[3::]
      if not gprompt:
          await message.reply("質問してください", mention_author=False)
          return
      msg = await message.reply("GPTに連絡中...⏱", mention_author=False)
      async with message.channel.typing():
          try:
              try:
                rep = await message.channel.fetch_message(message.reference.message_id)
                if gprompt[-3]+gprompt[-2]+gprompt[-1]==" -d":
                  flag=1
                  gprompt = rep.content+"\n\n>> "+gprompt[:-3]
                else:              
                  gprompt=rep.content+"\n\n>> "+gprompt
              except:
                None
              if ">>" in gprompt:
                gprompt1 = gprompt.split(">> ")
                i=0
                messages=[]
                
                while i < len(gprompt1):
                  if i%2==0:
                    messages.append({"role": "user", "content": f"{gprompt1[i]}"})
                    i=i+1
                  else:
                    messages.append({"role": "assistant", "content": f"{gprompt1[i]}"})
                    i=i+1

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages)
              else:  
                response = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=[
                      {"role": "user", "content": f"{gprompt}"},
                  ],
                )
                             
              gkun=(response.choices[0]["message"]["content"].strip())
              await msg.delete()
              try:
                if flag==1:
                  await rep.delete()
                await message.reply(gprompt+"\n\n>> "+gkun, mention_author=False)
              except:
                i=2
                gkun1=""
                while i < len(gprompt1):                  
                  gkun1=gkun1+f">> {gprompt1[i]}"
                  i=i+1
                try:
                  await message.reply(gkun1+"\n\n>> "+gkun, mention_author=False)
                except:
                  i=6
                  gkun1=""
                  while i < len(gprompt1):                  
                    gkun1=gkun1+f">> {gprompt1[i]}"
                    i=i+1
                  try:
                    await message.reply(gkun1+"\n\n>> "+gkun, mention_author=False)
                  except:
                    try:
                      await message.reply("会話がながすぎです！")
                    except:
                      await message.channel.send("メッセージが消されてます！")
          except Exception as e: 
              await msg.delete()
              await message.reply(f"エラー\n{e}",mention_author=False)


@tree.context_menu(name="gpt")
async def gpt(interaction: discord.Interaction,message: discord.Message):
  await interaction.response.send_message("GPTに連絡中...⏱")
  msg = await interaction.original_response()
  try:
    gprompt = message.content
    if message.content[:3] == "gpt":
      gprompt = message.content[3::]
    if not gprompt:
      await msg.edit(content='質問してください')
      return

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "user", "content": f"{gprompt}"},
      ],
    )

    gkun=(response.choices[0]["message"]["content"].strip())
    await msg.edit(content=gprompt+"\n\n>> "+gkun)
  except Exception as e: 
    import traceback
    traceback.print_exc()
    await msg.delete()
    await msg.edit(content=f"エラー\n{e}")

@client.event
async def on_ready():
    await client.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='みんなのこと'))
    print(f'Thank you for running! {client.user}')
    await tree.sync()
client.run(TOKEN)