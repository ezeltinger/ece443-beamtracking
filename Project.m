%% Cell and Users

r1 = 1;
q1 = [0:0.1:2*pi];
x1 = r1*cos(q1);
y1 = r1*sin(q1);

r = rand(10,1);
q = 2*pi*rand(10,1);
x = r.*cos(q);
y = r.*sin(q);

plot(x1,y1,'-',x,y,'o')