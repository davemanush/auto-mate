from app.model.script import Script, Step
from app.render.common_view import render_confirm_options_list

def render_step_details_screen(view_state):
    parent: Script = view_state.parent.active_data
    data: Step = view_state.wrapper
    print('', end='\n')
    print(f'>>> Script  - {parent.name}', end='\n')
    print(f'>> Step     - {data.name}', end='\n')
    render_step_data_list(view_state)

def render_confirmation_screen(view_state):
    name = ''
    object_type = ''
    parent = view_state.parent
    if isinstance(parent.active_data, Script):
        object_type = 'Script'
        o: Script = parent.parent.active_data
        name = o.getAttributeList("name").new_data
    if isinstance(parent.active_data, Step):
        object_type = 'Step'
        o: Step = parent.active_data
        name = o.get_attribute_by_name("name").new_data
    print('', end='\n')
    print(f'>>> Are you sude you want to delete {object_type} - {name}?')
    render_confirm_options_list(view_state)