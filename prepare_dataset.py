import os
import  json

image_schema = {
    'file_name' : 'img/MEN/lol.jpg',
    'height' : 1101,
    'width' : 450,
    'id' : '00000000000'
}

images = [
    
    image_schema
]

annotation_schema = {
    'segmentation' : [[1.0, 2.0]],
    'area' : 292116,
    'iscrowd' : 0,
    'image_id' : '00000000000',
    'bbox' : [56, 247, 573, 755],
    'id' : '1',
    'category_id' : '1'
}

annotations = [
    annotation_schema
]


category_schema = {
    'supercategory' : 'CLOTHES',
    'id': '1',
    'name' : 'top'
}

categories = [
    category_schema
]


category_id_map = {
    1 : 'top',
    2 : 'skirt',
    3 : 'leggings',
    4 : 'dress',
    5 : 'outer',
    6 : 'pants',
    7: 'bag',
    8 : 'neckwear',
    9: 'headwear',
    10: 'eyeglass',
    11: 'belt',
    12 : 'footwear',
    13: 'hair',
    14: 'skin',
    15 : 'face'
}

ignore_categories = [13, 14, 15]

schema = {
    'info' : 'info',
    'images' : images,
    'annotations' : annotations,
    'categories' : categories
}








def generate_dataset(json_path):
    schema = {}
    
    with open(json_path) as jp:
        ann = json.load(jp)
    
    keys = ann.keys()
    
    for key in keys:
        schema[key] = None
    #
    schema['info'] = ann['info']
    schema['images'] = ann['images']
    schema['categories'] = ann['categories']
    schema["annotations"] = []
    
    
    for annotation in ann['annotations']:
        category_id = annotation['category_id']
        if category_id not in ignore_categories:
            schema['annotations'].append(annotation)

    
    output_dir = '/'.join(json_path.split('/')[:-1])
    
    output_path =  json_path.split('/')[-1].replace('.json', '_custom.json')

    output_path = os.path.join(output_dir, output_path)

    with open(output_path, 'w') as keyj:
        json.dump(schema, keyj)




    







    
    

if __name__ == '__main__':
    json_path = 'data/DeepFashion/In-shop/Anno/segmentation/DeepFashion_segmentation_train.json'
    
    json_path = os.path.join(os.getcwd(), json_path)
   
    if os.path.exists(json_path):
        schema = generate_dataset(json_path=json_path)
    
