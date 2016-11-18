close all;
i = imread('img/1479496954.jpg');

r = edge(i(:,:,1));
g = edge(i(:,:,2));
b = edge(i(:,:,3));

t = r+g+b;

subplot(1,2,1);imshow(i);
subplot(1,2,2);imshow(t);

%this works!