import json
import asyncio
import math
import numpy as np
from curl_cffi import requests
from rlottie_python import LottieAnimation
from sklearn.cluster import KMeans
from colorspacious import cspace_convert, deltaE
from colormath.color_objects import sRGBColor, HSVColor
from colormath.color_conversions import convert_color
from PIL import Image

SIGMA2 = (5.0**2) / (2 * math.log(2))

async def getLottieData(short: str, num: int) -> dict:
    try:
        URL = f"https://nft.fragment.com/gift/{short}-{num}.lottie.json"
        RESPONSE = requests.get(URL, timeout=10)
        return RESPONSE.json()
    except Exception as e:
        return {"error": str(e)}

async def getBgColor(data: dict) -> tuple[int, int, int]:
    if "error" in data:
        return (0, 0, 0)
    for layer in data.get("layers", []):
        if layer.get("nm") == "Background":
            for shape in layer.get("shapes", []):
                for it in shape.get("it", []):
                    if it.get("ty") == "gf":
                        k = it.get("g", {}).get("k", {}).get("k", [])
                        if len(k) >= 4:
                            return tuple(round(v * 255) for v in k[1:4])
    return (0, 0, 0)

async def removeBgPatCol(data: dict) -> dict:
    LAYERS = {"Background", "Pattern", "Color Icon"}
    data["layers"] = [layer for layer in data.get("layers", []) if layer.get("nm") not in LAYERS]
    return data

async def DOM(data: dict) -> tuple[int, int, int]:
    ANIMATION = LottieAnimation.from_data(json.dumps(data))
    IMAGE = ANIMATION.render_pillow_frame(frame_num=3).convert("RGBA")
    ARRAY = np.array(IMAGE)
    if ARRAY.shape[2] == 4:
        # :D
        mask = ARRAY[:, :, 3] > 0
        rgb_pixels = ARRAY[:, :, :3][mask]
        if rgb_pixels.size == 0:
            return (0, 0, 0)
        km = KMeans(n_clusters=1, random_state=42).fit(rgb_pixels)
        return tuple(km.cluster_centers_.astype(int)[0])
    return (0, 0, 0)

def similarityPercentage(delta: float, rgb_dist: float, bg_hsv, fg_hsv) -> float:
    cam_sim = 100 * np.exp(-delta**2 / (2 * 18.04))
    rgb_sim = min(100, 100 - (rgb_dist / 150 * 100))
    raw_hue_diff = abs(bg_hsv.hsv_h - fg_hsv.hsv_h)
    hue_diff = min(raw_hue_diff, 360 - raw_hue_diff)
    hue_sim = 100 - min(100, (hue_diff / 45 * 100))
    chroma_diff = abs(bg_hsv.hsv_s - fg_hsv.hsv_s)
    chroma_sim = 100 - min(100, (chroma_diff / 0.3 * 100))
    if bg_hsv.hsv_s < 0.2 and fg_hsv.hsv_s < 0.2:
        weights = [0.4, 0.3, 0.2, 0.1]
    else:
        weights = [0.5, 0.2, 0.2, 0.1]
    return round(
        weights[0] * cam_sim + 
        weights[1] * rgb_sim + 
        weights[2] * hue_sim + 
        weights[3] * chroma_sim, 
    2)

async def colorSimilarity(short: str, num: int) -> dict:
    data = await getLottieData(short, num)
    bg = await getBgColor(data)
    data = await removeBgPatCol(data)
    fg = await DOM(data)
    BG_CAM = cspace_convert(bg, "sRGB255", "CAM02-UCS")
    FG_CAM = cspace_convert(fg, "sRGB255", "CAM02-UCS")
    DE = float(deltaE(BG_CAM, FG_CAM))
    rgb_dist = np.linalg.norm(np.array(bg) - np.array(fg))

    bg_rgb = sRGBColor(*bg, is_upscaled=True)
    fg_rgb = sRGBColor(*fg, is_upscaled=True)
    bg_hsv = convert_color(bg_rgb, HSVColor)
    fg_hsv = convert_color(fg_rgb, HSVColor)

    return {
        "similarity": similarityPercentage(DE, rgb_dist, bg_hsv, fg_hsv),
        "deltaE": round(DE, 2),
        "rgbDistance": round(rgb_dist, 2),
        "hueDifference": round(abs(bg_hsv.hsv_h - fg_hsv.hsv_h), 2),
        "chromaDifference": round(abs(bg_hsv.hsv_s - fg_hsv.hsv_s), 2),
        "bgColor": bg,
        "giftColor": fg
    }

if __name__ == "__main__":
    result = asyncio.run(colorSimilarity("bdaycandle", 29702))
    print(result)
