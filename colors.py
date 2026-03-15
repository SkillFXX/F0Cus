import hashlib
import colorsys
 
 
def app_color(name: str) -> str:
    """
    Text To Hex (By Sonnet 4.6)
    """
    digest = hashlib.sha256(name.lower().encode()).digest()
    hue = ((digest[0] << 8) | digest[1]) / 65535.0          
    sat = 0.55 + (digest[2] / 255.0) * 0.35         
    lum = 0.48 + (digest[3] / 255.0) * 0.20                 # [0.48, 0.68]
    r, g, b = colorsys.hls_to_rgb(hue, lum, sat)
 
    return "#{:02X}{:02X}{:02X}".format(
        int(r * 255),
        int(g * 255),
        int(b * 255),
    )
 