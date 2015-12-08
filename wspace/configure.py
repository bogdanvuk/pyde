from pyde.ddi import ddic
from wspace.desktop_gen import reload_buffers, get_layout

ddic.provide_on_demand('reload_buffers', reload_buffers, '')
ddic.provide('init_layout', get_layout())
