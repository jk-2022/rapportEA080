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
    # print(page.window.height)
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
    def route_change(route):
        print(route)
        if route == "/projet":
            page.views.append(ProjectView(state=state))
        if route == "/list-ouvrage":
            page.views.append(OuvrageView(state=state))
        if route == "/create-ouvrage":
            page.views.append(CreateOuvrageView(state=state))
        if route == "/edit-ouvrage":
            page.views.append(EditOuvrageView(state=state))
        if route == "/recap-ouvrage":
            page.views.append(RecapOuvrageView(state=state))
        if route == "/filtrer-ouvrage":
            page.views.append(FiltreOuvrageView(state=state))
        if route == "/stats":
            page.views.append(StatView(state=state))
        if route == "/statgeneral":
            page.views.append(StatGeneralView(state=state))
        if route == "/statparprojet":
            page.views.append(StatParProjetView(state=state))
        if route == "/statcommune":
            page.views.append(StatCommuneView(state=state))
        if route == "/statcanton":
            page.views.append(StatCantonView(state=state))
        if route == "/list-entreprise":
            page.views.append(ListEntrepriseView(state=state))
        if route == "/list-village":
            page.views.append(VillageView(state=state))
        if route == "/intervaldate":
            page.views.append(IntervalDateView(state=state))
        if route == "/archive":
            page.views.append(ArchiveView(state=state))
        if route == "/apropos":
            page.views.append(ApropoView(state=state))
        if route == "/settings":
            page.views.append(SettingView(state=state))

    def view_pop():
        page.views.pop()
        top_view = page.views.pop()
        page.views.append(top_view)

    async def go_apropos(e):
        await handle_change()
        page.page.on_route_change("/apropos")
        
    async def handle_change():
        await page.close_drawer()
    
    async def go_archive(e):
        await handle_change()
        page.on_route_change('/archive')
    
    async def go_settings(e):
        await handle_change()
        page.on_route_change('/settings')
    
    async def go_stats(e):
        await handle_change()
        page.on_route_change('/stats')
    
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

    
    page.drawer=page_drawer(handle_change=handle_change,
                                    go_apropos=go_apropos,
                                    go_archive=go_archive,
                                    go_stats=go_stats,
                                    go_settings=go_settings)
    
    page.on_route_change=route_change
    page.on_view_pop= view_pop
    page.add(AcceuilView(page))

if __name__=="__main__":
    ft.run(main)
