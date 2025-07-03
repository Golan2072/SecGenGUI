import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



def draw_hex(ax, center_x, center_y, size, facecolor='black', edgecolor='xkcd:neon green'):
    angle_offset = 0
    hexagon = [
        (
            center_x + size * np.cos(angle_offset + i * np.pi / 3),
            center_y + size * np.sin(angle_offset + i * np.pi / 3)
        )
        for i in range(6)
    ]
    hexagon.append(hexagon[0])
    xs, ys = zip(*hexagon)
    ax.plot(xs, ys, color=edgecolor)
    ax.fill(xs, ys, facecolor=facecolor, edgecolor=edgecolor)

@st.cache_data(ttl=24*36)
def generate_hex_grid(cols, rows, size, show_labels=True, _worlds=[]):
    height = np.sqrt(3) * size
    hex_width = 3 / 2 * size
    hex_height = height
    scale = size * 1.2
    fig_width = cols * 1.5 * scale
    fig_height = (rows + 1.5) * np.sqrt(3) * scale
    fig, ax = plt.subplots(
            figsize=(fig_width, fig_height))

    font_scale = size / 1.0
    for col in range(cols):
        for row in range(rows):
            flipped_row = rows - row - 1
            x = col * hex_width
            y = hex_height * (flipped_row + 0.5 * (col % 2))
            draw_hex(ax, x, y, size)
            world_label = None
            world_image = None
            for world in _worlds:
                if world['position'] == (col + 1, row + 1):
                    world_label = world.get('label', '')
                    world_image = world.get('image', None)
                    break
            if world_image is not None:
                img_size = size * 0.75
                extent = [
                    x - img_size / 2,
                    x + img_size / 2,
                    y - img_size / 2,
                    y + img_size / 2
                ]
                ax.imshow(world_image, extent=extent, zorder=10)
                # gg = Image.open("app/waterworld.png").convert("RGBA")
                # imbox = OffsetImage(gg, zoom=0.2)
                # ab = AnnotationBbox(imbox, (x+0.45, y+0.45), frameon=False)
                # ax.add_artist(ab)
            if world_label:
                ax.text(
                    x, y - size * 0.6,
                    world_label,
                    ha='center', va='bottom',
                    fontsize=16 * font_scale, color='xkcd:neon green', zorder=11
                )
            if show_labels:
                label = f"{col+1:02d}{row+1:02d}"
                ax.text(
                    x, y - size * 0.7,
                    label,
                    ha='center', va='center',
                    fontsize=14 * font_scale, color='xkcd:neon green', zorder=12
                )
        ax.set_aspect('equal')
        ax.axis('off')

    return fig

def location_parser(location_string):
    location = [0, 0]
    if location_string[2] == "1" and location_string[3] == "0":
        location[0] = int(location_string[1])
        location[1] = 10
    else:
        location[0] = int(location_string[1])
        location[1] = int(location_string[3])    
    return (location[0], location[1])

def world_type_parser(uwp):
    waterworld = Image.open("app/waterworld.png")
    nowaterworld = Image.open("app/nowaterworld.png")
    if uwp[3] == "A":
        return waterworld
    elif int(uwp[3]) > 0:
        return waterworld
    else:
        return nowaterworld       

@st.cache_data(ttl=24*36)
def render_map(map_data_list):
    worlds = []
    for i in range(len(map_data_list)):    
        worlds.append({"position": location_parser(map_data_list[i]["Hex"]), "label": map_data_list[i]["Name"], "image": world_type_parser(map_data_list[i]["UWP"])})
    figure = generate_hex_grid(8, 10, 1.0, True, worlds)
    figure.patch.set_facecolor('black')
    st.pyplot(figure)
