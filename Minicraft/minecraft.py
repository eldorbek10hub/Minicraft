from random import randint

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()


ground_color = color.rgb(0, 50, 0)



def create_block_material():
    from PIL import Image, ImageDraw

    
    size = 64
    image = Image.new('RGB', (size, size), color=(150, 150, 150))  
    draw = ImageDraw.Draw(image)

    
    border_thickness = 6
    draw.rectangle([0, 0, size - 1, size - 1], outline=(50, 50, 50), width=border_thickness)

    
    for _ in range(200):
        x, y = randint(border_thickness, size - border_thickness), randint(border_thickness, size - border_thickness)
        draw.point((x, y), fill=(randint(120, 180), randint(120, 180), randint(120, 180)))

    
    texture_path = 'block_texture.png'
    image.save(texture_path)
    return load_texture(texture_path)


block_texture = create_block_material()


blocks = {}
for x in range(50):  
    for z in range(50):  
        block = Entity(
            model='cube',
            texture=block_texture,
            position=(x, 0, z),
            scale=(1, 1, 1),
            collider='box',
            collision=True 
        )
        blocks[(x, 0, z)] = block


player = FirstPersonController(speed=6, mouse_sensitivity=Vec2(80, 80))   


sky = Entity(
    model='sphere',
    texture='sky_sunset',
    scale=150,
    double_sided=True
)


color_palette = [
    color.hex('#fffad3'),  # 1 oq
    color.hex('#414141'),  # 2 qora
    color.hex('#bf0101'),  # 3 qizil
    color.hex('#8fce00'),  # 4 yashil
    color.hex('#0b5394'),  # 5 ko`k
    color.hex('#e7e700'),  # 6 sariq
    color.hex('#f09c00'),  # 7 apilsin rang
    color.hex('#00d4d4'),  # 8 feruza rang
    color.hex('#ba00ba'),  # 9 siyoh rang
    color.hex('#808080')  # 10 kul rang
]
selected_color_index = 0  


hand1 = Entity(
    model='quad',
    texture='vecimg/hand12',
    scale=(0.5, 0.6),
    position=(0.5, -0.6),
    parent=camera.ui  
)

hand2 = Entity(
    model='quad',
    texture='vecimg/hand11',
    scale=(0.5, 0.6),
    position=(0.5, -0.6),
    parent=camera.ui,
    visible=False 
)


def animate_hand():
    hand1.visible = False
    hand2.visible = True
    hand2.animate_position((0.5, -0.5), duration=0.1, curve=curve.linear)
    invoke(
        lambda: (
            hand2.animate_position((0.5, -0.6), duration=0.1, curve=curve.linear),
            setattr(hand1, 'visible', True),
            setattr(hand2, 'visible', False)
        ),
        delay=0.1
    )


def input(key):
    global selected_color_index
    if key == 'left mouse down':
        hit_info = mouse.hovered_entity
        if hit_info:  
            position = hit_info.position
            destroy(hit_info)
            blocks.pop(tuple(position), None)
            animate_hand()  
    elif key == 'right mouse down':
        if mouse.hovered_entity:  
            hit_info = mouse.hovered_entity
            block_position = hit_info.position + mouse.normal
            if tuple(block_position) not in blocks:
                new_block = Entity(
                    model='cube',
                    texture=block_texture,  
                    color=color_palette[selected_color_index], 
                    position=block_position,
                    scale=(1, 1, 1),
                    collider='box',
                    collision=True  
                )
                blocks[tuple(block_position)] = new_block
                animate_hand() 
    elif key.isdigit():  
        index = int(key) - 1
        if 0 <= index < len(color_palette):
            selected_color_index = index
            print(f"Selected color index: {index + 1} Color:{color_palette[index]}")  


window.size = (1920, 1080)
window.fullscreen = True
window.exit_button.visible = False

app.run()
