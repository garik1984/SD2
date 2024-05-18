from IPython.display import display, HTML, clear_output
from nenen88 import download, say, tempe
from ipywidgets import widgets, Layout
from pathlib import Path
import os

path = Path(__file__).parent.parent
css = Path(__file__).parent / "cn-1_5.css"

with open(css, "r") as oppai:
    susu = oppai.read()
display(HTML(f"<style>{susu}</style>"))
    
url_list = {
    "Openpose": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors openpose.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_openpose_fp16.yaml openpose.yaml"],
    "Canny": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny_fp16.safetensors canny.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_canny_fp16.yaml canny.yaml"],
    "Depth": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors depth.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1p_sd15_depth_fp16.yaml depth.yaml"],
    "Lineart": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart_fp16.safetensors lineart.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_lineart_fp16.yaml lineart.yaml"],
    "Lineart Anime": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors lineart_anime.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15s2_lineart_anime_fp16.yaml lineart_anime.yaml"],
    "ip2p": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p_fp16.safetensors ip2p.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_ip2p_fp16.yaml ip2p.yaml"],
    "Shuffle": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle_fp16.safetensors shuffle.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_shuffle_fp16.yaml shuffle.yaml"],
    "Inpaint": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors inpaint.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_inpaint_fp16.yaml inpaint.yaml"],
    "MLSD": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors mlsd.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_mlsd_fp16.yaml mlsd.yaml"],
    "Normalbae": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae_fp16.safetensors normalbae.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_normalbae_fp16.yaml normalbae.yaml"],
    "Scribble": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble_fp16.safetensors scribble.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_scribble_fp16.yaml scribble.yaml"],
    "Seg": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg_fp16.safetensors seg.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_seg_fp16.yaml seg.yaml"],
    "Softedge": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge_fp16.safetensors softedge.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_softedge_fp16.yaml softedge.yaml"],
    "Tile": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors tile.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1e_sd15_tile_fp16.yaml tile.yaml"],
    
    "IP Adapter 1.5": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15.safetensors ip-adapter_sd15.safetensors"],
    "IP Adapter 1.5 Light": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_light.safetensors ip-adapter_sd15_light.safetensors"],
    "IP Adapter 1.5 VIT-G": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter_sd15_vit-G.safetensors ip-adapter_sd15_vit-G.safetensors"],
    "IP Adapter Plus 1.5": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus_sd15.safetensors ip-adapter-plus_sd15.safetensors"],
    "IP Adapter Plus Face 1.5": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-plus-face_sd15.safetensors ip-adapter-plus-face_sd15.safetensors"],
    "IP Adapter Full Face 1.5": [
        "https://huggingface.co/h94/IP-Adapter/resolve/main/models/ip-adapter-full-face_sd15.safetensors ip-adapter-full-face_sd15.safetensors"],

    "IP Adapter FaceID 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid_sd15_lora.safetensors {path}/models/loras \
        ip-adapter-faceid_sd15_lora.safetensors"],
    "IP Adapter FaceID Plus 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plus_sd15.bin ip-adapter-faceid-plus_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plus_sd15_lora.safetensors {path}/models/loras \
        ip-adapter-faceid-plus_sd15_lora.safetensors"],
    "IP Adapter FaceID PlusV2 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15.bin ip-adapter-faceid-plusv2_sd15.bin",
        f"https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sd15_lora.safetensors {path}/models/loras \
        ip-adapter-faceid-plusv2_sd15_lora.safetensors"],
    "IP Adapter FaceID Portrait 1.5": [
        "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-portrait_sd15.bin"]
}

list_half = len(url_list) // 2
half_list_1 = dict(list(url_list.items())[:list_half])
half_list_2 = dict(list(url_list.items())[list_half:])

cb1 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'})
     for name in half_list_1])
cb1.add_class("checkbox-group1")

cb2 = widgets.VBox(
    [widgets.Checkbox(value=False, description=name, style={'description_width': '0px'})
     for name in half_list_2])
cb2.add_class("checkbox-group2")

db = widgets.Button(description="Download")
db.add_class("download-button")
dbo = widgets.Output()
cbc = widgets.HBox([cb1, cb2], layout=widgets.Layout(align_items='flex-start'))

gariz3 = """<div class="gradient-cn2">asd</div>"""
garis3 = widgets.Output()

def sa_cb(b):
    for checkbox in cb1.children + cb2.children:
        checkbox.value = True

def usa_cb(b):
    for checkbox in cb1.children + cb2.children:
        checkbox.value = False
        
sab = widgets.Button(description="Select All")
sab.add_class("select-all-button")
sab.on_click(sa_cb)

usab = widgets.Button(description="Unselect All")
usab.add_class("unselect-all-button")
usab.on_click(usa_cb)

bs = widgets.Button(description="")
bs.add_class("border-style")

bl = widgets.HBox([sab, usab, db, bs])
boks2 = widgets.VBox([bl, cbc], layout=Layout(
    display='flex',
    flex_flow='column',
    width='630px',
    height='455px',
    align_items='center',
    padding='10px'))
boks2.add_class("boks2")
        
def d_b_click(b):
    surl = []
    for checkbox, key in zip(cb1.children + cb2.children, list(url_list.keys())):
        if checkbox.value:
            surl.extend(url_list[key])
            
    widgets.Widget.close(boks2)
    dbo.clear_output()
    
    with garis3:
        display(HTML(gariz3))
        
    with dbo:
        say("【{red} Downloading{cyan} Controlnet{magenta} Models{yellow} 】{red}")
        os.chdir(f"{path}/models/controlnet")
        
        for url in surl:
            download(url)
            
        with garis3:
            garis3.clear_output()
            
        say("【{red} Done{d} 】{red}")
            
tempe()
display(boks2, dbo, garis3)
db.on_click(d_b_click)