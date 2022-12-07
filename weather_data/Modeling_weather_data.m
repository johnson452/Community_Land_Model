% Temperature model: 
% T = 55.0901 - 19.6674cos(2*pi*t/365) - 8.6196sin(2*pi*t/365)
% misfit = 0.1454

a = readcell("Weather_data_of_NJ.xlsx");
data = zeros([365,3]);

%data matrix contains [day of the year, avg. temp., avg. humidity]
for i = 1 : 365
    data(i,1) = i;
end
%input temperature
for i = 2:378
    if a{i,1} == 'Jan'
        for k = 1:31
            data(k,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Feb'
        for k = 1:28
            data(k+31,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Mar'
        for k = 1:31
            data(k+28+31,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Apr'
        for k = 1:30
            data(k+28+31+31,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'May'
        for k = 1:31
            data(k+28+31+31+30,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Jun'
        for k = 1:30
            data(k+31+28+31+31+30,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Jul'
        for k = 1:31
            data(k+31+28+31+31+30+30,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Aug'
        for k = 1:31
            data(k+31+28+31+31+30+30+31,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Sep'
        for k = 1:30
            data(k+31+28+31+31+30+30+31+31,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Oct'
        for k = 1:31
            data(k+31+28+31+31+30+30+31+31+30,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Nov'
        for k = 1:30
            data(k+31+28+31+31+30+30+31+31+30+31,3) = a{k+i,9};
        end
    end
    if a{i,1} == 'Dec'
        for k = 1:31
            data(k+31+28+31+31+30+30+31+31+30+31+30,3) = a{k+i,9};
        end
    end
end



%input humidity
for i = 2:378
    if a{i,1} == 'Jan'
        for k = 1:31
            data(k,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Feb'
        for k = 1:28
            data(k+31,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Mar'
        for k = 1:31
            data(k+28+31,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Apr'
        for k = 1:30
            data(k+28+31+31,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'May'
        for k = 1:31
            data(k+28+31+31+30,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Jun'
        for k = 1:30
            data(k+31+28+31+31+30,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Jul'
        for k = 1:31
            data(k+31+28+31+31+30+30,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Aug'
        for k = 1:31
            data(k+31+28+31+31+30+30+31,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Sep'
        for k = 1:30
            data(k+31+28+31+31+30+30+31+31,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Oct'
        for k = 1:31
            data(k+31+28+31+31+30+30+31+31+30,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Nov'
        for k = 1:30
            data(k+31+28+31+31+30+30+31+31+30+31,2) = a{k+i,3};
        end
    end
    if a{i,1} == 'Dec'
        for k = 1:31
            data(k+31+28+31+31+30+30+31+31+30+31+30,2) = a{k+i,3};
        end
    end
end

%Modeling using inverse method
%Assume the period of temperature changing is 365days via observing

T = 365;
t = linspace(1,365,365);
Ghat = [ones(365,1), cos(2*pi*t/T)', sin(2*pi*t/T)'];
mhat = pinv(Ghat)*data(:,2);
Temphat = Ghat * mhat;

%calculating misfit

phiT = var(Temphat-data(:,2))/var(data(:,2));

%%visually examine temperature estimation by running the codes below
% subplot(2,1,1)
% plot(data(:,1),data(:,2))
% 
% subplot(2,1,2)
% plot(data(:,1),Temphat)


