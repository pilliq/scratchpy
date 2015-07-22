from scratch.scratch2 import Extension, Block, BlockType, Menu

# existing extension file
ext = Extension.load('./myAWESOMEextension.s2e')
ext = Extension.loads('{myextension string}')

beep = ext.blocks.get('beep')
block_format = beep.block_format
block_type = beep.block_type
name = beep.name
params = beep.default_params
beep.handler = func # property
handler = beep.handler

coord = ext.menus.get('coordinate')
opts = coord.options
coord.options.append('theta')



# new extension file
ext = Extension('My extension', 23000, blocks=blocks, menus=menus)

block = Block('name', BlockType.command, 'format', default_params=['parameters'], handler=func)
ext.blocks.add(block)
json = str(ext.blocks)

foods = Menu('food', options=['pizza'])
foods.options.append('churros')
ext.menus.add(foods)
json = str(ext.menus)

ext.save('./path/to/my/extension')
json = str(ext)

ext.run() # ???
# or should it run automatically when handlers are added? (with the option of not running)
