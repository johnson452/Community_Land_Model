% Temperature model:
% T = 55.0901 - 19.6674cos(2*pi*t/365) - 8.6196sin(2*pi*t/365)
% misfit = 0.1454

a = readcell("Weather_data_of_NJ.xlsx");
data = zeros([365,4]);

%data matrix contains [day of the year, avg. windspeed, avg. temp.]
for i = 1 : 365
    data(i,1) = i;
end
%input temperature
for i = 2:378
    if a{i,1} == 'Jan'
        for k = 1:31
            data(k,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Feb'
        for k = 1:28
            data(k+31,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Mar'
        for k = 1:31
            data(k+28+31,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Apr'
        for k = 1:30
            data(k+28+31+31,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'May'
        for k = 1:31
            data(k+28+31+31+30,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Jun'
        for k = 1:30
            data(k+31+28+31+31+30,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Jul'
        for k = 1:31
            data(k+31+28+31+31+30+30,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Aug'
        for k = 1:31
            data(k+31+28+31+31+30+30+31,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Sep'
        for k = 1:30
            data(k+31+28+31+31+30+30+31+31,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Oct'
        for k = 1:31
            data(k+31+28+31+31+30+30+31+31+30,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Nov'
        for k = 1:30
            data(k+31+28+31+31+30+30+31+31+30+31,3) = a{k+i,3};
        end
    end
    if a{i,1} == 'Dec'
        for k = 1:31
            data(k+31+28+31+31+30+30+31+31+30+31+30,3) = a{k+i,3};
        end
    end
end



%input windspeed
for i = 2:378
    if a{i,1} == 'Jan'
        for k = 1:31
            data(k,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Feb'
        for k = 1:28
            data(k+31,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Mar'
        for k = 1:31
            data(k+28+31,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Apr'
        for k = 1:30
            data(k+28+31+31,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'May'
        for k = 1:31
            data(k+28+31+31+30,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Jun'
        for k = 1:30
            data(k+31+28+31+31+30,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Jul'
        for k = 1:31
            data(k+31+28+31+31+30+30,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Aug'
        for k = 1:31
            data(k+31+28+31+31+30+30+31,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Sep'
        for k = 1:30
            data(k+31+28+31+31+30+30+31+31,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Oct'
        for k = 1:31
            data(k+31+28+31+31+30+30+31+31+30,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Nov'
        for k = 1:30
            data(k+31+28+31+31+30+30+31+31+30+31,2) = a{k+i,12};
        end
    end
    if a{i,1} == 'Dec'
        for k = 1:31
            data(k+31+28+31+31+30+30+31+31+30+31+30,2) = a{k+i,12};
        end
    end
end


%Modeling using inverse method
%Assume the period of temperature changing is 365days via observing
%periodogram(data(:,2)-mean(data(:,2)),hann(length(data(:,2))))

figure(1)
T = 365;
t = linspace(1,365,365);
Ghat = [ones(365,1), cos(2*pi*t/T)', sin(2*pi*t/T)'];
mhat = pinv(Ghat)*data(:,3);
Temphat = Ghat * mhat;
plot(data(:,1),Temphat)
hold on
plot(data(:,1),data(:,3))
%calculating variance reduction

phiT = var(Temphat-data(:,3))/var(data(:,3));

mean(data(:,2))
std(data(:,2))
figure(2)
plot(())
% figure(2)
% periodogram(data(:,2) - mean(data(:,2)))
% %peak at 0.003906
%
% figure(3)
% T = 90;
% t = linspace(1,365,365);
% Ghat_w = [ones(365,1), cos(2*pi*t/T)', sin(2*pi*t/T)'];
% mhat_w = pinv(Ghat_w)*data(:,2);
% Windhat = Ghat_w * mhat_w;
% plot(data(:,1),Windhat)
% hold on
% plot(data(:,1),data(:,2))


%%visually examine temperature estimation by running the codes below
% subplot(2,1,1)
% plot(data(:,1),data(:,2))
%
% subplot(2,1,2)
% plot(data(:,1),Temphat)

% % plot (data(:,1),data(:,3))
% GhatH = [ones(365,1), cos(2*pi*t/10)', sin(2*pi*t/10)'];
% mhatH = pinv(GhatH)*data(:,3);
% Hhat = GhatH * mhatH;
% phiH = var(Hhat-data(:,3))/var(data(:,3));
% plot(data(:,1),Hhat)
