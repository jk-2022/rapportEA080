# import asyncio
import flet as ft
from myaction.myaction_village import init_db_village
from screens.acceuilscreen.acceuilview import AcceuilView
from myaction.myaction_entreprise import init_db_entreprise
from myaction.myaction_ouvrage import init_db_ouvrage
from myaction.myaction_projet import init_db
from myaction.myaction_pompage import init_db_pompage
from myaction.myaction_foration import init_db_foration
from myaction.myaction_suivi import init_db_suivi
from myaction.myaction_panne import init_db_panne
# import asyncio

from appstate import AppState
from screens.acceuilscreen.drawer import page_drawer
from screens.screens import *

from mystorage import *

async def main(page: ft.Page):
    page.title = "Gestion des ouvrages EA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width=460
    page.padding=0
    page.expand=True
    page.scroll = ft.ScrollMode.ADAPTIVE
    set_value("win_height",page.height)
    
    storage_paths = ft.StoragePaths()

    theme=get_value('theme')
    if theme=="ThemeMode.LIGHT":
        theme=ft.ThemeMode.LIGHT
    else:
        theme=ft.ThemeMode.DARK
    if theme:
        page.theme_mode = theme
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    theme = ft.Theme()
    theme.page_transitions.android = ft.PageTransitionsTheme.android

    state=AppState()

    def route_change():
        page.views.clear()
        page.views.append(AcceuilView(state=state))
        if page.route == "/projet" or page.route == "/projet/list-ouvrage":
            page.views.append(ProjectView(state=state))
        if page.route == "/projet/list-ouvrage"  or page.route == "/projet/list-ouvrage/recap-ouvrage":
            page.views.append(OuvrageView(state=state))
        if page.route == "/projet/list-ouvrage/recap-ouvrage":
            page.views.append(RecapOuvrageView(state=state))
        if page.route == "/stats":
            page.views.append(StatView(state=state))
        if page.route == "/list-entreprise":
            page.views.append(ListEntrepriseView(state=state))
        if page.route == "/list-village":
            page.views.append(VillageView(state=state))
        if page.route == "/archive":
            page.views.append(ArchiveView(state=state))
        if page.route == "/apropos":
            page.views.append(ApropoView(state=state))
        if page.route == "/settings":
            page.views.append(SettingView(state=state))

    # async def view_pop():
    #     page.views.pop()
    #     top_view = page.views.pop().route
    #     await page.push_route(top_view)
        
    async def view_pop(e):
        if e.view is not None:
            # print("View pop:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)
    
    async def get_absolute_path():
        platform = page.platform.name
        if platform=="WINDOWS" or platform=="LINUX":
            doc_dir = await storage_paths.get_application_documents_directory()
            return doc_dir
        else:
            doc_dir = "/storage/emulated/0/Documents/rapea"
            # doc_dir= await storage_paths.get_external_storage_directory()
            # try:
            #     doc_dir = "/storage/emulated/0/Documents/rapea"
            # except:
            #     doc_dir= await storage_paths.get_external_storage_directory()
            return doc_dir

    async def base_path():
        doc_dir = await get_absolute_path()
        if doc_dir:
            base_dir = os.path.join(doc_dir,'basedb')
            if not os.path.exists(base_dir):
                os.makedirs(base_dir, exist_ok=True)
            return base_dir 
        else:
            print('pas créer')

    async def archive_path():
        doc_dir = await get_absolute_path()
        base_dir = os.path.join(doc_dir,'archives')
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
        return base_dir 

    async def image_path():
        doc_dir = await get_absolute_path()
        base_dir = os.path.join(doc_dir,'images')
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
        return base_dir 
    
    basedb_path= await base_path()
    doc_path= await archive_path()
    images_path= await image_path()
    set_value("base_path",basedb_path)
    set_value("archive_path",doc_path)
    set_value("image_path",images_path)
    await init_db()
    await init_db_entreprise()
    await init_db_ouvrage()
    await init_db_pompage()
    await init_db_foration()
    await init_db_suivi()
    await init_db_panne()
    await init_db_village()

    page.on_route_change=route_change
    page.on_view_pop= view_pop
    route_change()

if __name__=="__main__":
    ft.run(main)
