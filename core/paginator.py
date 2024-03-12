import discord
from utils.config import Config
import embeds

er_em = Config("Error_Emoji").value
name = Config("Bot_Name").value
icon_url = Config("Icon_URL").value
error_c = Config("Error_Color").value
success_c = Config("Success_Color").value

class Paginator(discord.ui.View):
    """
    Base help paginator controller class. 

    Params
    -----------
    ##### requester_id:
                The user ID of the original requester of the help session obtained from either ctx.author.id or interaction.user.id
    ##### initial_page:
                The page to start the help session with.
    ##### max_pages:
                The max number of embed allocated in embeds module for admin or user help session
    ##### admin:
            bool definition of whether the user is a admin or regular user

    Returns
    -----------
    None

    Raises
    -----------
    ##### ValueError:
                Any of the values supplied to not of the required heritage
    
    """
    def __init__(self, requester_id: int, initial_page: int, max_pages: int, admin: bool):
        super().__init__(timeout=None)
        self.original_requester_id = requester_id
        self.page_number = initial_page
        self.max_pages = max_pages
        self.role = admin
        if self.original_requester_id is not int or self.page_number is not int or self.max_pages is not int or self.role is not bool:
            raise ValueError("Invalid parameters passed.")
        # non constant
        self.cancelled = False

    @discord.ui.button(label='x2 Back', custom_id="HELPTWOBACKBUTTON", style=discord.ButtonStyle.green, emoji="<:r_x2_back:1197992839964012574>")
    async def two_back_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.original_requester_id == interaction.user.id:
            self.cancelled = False
            if self.page_number > 2:
                self.page_number -= 2
                await self.update_embed(interaction)
            else:
                embed = discord.Embed(
                    description=f'{er_em} **You are currently on or before the second page. You cannot go back two pages.**',
                    color=error_c
                )
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
                embed.set_footer(text=name, icon_url=icon_url)
                embed.timestamp = discord.utils.utcnow()
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=f'{er_em} **This is not for you.**',
                color=error_c
            )
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
            embed.set_footer(text=name, icon_url=icon_url)
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label='Back', custom_id="HELPBACKBUTTON", style=discord.ButtonStyle.blurple, emoji="<:r_back:1197954523113726063>")
    async def back_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.original_requester_id == interaction.user.id:
            self.cancelled = False
            if self.page_number > 1:
                self.page_number -= 1
                await self.update_embed(interaction)
            else:
                embed=discord.Embed(
                    description=f'{er_em} **You are currently on the first page. You cannot go back.**',
                    color=error_c
                )
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
                embed.set_footer(text=name, icon_url=icon_url)
                embed.timestamp = discord.utils.utcnow()
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=f'{er_em} **This is not for you.**',
                color=error_c
            )
            embed.set_footer(text=name, icon_url=icon_url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label='Next', custom_id="HELPNEXTBUTTON", style=discord.ButtonStyle.blurple, emoji="<:r_next:1197954517732429834>")
    async def next_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.original_requester_id == interaction.user.id:
            self.cancelled = False
            if self.page_number < self.max_pages:
                self.page_number += 1
                await self.update_embed(interaction)
            else:
                embed=discord.Embed(
                    description=f'{er_em} **You are currently on the last page. You cannot go ahead.**',
                    color=error_c
                )
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
                embed.set_footer(text=name, icon_url=icon_url)
                embed.timestamp = discord.utils.utcnow()
            
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=f'{er_em} **This is not for you.**',
                color=error_c
            )
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
            embed.set_footer(text=name, icon_url=icon_url)
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label='x2 Next', custom_id="HELPTWONEXTBUTTON", style=discord.ButtonStyle.green, emoji="<:r_x2_next:1197992770841878589>")
    async def two_next_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.original_requester_id == interaction.user.id:
            self.cancelled = False
            if self.page_number < self.max_pages - 1:
                self.page_number += 2
                await self.update_embed(interaction)
            else:
                embed = discord.Embed(
                    description=f'{er_em} **You are currently on or before the second last page. You cannot go ahead two pages.**',
                    color=error_c
                )
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
                embed.set_footer(text=name, icon_url=icon_url)
                embed.timestamp = discord.utils.utcnow()
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=f'{er_em} **This is not for you.**',
                color=error_c
            )
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
            embed.set_footer(text=name, icon_url=icon_url)
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label='Cancel', custom_id="HELPCUTBUTTON", style=discord.ButtonStyle.danger, emoji="<:noEntry:1172627159244873790>")
    async def cancel_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        if self.original_requester_id == interaction.user.id:
            self.cancelled = True
          
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
                    
            await self.update_embed(interaction)
            self.stop()
        else:
            embed = discord.Embed(
                description=f'{er_em} **This is not for you.**',
                color=error_c
            )
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url or None, url=f'https://discord.com/users/{interaction.user.id}')
            embed.set_footer(text=name, icon_url=icon_url)
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    async def update_embed(self, interaction: discord.Interaction):
        if self.cancelled: 
            embedc=discord.Embed(
                description='<:locked:1172627945119027230> **This help session has been ended.**',
                color=success_c
            )
            await interaction.response.edit_message(embed=embedc, view=self)
        else:
            embed_name = f"EMBED{self.page_number}"
            if hasattr(embeds, embed_name):
                embed = getattr(embeds, embed_name)
                # TODO: The footer doesn't gets set on the initial request.
                embed.set_footer(text=f"{name} | Page {self.page_number}/{self.max_pages}", icon_url=icon_url)
                await interaction.response.edit_message(embed=embed, view=self)
    


# any problem?