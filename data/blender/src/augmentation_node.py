import random
import math


class Material:
    """    Класс создания материала.
    """
    def __init__(self, config: dict):
        self.config = config
        self.checker = self._random_choice(probability=0.2)

    def _random_choice(self, probability=0.2):
        return random.choices([1, 0], weights=[probability, 1 - probability])[0]

    def _clear(self, nodes, links):
        for link in list(links):
            links.remove(link)

        for node in list(nodes):
            nodes.remove(node)

    def create_material(self, object):
        material = object.data.materials[0]
        material.use_nodes = True
        material_nodes = material.node_tree.nodes
        material_links = material.node_tree.links
        self._clear(material_nodes, material_links)

        bsdf = material_nodes.new(type='ShaderNodeBsdfPrincipled')
        material_output_node = material_nodes.new(type='ShaderNodeOutputMaterial')

        random_r = random.uniform(0.0, 1.0)
        random_g = random.uniform(0.0, 1.0)
        random_b = random.uniform(0.0, 1.0)
        random_alpha = random.uniform(0.7, 1.0)
        bsdf.inputs['Base Color'].default_value = (random_r, random_g, random_b, random_alpha)
        bsdf.inputs['Metallic'].default_value = random.uniform(0.5, 1.0)
        bsdf.inputs['Roughness'].default_value = random.uniform(0, 1.0)
        #uslovie
        bump_node = self._create_noise_mask(material)
        material.node_tree.links.new(bsdf.outputs["BSDF"], material_output_node.inputs["Surface"])
        material.node_tree.links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

        if self.checker:
            checker_node = self._create_checker(material)
            material.node_tree.links.new(checker_node.outputs["Color"], bsdf.inputs["Base Color"])


    def _create_noise_mask(self, material):

        bump_node = material.node_tree.nodes.new(type="ShaderNodeBump")
        bump_node.inputs["Strength"].default_value = 2
        bump_node.inputs["Distance"].default_value = 0.2  #

        noise_texture_node = material.node_tree.nodes.new(type="ShaderNodeTexNoise")
        noise_texture_node.inputs['Scale'].default_value = random.uniform(5.0, 10.0)
        noise_texture_node.inputs['Detail'].default_value = random.uniform(2.5, 5.0)
        noise_texture_node.inputs['Roughness'].default_value = random.uniform(0.8, 1)

        mapping_node = material.node_tree.nodes.new(type="ShaderNodeMapping")
        mapping_node.inputs["Rotation"].default_value.x = math.radians(random.uniform(0.0, 360.0))
        mapping_node.inputs["Rotation"].default_value.y = math.radians(random.uniform(0.0, 360.0))
        mapping_node.inputs["Rotation"].default_value.z = math.radians(random.uniform(0.0, 360.0))

        texture_coordinate_node = material.node_tree.nodes.new(type="ShaderNodeTexCoord")

        material.node_tree.links.new(noise_texture_node.outputs["Color"], bump_node.inputs["Height"])
        material.node_tree.links.new(mapping_node.outputs["Vector"], noise_texture_node.inputs["Vector"])
        material.node_tree.links.new(texture_coordinate_node.outputs["Generated"], mapping_node.inputs["Vector"])
        return bump_node


    def _create_checker(self, material):
        checker_node = material.node_tree.nodes.new(type="ShaderNodeTexChecker")
        color1 = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 1.0)
        color2 = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 1.0)
        checker_node.inputs['Color1'].default_value = color1
        checker_node.inputs['Color2'].default_value = color2
        return checker_node


