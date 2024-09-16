import bpy


class Depth_node:
    """    Класс создания карты глубины
    """
    def __init__(self, depth_config: dict):
        self.config = depth_config
        print(depth_config)

    def _clear(self, compose_nodes, compose_links):
        for node in compose_nodes:
            compose_nodes.remove(node)
        for link in compose_links:
            compose_links.remove(link)

    def create_depth(self, ):
        view_layer = bpy.context.view_layer
        view_layer.use_pass_z = True
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        compose_nodes = tree.nodes
        compose_links = tree.links
        self._clear(compose_nodes, compose_links)
        return self._create_depth_pipeline(compose_nodes, compose_links)

    def _create_depth_pipeline(self, compose_nodes, compose_links):
        render_layers = compose_nodes.new(type='CompositorNodeRLayers')
        normalize = compose_nodes.new(type='CompositorNodeNormalize')
        invert = compose_nodes.new(type='CompositorNodeInvert')
        output_depth = compose_nodes.new(type='CompositorNodeOutputFile')
        output_depth.format.file_format = self.config['save_format']
        output_depth.format.color_mode = self.config['image_format']
        output_depth.format.color_depth = self.config['color_depth']
        output_depth.format.compression = self.config['compression']
        output_depth.base_path = self.config['base_path']

        compose_links.new(render_layers.outputs['Depth'], normalize.inputs['Value'])
        compose_links.new(normalize.outputs['Value'], invert.inputs['Color'])
        compose_links.new(invert.outputs['Color'], output_depth.inputs['Image'])
        return output_depth

