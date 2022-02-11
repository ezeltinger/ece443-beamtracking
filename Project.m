%% Cell and Users
% Circle
r1 = 1;
q1 = [0:0.1:2*pi];
x1 = r1*cos(q1);
y1 = r1*sin(q1);

% Users
ru = rand();
qu = 2*pi*rand();
xu = ru.*cos(qu);
yu = ru.*sin(qu);

plot(x1,y1,'-',xu,yu,'o')
hold on

% Sectors
sector_borders = [0, pi/2, pi, 3*pi/2, 2*pi];

for i = 1:length(sector_borders)-1
    ri = 1;
    qi = sector_borders(i);
    x = ri*cos(qi);
    y = ri*sin(qi);
    plot([0, x], [0, y], 'b')
end

for i = 1:length(sector_borders)-1
    sector = linspace(sector_borders(i), sector_borders(end), 50);
    if (qu >= sector_borders(i)) && (qu <= sector_borders(i+1))
        patch([0 cos(sector) 0], [0 sin(sector) 0], 'r');
    end
end

hold off