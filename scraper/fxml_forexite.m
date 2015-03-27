% function [data] = fxml_forexite(num_days,currencies)
% fxml_forexite - This function organizes the data downloaded as a bunch of
% .txt files using "scrape_forexite.py" to create a MATLAB data file
% 
% This function has 2 inputs:
% 1. num_days - number of days (files) of forex data to process
% 2. currencies - cell of the currency pairs with data
% 3. v - version number of the data
% ----v2 = all data from 2011. 312 days. 52 weeks. 370590 minutes. Missing
% 689 minutes from day 308, missing 1 minute from day 274)
%
% This function has 1 outputs:
% 1. forexite_# - output .mat file that has all the data from the .txt
% files
% 
% Possible changes: no linear interpolation: just keep same value until
% changed.
% 
% nov62011pairs = {'EURUSD','GBPUSD','USDCHF','USDJPY','EURGBP','EURCHF', ...
%     'EURJPY','GBPCHF','GBPJPY','CHFJPY','USDCAD','EURCAD','AUDUSD', ...
%     'AUDJPY','NZDUSD','NZDJPY','XAUUSD','XAGUSD','USDCZK','USDDKK', ...
%     'EURRUB','USDHUF','USDNOK','USDPLN','USDRUB','USDSEK','USDSGD','USDZAR'};
% 
%
% Created by: Scott Cole
% Copyright (c) 2014
% University of California, San Diego
% Neurosciences Graduate Program
clear
clc
close all

% User input
num_days = 12; %312 - numminutes should be 371280 (actual 370590, 690 diff)
out_finame = 'fxdata';

% Convert data from .txt to a cell array
for d = 1:num_days
    fprintf('%d\n',d)
    filename = strcat('fxday',num2str(d));
    data_table = readtable(filename);
    all_cell = table2cell(data_table);
    data_pairs = cell2mat(all_cell(:,1));
    data_times = cell2mat(all_cell(:,3));
    data1 = cell2mat(all_cell(:,4));
    
    %split up data by currency
    data_times(data_times==0)=240000;
    locs = findpeaks(data_times);
    bounds = [0; locs.loc; length(data_times)];
    for b = 2:length(bounds)
        interval = bounds(b-1)+1:bounds(b);
        data2{d,b-1} = [data_times(interval), data1(interval)];
        pairs{d,b-1} = data_pairs(bounds(b),1:6);
    end
    
    %interpolate missing values
    %find ideal time vector
    for c=1:size(data2,2)
        tlengths = length(data2{d,c});
    end
    [max_tlength max_tlength_index] = max(tlengths);
    time_vector{d} = data2{d,max_tlength_index}(:,1);
    date_vector{d} = all_cell{1,2};
    for c=1:size(data2,2)
        data3{d,c} = interp1(data2{d,c}(:,1),data2{d,c}(:,2),time_vector{d});
    end
end

% %Check to see if the currency pairs in the first day were the same as the last
% %day
% pairs_first = pairs(1,:);
% pairs_last = pairs(end,:);
% for i=1:length(pairs_last)
%     if pairs_first{i}~=pairs_last{i}
%         fprintf('ERROR: The currency pairs in the data are not the same each day.')
%         pause
%         manual_pairs=1;
%     end
% end
%
% %sort data manually by looking at each currency pair
% if manual_pairs
%     allpairs = pairs(1,:);
%     for d=1:size(data3,1)
%         day_pairs = pairs(d,:);
%         day_pairs = day_pairs(~cellfun('isempty',day_pairs));
%         for c=1:length(day_pairs)
%             for k = 1:length(allpairs)
%                 if day_pairs{c}==allpairs{k}
%                     data4{d,k} = data3{d,c};
%                 end
%             end
%         end
%     end
% else
%     data4=data3;
% end
        
pairs = pairs(1,:);

%Replace data3 cell matrix with a matrix with continuous data
total_minutes = 0;
for d=1:num_days
    total_minutes = total_minutes + length(data3{d,1});
end

fxdata = zeros(total_minutes,length(pairs{1,1}));
current_minute = 0;
for d=1:num_days
    for c=1:size(data3,2)
        interval = current_minute+1 : current_minute+length(data3{d,c});
        fxdata(interval,c) = data3{d,c};
    end
    current_minute = current_minute + length(data3{d,c});
end

save(out_finame,'fxdata','time_vector','date_vector','pairs')