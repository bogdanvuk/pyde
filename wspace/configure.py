from pyde.ddi import ddic
from wspace.desktop_gen import reload_buffers, set_layout

ddic.provide_on_demand('reload_buffers', reload_buffers, '')
ddic.provide_on_demand('set_layout', set_layout, '')
