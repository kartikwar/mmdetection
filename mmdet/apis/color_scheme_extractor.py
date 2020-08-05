import cv2
from sklearn.cluster import KMeans
from collections import Counter
import json



class ColorScheme(object):

    def __init__(self, img_path, roi_coords_list):
    
        self.color_map = {}
    
        with open('resources/color_map.json') as cmp:
            self.color_map = json.load(cmp)
        
        self.img_path = img_path
        self.roi_coords_list = roi_coords_list
        self.color_scheme = {}
        self.number_of_clusters = 5

        self.im = self.get_image()
        
        # color scheme list will be a list of color counts for different products
        self.color_scheme_list = list(map(self.get_color_scheme_for_region, self.roi_coords_list))
        
        # once colour counts are obtained, get the color scheme
        # in percentage and return the complete color scheme
        self.extract_color_scheme()



    def extract_color_scheme(self):
        # color_scheme = {}
    
        # color scheme for each fashion product
        self.product_wise_color_scheme = self.extract_color_scheme_product_wise()
    
        # color scheme for all products combined
        self.overall_color_scheme = self.extract_color_scheme_overall()
    
        self.color_scheme.update(self.product_wise_color_scheme)
    
        self.color_scheme.update(self.overall_color_scheme)



    def get_image(self):
        image = cv2.imread(self.img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image



    def extract_color_scheme_product_wise(self):
        color_scheme = {}
        
        for ordered_colors, product_label in self.color_scheme_list:
            color_scheme[product_label] = self.convert_color_counts_to_percentages(ordered_colors)
    
        return color_scheme



    def get_name_of_color(self, color_array):
        requested_colour = (int(color_array[0]), int(color_array[1]), int(color_array[2]))
        
        min_colours = {}
        
        for key, name in self.color_map.items():
            r_c, g_c, b_c = name
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = key
        
        return min_colours[min(min_colours.keys())]



    def get_color_scheme_for_region(self, roi):
        product_label = roi[4]

        #reshape the image to feed it into KMEANS algorithm
        roi = self.im[roi[1]: roi[3], roi[0]: roi[2], :]
        
        roi = roi.reshape(roi.shape[0] * roi.shape[1], 3)
        
        clf = KMeans(n_clusters=self.number_of_clusters)
        labels = clf.fit_predict(roi)
        
        counts = Counter(labels)
        counts = [(key, val) for key, val in counts.items()]

        # sort to ensure correct color percentage
        counts = sorted(counts, key=lambda x: x[1], reverse=True)
        
        
        center_colors = clf.cluster_centers_
        
        ordered_cs = [(center_colors[i[0]], counts[i[0]][1]) for i in counts]
        
        ordered_colors = [(self.get_name_of_color(i[0]), i[1]) for i in ordered_cs]

        return (ordered_colors, product_label)



    def convert_color_counts_to_percentages(self, color_counts):
        color_scheme = {}
        counts_all_colours = 0
        unique_colours = list(set([color_count[0] for color_count in color_counts]))
        
        #calculate total count for each colour
        for index , color in enumerate(unique_colours):
            color_count = sum([color_count[1] for color_count in color_counts if color_count[0] == color])
            counts_all_colours += color_count
            unique_colours[index] = (unique_colours[index], color_count)
            

        #calculate percentage for each colour
        for index, color in enumerate(unique_colours):
            color_scheme[color[0]] = float("{:.2f}".format((color[1] * 100) / counts_all_colours))

        return color_scheme



    def extract_color_scheme_overall(self):
        color_scheme = {}
        
        color_counts = []
       
        for ordered_colors, product_label in self.color_scheme_list:
            color_counts = color_counts + ordered_colors

        color_scheme['overall'] =  self.convert_color_counts_to_percentages(color_counts)
        
        return color_scheme




