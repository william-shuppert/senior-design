from multiapp import MultiApp
from app1 import style_gan
from app2 import demo_app
from app3 import image_seg
from will_projects import object

backend = 'http://backend:8080'

home = MultiApp(backend)

home.add_category('Welcome', {'Welcome Page':demo_app.app})

home.add_category('demo apps1', {'Style Transfer':style_gan.app, 
                                    'image segmentation': image_seg.app})

home.add_category('demo apps2', {'image segmentation':image_seg.app,
                                 'object detection': object.app})


if __name__ == "__main__":
    home.run()
