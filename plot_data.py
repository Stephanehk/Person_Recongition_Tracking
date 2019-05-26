import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
# import plot_matrix
import cv2

#
# def add_text(dists):
#     time = 0
#     for dist in dists:
#         time = time + 15
#         text = dist, 'km in', time,'mins'
#         text(0, (.75 *dist), text, fontsize=12)

def plot (matrix, dists):
    time = 0
    fig = np.array(matrix)
    fig = plt.figure(figsize=(6, 3.2))
    for dist in dists:
        time = time + 15
        text = round(dist,0), time
        # fig.text(.5, (.015 *dist), text, fontsize=6)
        fig.text(0.5, .475 +(.015 *dist), text,fontsize=8, horizontalalignment='center', verticalalignment='center')

    plt.axis('off')

    #ax = fig.add_subplot(111)
    #ax.set_title('colorMap')

    plt.imshow(matrix)
    fig.savefig("mapped_area.png",transparent = True, bbox_inches = 'tight', pad_inches = 0)

    # ax.set_aspect('equal')
    #
    # cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    # cax.get_xaxis().set_visible(False)
    # cax.get_yaxis().set_visible(False)
    # cax.patch.set_alpha(0)
    # cax.set_frame_on(False)
    # plt.colorbar(orientation='vertical')
    #plt.show()

def replace_img (l_img,s_img):
    y_offset = 0
    x_offset = 0
    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]

    alpha_s = s_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                  alpha_l * l_img[y1:y2, x1:x2, c])
    return l_img

def edit_image (map_img):
    img = cv2.imread("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/mapped_area.png",-1)
    h,w,c = map_img.shape
    #print (str(h) + str(" , ") + str(w))
    # img = cv2.resize(img,(h,w))
    #overlayed = cv2.addWeighted(map_img,0.4,img,0.1,0)

    overlayed = replace_img (map_img,img)

    cv2.imshow("overlayed", overlayed)
    cv2.waitKey(0)

#map = cv2.imread("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/map.png",-1)
# img, dists = plot_matrix.run(20000,50)
# plot (img, dists)
#edit_image (map)
