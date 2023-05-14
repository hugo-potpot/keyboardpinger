import threading
from datetime import datetime

from discord import Intents, option
from discord.ext import commands

from src.Database import Database


class DiscordBot(commands.Bot):
    def __init__(self, database: Database, command_prefix, intents: Intents):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)
        self.database = database
        self.remove_command("help")
        self.add_commands()
        self.msg_loop = []

    async def on_ready(self):
        self.checkTime()
        print("Bot is ready")

    def get_all_size(self):
        return ["36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46"]

    def checkTime(self):
        threading.Timer(1.0, self.checkTime).start()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # if (current_time == "00:00:00"):
        #     self.get_all_channels()

    def add_commands(self):
        @self.event
        async def on_member_join(member):
            self.database.add_user(member.id, member.name)
            print(f"New user: {member.name} ({member.id})")

        @self.event
        async def on_member_remove(member):
            self.database.remove_user(member.id)
            print(f"User left: {member.name} ({member.id})")

        @self.event
        async def on_message(message):
            line = [line for line in message.content.split("\n") if line != ""]
            status = ""
            if line[0].lower.contains("wtb"):
                status = "WTB"
            elif line[0].lower.contains("wts"):
                status = "WTS"
            # for l in line:
            #     if len(self.database.get_message_content(line) > 0):
            #         for



        @self.slash_command(name="add_keyword", description="Add a keyword to a category")
        @option(name="categorie", description="The category where you want to add the keyword", required=True)
        @option(name="name_sneakers", description="The name of sneakers", required=True)
        @option(name="size", description="The size of sneakers", required=True, choices=self.get_all_size())
        @option(name="sku", description="The sku of sneakers", required=False)
        async def add_keyword(ctx, categorie: str, name_sneakers: str, size: str, sku: str = None):
            if ctx.guild is None:
                if self.database.add_favoris(name_sneakers, size, sku, categorie, ctx.author.id, ):
                    await ctx.send("Keyword added")
                else:
                    await ctx.send("Keyword already exist")

        @self.slash_command(name="remove_keyword", description="Remove a keyword to a category")
        @option(name="categorie", description="The category where you want to remove the keyword", required=True)
        @option(name="id", description="The id of the keyword", required=True)
        async def remove_keyword(ctx, categorie: str, id: int):
            if ctx.guild is None:
                if self.database.remove_favoris(ctx.author.id, id, categorie):
                    await ctx.send("Keyword removed")
                else:
                    await ctx.send("Keyword not found")

        # @self.slash_command(name="list_keyword", description="List all keyword")
        # @option(name="categorie", description="The category where you want to list the keyword", required=True)
        # async def list_keyword(ctx, categorie: str):
        #     if ctx.guild is None:
        #         if self.database.list_favoris(ctx.author.id, categorie):
        #             await ctx.send("Keyword listed")
        #         else:
        #             await ctx.send("Keyword not found")

