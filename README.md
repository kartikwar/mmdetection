## Fashion Products Tagger


![demo image](resources/Figure_1.png)

### Major features

- **Output Product Type**
    
    Product type is identified along with confidence. For eg: top | 0.98
    
- **Bounding boxes are detected**
    
    Coordinates of the products are detected and displayed.

- **Color Scheme for Products**

    Color composition for products(combined and individually) is reported in a json format 
    
    {
        
        'top' : {
            'grey' : 76.23,
            'white' : 34.36
        },
        'overall' : {
            'grey' : 33.34,
            'black' : '23',
            'white' : '44'
        }
    }
    
- **Extensions**

   training script can be used to train on more data to increase the accuracy of detections


## License

This project is released under the [Apache 2.0 license](LICENSE).


## Benchmark and model zoo

model is available at [model g-drive](https://drive.google.com/file/d/1fol3hgl2IHee2f4wOj_TfTQ5hPQfeTl0/view?usp=sharing).


## Installation

Please refer to [install.md](docs/install.md) for installation and dataset preparation.


## Usage
python fashion_assignment.py --checkpoint checkpoints/fashion_product_detector --img images/04_6_flat.jpg

Pass the checkpoint path in the parameter(--checkpoint).

The trained model is available at [model g-drive](https://drive.google.com/file/d/1fol3hgl2IHee2f4wOj_TfTQ5hPQfeTl0/view?usp=sharing) 

Pass the input image path in the parameter(--img)

**Output**

Outputs an image with bounding boxes along with product type and color scheme.

## Contact

This repo was forked from https://github.com/open-mmlab/mmdetection and was changed by 
Kartik Sirwani([@kartikwar]) based on his requirements

