import flet as ft
import os


storage_paths = ft.StoragePaths()


async def base_path():
    doc_dir = await storage_paths.get_application_documents_directory
    base_dir = os.path.join(doc_dir,'base_db')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
    return base_dir  

async def archive_path():
    doc_dir = await storage_paths.get_application_documents_directory
    base_dir = os.path.join(doc_dir,'archives')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
    return base_dir 

async def image_path():
    doc_dir = await storage_paths.get_application_documents_directory
    base_dir = os.path.join(doc_dir,'images')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
    return base_dir       

