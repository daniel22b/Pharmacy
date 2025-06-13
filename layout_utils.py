import PySimpleGUI as sg

def white_push(horizontal=True):
    return sg.Push(background_color='white') if horizontal else sg.VPush(background_color='white')

def center_layout(layout):
    return [
        [white_push(horizontal=False)],
        [white_push(), sg.Column(layout, justification='center', element_justification='center',
                                 expand_x=True, background_color='white'), white_push()],
        [white_push(horizontal=False)]
    ]
input_style = {
    'font': ('Segoe UI', 14),
    'size': (40, 1),
    'background_color': '#F0F0F0',
    'text_color': 'black'
}