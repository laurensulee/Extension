import omni.ext
import omni.ui as ui
import omni.kit.commands
from pxr import Usd, Gf, Sdf
from random import randrange 

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        #plane does not exist
        self.planehasbeencreated = False
        #number of cubes is 0
        self.cubecount= 0
        self.cheesecount = 0
        print("[lauren.extension] MyExtension startup")

    #puts in an environment texture
        omni.kit.commands.execute('CreateHdriSkyCommand',
            sky_url='http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Skies/Clear/noon_grass_4k.hdr',
            sky_path='/Environment/sky')

        #this was supposed to make a physics scene but kept raising an error for some reason 
        #omni.kit.commands.execute('AddPhysicsSceneCommand',
        #    stage=Usd.Stage.Open(rootLayer=Sdf.Find('anon:000002C9489E6510:World2.usd'), sessionLayer=Sdf.Find('anon:000002C9489E66F0:World2-session.usda')),
        #   path='/World/PhysicsScene')

        #to make the window
        self._window = ui.Window("picnic day!!!!!!!", width=300, height=300)
        with self._window.frame:           
            with ui.VStack():
                ui.Label("remember to hit play :)", alignment = ui.Alignment.CENTER, style ={"font_size": 30.0})
                
                #click for plane
                def on_click():
                    
                    #if a plane does not already exist
                    if self.planehasbeencreated == False:
                        print("plane has been spawned!")

                        #creating the plane
                        omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
                            prim_type='Plane')
                        
                        #making it a static collider
                        omni.kit.commands.execute('SetStaticCollider',
                            path=Sdf.Path('/World/Plane'),
                            approximationShape='none')
                        
                        #change the scale
                        omni.kit.commands.execute('ChangeProperty',
                            prop_path=Sdf.Path('/World/Plane.xformOp:scale'),
                            value=Gf.Vec3d(40.0, 40.0, 40.0),
                            prev=Gf.Vec3d(1.0, 1.0, 1.0))
                        
                        #creates a texture for the plane
                        omni.kit.commands.execute('CreateMdlMaterialPrimCommand',
                            mtl_url='http://omniverse-content-production.s3-us-west-2.amazonaws.com/Materials/Base/Carpet/Carpet_Pattern_Leaf_Squares_Tan.mdl',
                            mtl_name='Carpet_Pattern_Leaf_Squares_Tan',
                            mtl_path='/World/Looks/Carpet_Pattern_Leaf_Squares_Tan_04')
                        #binds the texture to the plane
                        omni.kit.commands.execute('BindMaterialCommand',
                            prim_path='/World/Plane',
                            material_path='/World/Looks/Carpet_Pattern_Leaf_Squares_Tan_04',
                            strength='strongerThanDescendants')

                        #once a plane has been created, set the variable to True
                        self.planehasbeencreated = True
                    #if a plane already exists
                    else:
                        print("you already have a plane :|")
                
                #button for the plane
                ui.Button("click to lay down your blanket!!", clicked_fn=lambda: on_click())
                
                with ui.HStack():
                    #click for apples
                    def on_click1():
                        print('spawned an apple!')

                        #creates a cube
                        omni.kit.commands.execute('CreateReferenceCommand',
                        asset_path="omniverse://localhost/Users/labuser/Apple.usdz",
                        path_to = '/World/Apple',
                        usd_context = omni.usd.get_context())

                        #has a variable for what the cube path name should be if it is the first cube or a cube <= 9
                        cube_path = 'Apple' if self.cubecount == 0 else f'Apple_0{self.cubecount}'

                        #if the number is greater than 9, begin to just use the number rather than the format '0_'
                        if self.cubecount > 9:
                            cube_path =f'Apple_{self.cubecount}'

                        #set the created cube as a rigid body
                        omni.kit.commands.execute('SetRigidBody',
                            path=Sdf.Path(f'/World/{cube_path}'),
                            approximationShape='convexHull',
                            kinematic=False)

                        #gives it angular velocity or spin
                        omni.kit.commands.execute('ChangeProperty',
                            prop_path=Sdf.Path(f'/World/{cube_path}.physics:angularVelocity'),
                            value=Gf.Vec3f(randrange(-360,360), 0.0, 0.0),
                            prev=Gf.Vec3f(0.0, 0.0, 0.0))
                        
                        #spawns a cube in a random spot
                        omni.kit.commands.execute('TransformPrimSRT',
                            path=Sdf.Path(f'/World/{cube_path}'),
                            new_translation=Gf.Vec3d(randrange(-1000,1000), 650.0, randrange(-1000,1000)),
                            #new_rotation_euler=Gf.Vec3d(0.0, 0.0, 0.0),
                            #new_rotation_order=Gf.Vec3i(0, 1, 2),
                            #new_scale=Gf.Vec3d(1.0, 1.0, 1.0),
                            old_translation=Gf.Vec3d(0.0, 0.0, 0.0),
                            #old_rotation_euler=Gf.Vec3d(0.0, 0.0, 0.0),
                            #old_rotation_order=Gf.Vec3i(0, 1, 2),
                            #old_scale=Gf.Vec3d(1.0, 1.0, 1.0)
                                )   
                        
                        #iterate the cube count variable after a cube has been spawned 
                        self.cubecount +=1
                    #button for cubes 
                    ui.Button("click for an apple!!", clicked_fn=lambda: on_click1())

                    def on_click15():
                        print('spawned a cheese!')

                        #creates a cube
                        omni.kit.commands.execute('CreateReferenceCommand',
                        asset_path="omniverse://localhost/Users/labuser/Cheese_Wedge.usdz",
                        path_to = '/World/Cheese_Wedge',
                        usd_context = omni.usd.get_context())

                        #has a variable for what the cube path name should be if it is the first cube or a cube <= 9
                        cheese_path = 'Cheese_Wedge' if self.cheesecount == 0 else f'Cheese_Wedge_0{self.cheesecount}'

                        #if the number is greater than 9, begin to just use the number rather than the format '0_'
                        if self.cheesecount > 9:
                            cheese_path =f'Cheese_Wedge_{self.cheesecount}'

                        #set the created cube as a rigid body
                        omni.kit.commands.execute('SetRigidBody',
                            path=Sdf.Path(f'/World/{cheese_path}'),
                            approximationShape='convexHull',
                            kinematic=False)

                        #gives it angular velocity or spin
                        omni.kit.commands.execute('ChangeProperty',
                            prop_path=Sdf.Path(f'/World/{cheese_path}.physics:angularVelocity'),
                            value=Gf.Vec3f(randrange(-360,360), 0.0, 0.0),
                            prev=Gf.Vec3f(0.0, 0.0, 0.0))
                        
                        #spawns a cube in a random spot
                        omni.kit.commands.execute('TransformPrimSRT',
                            path=Sdf.Path(f'/World/{cheese_path}'),
                            new_translation=Gf.Vec3d(randrange(-1000,1000), 650.0, randrange(-1000,1000)),
                            #new_rotation_euler=Gf.Vec3d(0.0, 0.0, 0.0),
                            #new_rotation_order=Gf.Vec3i(0, 1, 2),
                            new_scale=Gf.Vec3d(25.0, 25.0, 25.0),
                            old_translation=Gf.Vec3d(0.0, 0.0, 0.0),
                            #old_rotation_euler=Gf.Vec3d(0.0, 0.0, 0.0),
                            #old_rotation_order=Gf.Vec3i(0, 1, 2),
                            old_scale=Gf.Vec3d(1.0, 1.0, 1.0)
                                )   
                        
                        #iterate the cube count variable after a cube has been spawned 
                        self.cheesecount +=1
                    #button for cubes 
                    ui.Button("click for a cheese!!", clicked_fn=lambda: on_click15())
                
                #'refresh' the extension after the stage has been cleared 
                def on_click2():
                    print('resetting...')
                    #no more plane
                    self.planehasbeencreated = False
                    #set the cube count to 0
                    self.cubecount= 0
                    self.cheesecount = 0
                ui.Button('press to reset after you\'ve deleted everything :P', clicked_fn=lambda: on_click2())

    def on_shutdown(self):
        print("[lauren.extension] MyExtension shutdown")
