import cv2
from sklearn.cluster import KMeans
from collections import Counter
import webcolors
import json

color_map = {}

with open('resources/color_map.json') as cmp:
    color_map = json.load(cmp)


class ColorScheme(object):
    """A simple pipeline to load image."""

    def __init__(self, img_path, roi_coords_list):
        self.img_path = img_path
        self.roi_coords_list = roi_coords_list
        self.color_scheme = {}
        self.number_of_clusters = 8
        self.extract_color_scheme()



    def extract_color_scheme(self):
        # color_scheme = {}
        self.im = self.get_image()
    
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
    
        for roi_coord in self.roi_coords_list:
            roi = self.im[roi_coord[1]: roi_coord[3], roi_coord[0]: roi_coord[2], :]
        
            ordered_colors = self.get_color_scheme_for_region(roi)
        
            # the fourth coordinate represents the product label
            color_scheme[roi_coord[4]] = self.convert_color_counts_to_percentages(ordered_colors)
    
        return color_scheme




    def get_name_of_color(self, color_array):
        requested_colour = (int(color_array[0]), int(color_array[1]), int(color_array[2]))
        
        min_colours = {}
        
        # for key, name in webcolors.css3_hex_to_names.items():
        for key, name in color_map.items():
            r_c, g_c, b_c = name
            # if name == 'black':
            #     lol = 0
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = key
        
        return min_colours[min(min_colours.keys())]



    def get_percentages(self, colors_count):
        percentages = []
        total_sum = sum([a[1] for a in colors_count])
        percentages = [(a[0], (a[1] * 100) / total_sum) for a in colors_count]
        return percentages


    def get_color_scheme_for_region(self, roi):
        #reshape the image to feed it into KMEANS algorithm
        roi = roi.reshape(roi.shape[0] * roi.shape[1], 3)
        
        clf = KMeans(n_clusters=self.number_of_clusters)
        labels = clf.fit_predict(roi)
        
        counts = Counter(labels)
        counts = [(key, val) for key, val in counts.items()]

        # sort to ensure correct color percentage
        counts = sorted(counts, key=lambda x: x[1], reverse=True)
        
        
        center_colors = clf.cluster_centers_
        
        ordered_cs = [(center_colors[i[0]], counts[i[0]][1]) for i in counts]
        
        # We get ordered colors by iterating through the keys
        ordered_colors = [(self.get_name_of_color(i[0]), i[1]) for i in ordered_cs]
        # ordered_colors_lib = [(get_name_of_color_lib(i[0]), i[1]) for i in ordered_cs]
        percenatges = self.get_percentages(ordered_colors)
        temp = 0
        
        return ordered_colors







    def convert_color_counts_to_percentages(self, color_counts):
        color_scheme = {}
        
        temp = 0
        
        counts_all_colours = 0
        
        unique_colours = list(set([color_count[0] for color_count in color_counts]))
        
        
        #calculate total count for each colour
        for index , color in enumerate(unique_colours):
            
            color_count = sum([color_count[1] for color_count in color_counts if color_count[0] == color])
            
            counts_all_colours += color_count
            
            unique_colours[index] = (unique_colours[index], color_count)
            
        
        
            
            temp = 0

        #calculate percentage for each colour
        for index, color in enumerate(unique_colours):
            # color_count = sum([color_count[1] for color_count in color_counts if color_count[0] == color])
        
            # counts_all_colours += color_count
            #
            # unique_colours[index] = (unique_colours[index], color_count)
        
            color_scheme[color[0]] = (color[1] * 100) / counts_all_colours

        return color_scheme


    def extract_color_scheme_overall(self):
        color_scheme = {}
        
        color_counts = []
        
        
        for roi_coord in self.roi_coords_list:
            roi = self.im[roi_coord[1]: roi_coord[3], roi_coord[0]: roi_coord[2], :]
            
            ordered_colors = self.get_color_scheme_for_region(roi)
            
            color_counts = color_counts + ordered_colors
            
            # temp = 0
       
        color_scheme['overall'] =  self.convert_color_counts_to_percentages(color_counts)
        
        return color_scheme




