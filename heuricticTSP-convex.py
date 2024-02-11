from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import numpy as np

# ulysee16
data=[[38.24, 20.42],[39.57, 26.15],[40.56, 25.32],[36.26, 23.12],[33.48, 10.54],[37.56, 12.19],
        [38.42, 13.11],[37.52, 20.44],[41.23 ,9.10],[41.17,13.05],[36.08, -5.21],[38.47, 15.13],
        [38.15, 15.35],[37.51, 15.17],[35.49, 14.32],[39.36, 19.56]]

points=np.array(data)

hull = ConvexHull(points)

V1=[]
for i in hull.vertices:
    V1.append(i)
V1=np.array(V1)

V2=[]
for element in range(len(data)):
    if element not in V1:
        V2.append(element)
V2=np.array(V2)


sumx=0
sumy=0
for element in range(len(data)):
    if element in V2:
        sumx=sumx+data[element][0]
        sumy=sumy+data[element][1]

center= sumx/len(V2),sumy/len(V2)

from scipy.spatial import distance
minimum=9999999999999
for element in V2:
    dst = distance.euclidean(center, data[element])
    if dst<minimum:
        minimum=dst
        centroid=element

fig, (ax1, ax2,ax3) = plt.subplots(ncols=3, figsize=(10, 3))

for ax in (ax1, ax2,ax3):
    # plt.xlim(24, 1745)
    # plt.ylim(4, 1176)
    if ax == ax1:
        ax.plot(points[:, 0], points[:, 1], '.', color='k')
        ax.set_title('Given points')
    elif ax == ax2:
        ax.plot(points[:, 0], points[:, 1], '.', color='k')
        ax.set_title('Convex hull')
        for simplex in hull.simplices:
           
            ax.plot(points[simplex, 0], points[simplex, 1], 'c')
        ax.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'o', mec='r', color='none', lw=1, markersize=10)
    else:
        ax.set_title('Center of non-hull points')
        ax.plot(points[V2, 0], points[V2, 1], '.', color='k')
        ax.plot(points[centroid,0],points[centroid,1], 'o', mec='r', color='none', lw=1, markersize=8)
plt.show()

tour=hull.vertices
# merkezdeki tepeden V2 deki tüm tepelere uzaklıkları bulur ve azalan sırada sıralar
dst_from_centroid= [0 for _ in range(len(V2))]
i=0
for element in V2:
    dst = np.linalg.norm(np.array(data[centroid])-np.array(data[element]))
    dst_from_centroid[i]=[dst,element]
    i=i+1
dst_from_centroid.sort(reverse=False)

for i in range(len(dst_from_centroid)):
    min_distance=999999999999
    for element in range(len(tour)):
        source=tour[element]
        if element==len(tour)-1:
            target=tour[0]
        else:
            target=tour[element+1]
        dst1 = distance.euclidean(data[dst_from_centroid[i][1]], data[source])
        dst2 = distance.euclidean(data[dst_from_centroid[i][1]], data[target])
        dst_edge=distance.euclidean(data[source], data[target])
        if dst1+dst2-dst_edge<min_distance:
            min_distance=dst1+dst2-dst_edge
            new_source=source
            new_target=target
            
    for element in range(len(tour)):
        first_v=tour[element]
        if element==len(tour)-1:
            second_v=tour[0]
        else:
            second_v=tour[element+1]
        if first_v==new_source and second_v==new_target:
            tour=np.insert(tour,element+1,dst_from_centroid[i][1])
        if first_v==new_target and second_v==new_source:
            tour=np.insert(tour,element+1,dst_from_centroid[i][1])
            


#tour uzunluğu hesaplama
total=0
for element in range(len(tour)):
    source=tour[element]
    if element==len(tour)-1:
        target=tour[0]
    else:
        target=tour[element+1]
    total = total+ distance.euclidean(data[source], data[target])
print("Total length of tour=",total)

plt.plot(points[:, 0], points[:, 1], '.', color='k')
for element in range(len(tour)):
    source=tour[element]
    if element==len(tour)-1:
        target=tour[0]
    else:
        target=tour[element+1]
    x_values = [points[source][0], points[target][0]]
    y_values = [points[source][1], points[target][1]]
    plt.plot(x_values,y_values,'b')
#plt.plot(points[tour, 0], points[tour, 1], 'o', mec='r', color='none', lw=1, markersize=10)
plt.plot(points[centroid,0],points[centroid,1], 'o', mec='r', color='none', lw=1, markersize=8)